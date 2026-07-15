"""Small GitHub GraphQL client with clear failure modes."""

from __future__ import annotations

import logging
from typing import Any

import requests


LOGGER = logging.getLogger(__name__)


class GitHubGraphQLError(RuntimeError):
    """Raised when GitHub GraphQL returns an error payload."""


class GitHubClient:
    """Execute authenticated GitHub GraphQL requests."""

    def __init__(self, token: str, graphql_url: str) -> None:
        self.graphql_url = graphql_url
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "onkar0629-profile-engine",
            }
        )

    def execute(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        """Run a GraphQL query and return the decoded response data."""

        LOGGER.info("Requesting GitHub GraphQL data")
        response = self.session.post(
            self.graphql_url,
            json={"query": query, "variables": variables},
            timeout=30,
        )

        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise RuntimeError(
                f"GitHub GraphQL request failed with HTTP {response.status_code}"
            ) from exc

        payload: dict[str, Any] = response.json()
        errors = payload.get("errors")
        if errors:
            messages = "; ".join(error.get("message", str(error)) for error in errors)
            raise GitHubGraphQLError(f"GitHub GraphQL returned errors: {messages}")

        data = payload.get("data")
        if not isinstance(data, dict):
            raise GitHubGraphQLError("GitHub GraphQL response did not include data.")

        return data
