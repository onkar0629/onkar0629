from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GRAPHQL_URL = "https://api.github.com/graphql"
