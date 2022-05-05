import click
from codeowners import CodeOwners


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
