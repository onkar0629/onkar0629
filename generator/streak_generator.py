"""Business logic for GitHub contribution streak metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import TYPE_CHECKING, Any

from generator.github_queries import PROFILE_QUERY

if TYPE_CHECKING:
    from generator.github_client import GitHubClient


@dataclass(frozen=True)
class ContributionDay:
    day: date
    count: int


@dataclass(frozen=True)
class StreakMetrics:
    username: str
    display_name: str
    current_streak: int
    longest_streak: int
    total_contributions: int
    contributions_today: int
    repositories: int
    followers: int
    following: int
    stars: int
    commits: int
    last_updated: datetime
    from_date: date
    to_date: date


class StreakGenerator:
    def __init__(self, client: "GitHubClient", username: str) -> None:
        self.client = client
        self.username = username

    def generate(self, lookback_days: int = 366) -> StreakMetrics:
        now = datetime.now(timezone.utc)

        request_to = now.date()
        request_from = request_to - timedelta(days=lookback_days)

        data = self.client.execute(
            PROFILE_QUERY,
            {
                "login": self.username,
                "from": self._date_time(request_from),
                "to": self._date_time(request_to, end_of_day=True),
            },
        )

        user = data.get("user")
        if not isinstance(user, dict):
            raise RuntimeError(f"GitHub user '{self.username}' was not found.")

        calendar = user["contributionsCollection"]["contributionCalendar"]
        collection = user["contributionsCollection"]
        repositories = user["repositories"]

        days = self._parse_days(calendar["weeks"])

        if not days:
            raise RuntimeError("No contribution data returned by GitHub.")

        days_by_date = {d.day: d.count for d in days}

        latest_day = days[-1].day
        earliest_day = days[0].day

        repository_nodes = repositories.get("nodes") or []

        return StreakMetrics(
            username=user["login"],
            display_name=user.get("name") or user["login"],
            current_streak=self._current_streak(days_by_date, latest_day),
            longest_streak=self._longest_streak(days),
            total_contributions=int(calendar["totalContributions"]),
            contributions_today=int(days_by_date.get(latest_day, 0)),
            repositories=int(repositories["totalCount"]),
            followers=int(user["followers"]["totalCount"]),
            following=int(user["following"]["totalCount"]),
            stars=sum(int(repo.get("stargazerCount", 0)) for repo in repository_nodes),
            commits=int(collection["totalCommitContributions"]),
            last_updated=now,
            from_date=earliest_day,
            to_date=latest_day,
        )

    @staticmethod
    def _date_time(value: date, end_of_day: bool = False) -> str:
        t = time.max if end_of_day else time.min
        return datetime.combine(value, t, tzinfo=timezone.utc).isoformat()

    @staticmethod
    def _parse_days(weeks: list[dict[str, Any]]) -> list[ContributionDay]:
        days: list[ContributionDay] = []

        for week in weeks:
            for item in week["contributionDays"]:
                days.append(
                    ContributionDay(
                        day=date.fromisoformat(item["date"]),
                        count=int(item["contributionCount"]),
                    )
                )

        return sorted(days, key=lambda d: d.day)

    @staticmethod
    def _current_streak(days_by_date: dict[date, int], latest_day: date) -> int:
        cursor = latest_day

        # If the latest calendar day has no contributions,
        # the streak can still be active.
        if days_by_date.get(cursor, 0) == 0:
            cursor -= timedelta(days=1)

        streak = 0

        while True:
            count = days_by_date.get(cursor)

            if count is None or count == 0:
                break

            streak += 1
            cursor -= timedelta(days=1)

        return streak

    @staticmethod
    def _longest_streak(days: list[ContributionDay]) -> int:
        if not days:
            return 0

        longest = 0
        current = 0
        previous_day: date | None = None

        for day in days:
            if day.count > 0:
                if previous_day is None:
                    current = 1
                elif day.day == previous_day + timedelta(days=1):
                    current += 1
                else:
                    current = 1

                longest = max(longest, current)
                previous_day = day.day
            else:
                current = 0
                previous_day = day.day

        return longest
