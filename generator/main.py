from config import GITHUB_USERNAME
from client import GitHubClient
from queries import PROFILE_QUERY


def main():

    client = GitHubClient()

    result = client.execute(
        PROFILE_QUERY,
        {
            "login": GITHUB_USERNAME
        }
    )

    user = result["data"]["user"]

    print(f"Username     : {user['login']}")
    print(f"Name         : {user['name']}")
    print(f"Followers    : {user['followers']['totalCount']}")
    print(f"Following    : {user['following']['totalCount']}")
    print(f"Repositories : {user['repositories']['totalCount']}")


if __name__ == "__main__":
    main()
