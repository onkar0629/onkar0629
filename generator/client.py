import requests

from config import GRAPHQL_URL, GITHUB_TOKEN


class GitHubClient:

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}"
        }

    def execute(self, query: str, variables=None):

        response = requests.post(
            GRAPHQL_URL,
            json={
                "query": query,
                "variables": variables or {}
            },
            headers=self.headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise Exception(data["errors"])

        return data
