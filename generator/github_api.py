import requests

from config import (
    GITHUB_GRAPHQL_URL,
    GITHUB_TOKEN
)


class GitHubAPI:

    def __init__(self):

        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}"
        }

    def query(self, query: str):

        response = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query},
            headers=self.headers
        )

        response.raise_for_status()

        return response.json()
