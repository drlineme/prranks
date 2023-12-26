import requests
from github import Github


def get_discussion_titles(repo_owner, repo_name, github_token):
    """
    Retrieves discussion titles from a GitHub repository using the GraphQL API.

    :param repo_owner: The owner of the repository.
    :param repo_name: The name of the repository.
    :param github_token: GitHub personal access token with appropriate permissions.
    :return: List of discussion titles.
    """
    try:
        # GraphQL query to retrieve discussion titles
        query = """
        {
          repository(owner: "%s", name: "%s") {
            discussions(first: 10) {
              nodes {
                title
              }
            }
          }
        }
        """ % (repo_owner, repo_name)

        # Make a GraphQL request
        headers = {"Authorization": f"Bearer {github_token}"}
        response = requests.post("https://api.github.com/graphql", json={"query": query}, headers=headers)

        # Extract discussion titles from the response
        discussion_titles = [discussion["title"] for discussion in response.json()["data"]["repository"]["discussions"]["nodes"]]

        return discussion_titles

    except Exception as e:
        # Handle exceptions, such as authentication errors or repository not found
        print(f"Error: {str(e)}")
        return []


def check_file_existence(repo_owner, repo_name, file_path, github_token):
    """
    Checks if a file exists in a GitHub repository using PyGithub.

    :param repo_owner: The owner of the repository.
    :param repo_name: The name of the repository.
    :param file_path: The path to the file in the repository.
    :param github_token: GitHub personal access token with appropriate permissions.
    :return: True if the file exists, False otherwise.
    """
    try:
        # Authenticate with GitHub using the provided token
        g = Github(github_token)

        # Get the specified repository
        repo = g.get_repo(f"{repo_owner}/{repo_name}")

        # Get the contents of the repository at the specified file path
        repo.get_contents(file_path)

        # If contents exist, the file exists
        return True

    except Exception as e:
        # If the file is not found, handle the exception and return False
        if "Not Found" in str(e):
            return False
        else:
            # Handle other exceptions, such as authentication errors or repository not found
            print(f"Error: {str(e)}")
            return False
