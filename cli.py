import click

from codeowners_cli.owners.commands import owners


@click.group()
def cli():
    pass


cli.add_command(owners)

if __name__ == "__main__":
    cli()
