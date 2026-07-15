from client import GitHubClient
from queries import VIEWER_QUERY


client = GitHubClient()

result = client.execute(VIEWER_QUERY)

print(result)
