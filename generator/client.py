import requests

from config import (
    GRAPHQL_URL,
    GITHUB_TOKEN
)


class GitHubClient:

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}"
        }

    def execute(self, query: str):

        response = requests.post(
            GRAPHQL_URL,
            json={"query": query},
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
