"""Business logic for GitHub contribution streak metrics."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from typing import TYPE_CHECKING, Any

from generator.github_queries import CONTRIBUTIONS_QUERY

if TYPE_CHECKING:
    from generator.github_client import GitHubClient


@dataclass(frozen=True)
class ContributionDay:
    """One calendar day from GitHub's contribution calendar."""

    day: date
    count: int


@dataclass(frozen=True)
class StreakMetrics:
    """Computed values displayed on the streak card."""

    username: str
    display_name: str
    current_streak: int
    longest_streak: int
    total_contributions: int
    contributions_today: int
    last_updated: datetime
    from_date: date
    to_date: date


class StreakGenerator:
    """Fetch GitHub contribution data and compute streak statistics."""

    def __init__(self, client: "GitHubClient", username: str) -> None:
        self.client = client
        self.username = username

    def generate(self, lookback_days: int = 366) -> StreakMetrics:
        """Return streak metrics for the configured user."""

        now = datetime.now(timezone.utc)
        to_date = now.date()
        from_date = to_date - timedelta(days=lookback_days)

        data = self.client.execute(
            CONTRIBUTIONS_QUERY,
            {
                "login": self.username,
                "from": self._date_time(from_date),
                "to": self._date_time(to_date, end_of_day=True),
            },
        )

        user = data.get("user")
        if not isinstance(user, dict):
            raise RuntimeError(f"GitHub user '{self.username}' was not found.")

        calendar = user["contributionsCollection"]["contributionCalendar"]
        days = self._parse_days(calendar["weeks"])
        days_by_date = {item.day: item.count for item in days}

        return StreakMetrics(
            username=user["login"],
            display_name=user.get("name") or user["login"],
            current_streak=self._current_streak(days_by_date, to_date),
            longest_streak=self._longest_streak(days),
            total_contributions=int(calendar["totalContributions"]),
            contributions_today=int(days_by_date.get(to_date, 0)),
            last_updated=now,
            from_date=from_date,
            to_date=to_date,
        )

    @staticmethod
    def _date_time(value: date, end_of_day: bool = False) -> str:
        day_time = time.max if end_of_day else time.min
        return datetime.combine(value, day_time, tzinfo=timezone.utc).isoformat()

    @staticmethod
    def _parse_days(weeks: list[dict[str, Any]]) -> list[ContributionDay]:
        days: list[ContributionDay] = []
        for week in weeks:
            for item in week.get("contributionDays", []):
                days.append(
                    ContributionDay(
                        day=date.fromisoformat(item["date"]),
                        count=int(item["contributionCount"]),
                    )
                )
        return sorted(days, key=lambda item: item.day)

    @staticmethod
    def _current_streak(days_by_date: dict[date, int], to_date: date) -> int:
        streak = 0
        cursor = to_date

        while days_by_date.get(cursor, 0) > 0:
            streak += 1
            cursor -= timedelta(days=1)

        return streak

    @staticmethod
    def _longest_streak(days: list[ContributionDay]) -> int:
        longest = 0
        current = 0

        for item in days:
            if item.count > 0:
                current += 1
                longest = max(longest, current)
            else:
                current = 0

        return longest
