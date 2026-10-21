import os
from github import Github


def get_github_client(token=None):
    token = token or os.getenv("GITHUB_TOKEN")

    if not token:
        return None

    return Github(token)


def get_user_info(token=None):
    github = get_github_client(token)

    if github is None:
        return None

    user = github.get_user()

    return {
        "login": user.login,
        "name": user.name,
        "email": user.email,
        "public_repos": user.public_repos
    }


def get_repositories(token=None):
    github = get_github_client(token)

    if github is None:
        return []

    user = github.get_user()

    repositories = []

    for repo in user.get_repos():

        repositories.append({
            "name": repo.name,
            "full_name": repo.full_name,
            "private": repo.private,
            "url": repo.html_url
        })

    return repositories


def get_recent_commits(
    repository_name,
    token=None,
    limit=20
):
    github = get_github_client(token)

    if github is None:
        return []

    repo = github.get_repo(
        repository_name
    )

    commits = []

    for commit in repo.get_commits()[:limit]:

        commits.append({
            "sha": commit.sha,
            "message": commit.commit.message,
            "author": (
                commit.author.login
                if commit.author
                else None
            ),
            "date": str(
                commit.commit.author.date
            )
        })

    return commits


def get_pull_requests(
    repository_name,
    token=None,
    state="all"
):
    github = get_github_client(token)

    if github is None:
        return []

    repo = github.get_repo(
        repository_name
    )

    pull_requests = []

    for pr in repo.get_pulls(
        state=state
    ):

        pull_requests.append({
            "number": pr.number,
            "title": pr.title,
            "state": pr.state,
            "merged": pr.merged,
            "url": pr.html_url
        })

    return pull_requests