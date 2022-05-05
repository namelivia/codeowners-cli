import click
import os
from codeowners import CodeOwners
from git import Repo
from github import Github
from collections import Counter


@click.group()
def owners():
    pass


@click.command()
@click.option("--path", help="The path for the file to check", required=True)
@click.option("--owners_file_path", help="The path for codeowners file", required=True)
def get(path, owners_file_path):
    try:
        with open(owners_file_path) as f:
            content = f.read()
            owners = CodeOwners(content)
            click.echo(owners.of(path))
    except Exception as e:  # TODO: Try restricting the exception to have better granularity
        click.echo(click.style(str(e), fg="red"))


owners.add_command(get)


def get_owners_for_file(repo, path):
    authors = dict()
    for commit, lines in repo.blame("HEAD", path):
        if commit.author.email not in authors:
            authors[commit.author.email] = 1
        else:
            authors[commit.author.email] += 1
    return authors


def get_user_teams(email, token, organization):
    user_teams = []
    github = Github(token)
    org = github.get_organization(organization)
    teams = org.get_teams()
    try:
        users = list(github.search_users(f"{email} in:email"))
        if len(users) == 0:
            return []  # email not found
        user = github.get_user(users[0].login)
        for team in teams:
            if team.has_in_members(user):
                user_teams.append(team)
        return user_teams
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))
        return []


@click.command()
@click.option("--path", help="The path for the file to check", required=True)
@click.option("--owners_file_path", help="The path for codeowners file", required=True)
@click.option("--repo", help="The path for repo root", required=True)
@click.option("--token", help="Access token to access Github", required=False)
@click.option("--organization", help="Organization name", required=False)
def suggest(path, owners_file_path, repo, token=None, organization=None):
    try:
        repo_path = repo
        full_path = os.path.join(repo, path)
        repo = Repo(repo)
        assert not repo.bare
        if not os.path.isdir(full_path):
            total_authors = get_owners_for_file(repo, path)
        else:
            authors = []
            complete_files = []
            for root, dir_names, file_names in os.walk(full_path):
                for f in file_names:
                    complete_files.append(os.path.join(root, f))
            for file in complete_files:
                path = file.replace(repo_path + "/", "")
                authors.append(get_owners_for_file(repo, path))
            total_authors = sum((Counter(dict(x)) for x in authors), Counter())

        total = sum(total_authors.values())
        sorted_authors = dict(
            sorted(total_authors.items(), key=lambda item: item[1], reverse=True)
        )
        for author, lines in sorted_authors.items():
            if token is not None and organization is not None:
                author_teams = " ".join(
                    [team.name for team in get_user_teams(author, token, organization)]
                )
            else:
                author_teams = " "
            percentage = lines / total * 100
            click.echo(f"{author_teams} ({author}) : {percentage} %")
    except Exception as e:  # TODO: Try restricting the exception to have better granularity
        click.echo(click.style(str(e), fg="red"))


owners.add_command(suggest)
