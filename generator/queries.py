PROFILE_QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    name
    followers {
      totalCount
    }
    following {
      totalCount
    }
    repositories(
      ownerAffiliations: OWNER
      privacy: PUBLIC
    ) {
      totalCount
    }
  }
}
"""
