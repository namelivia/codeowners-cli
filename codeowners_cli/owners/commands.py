import click
from codeowners import CodeOwners
from git import Repo


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


@click.command()
@click.option("--path", help="The path for the file to check", required=True)
@click.option("--owners_file_path", help="The path for codeowners file", required=True)
@click.option("--repo", help="The path for repo root", required=True)
def suggest(path, owners_file_path, repo):
    try:
        repo = Repo(repo)
        assert not repo.bare
        authors = dict()
        for commit, lines in repo.blame("HEAD", path):
            if commit.author.email not in authors:
                authors[commit.author.email] = 1
            else:
                authors[commit.author.email] += 1
        total = sum(authors.values())
        sorted_authors = dict(
            sorted(authors.items(), key=lambda item: item[1], reverse=True)
        )
        for author, lines in sorted_authors.items():
            percentage = lines / total * 100
            click.echo(f"{author} : {percentage} %")
    except Exception as e:  # TODO: Try restricting the exception to have better granularity
        click.echo(click.style(str(e), fg="red"))


owners.add_command(suggest)
