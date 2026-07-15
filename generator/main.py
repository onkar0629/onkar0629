from github_api import GitHubAPI

query = """
{
  viewer {
    login
    name
  }
}
"""

api = GitHubAPI()

response = api.query(query)

print(response)
