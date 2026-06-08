"""Main CLI entrypoint using Click."""

import click
from cli.auth import auth_group
from cli.git_wrapper import git_group


@click.group()
def cli():
    """Colab-GitHub Bridge CLI - Connect Colab notebooks with GitHub repositories."""
    pass


# Add command groups
cli.add_command(auth_group, name="auth")
cli.add_command(git_group, name="git")


@cli.command()
@click.option("--repo", type=str, help="Repository URL or path")
def status(repo):
    """Show current repository status."""
    click.echo(f"Checking status for: {repo or 'current directory'}")
    click.echo("Status: OK")


@cli.command()
@click.option("--version", is_flag=True, help="Show version")
def info(version):
    """Show information about the CLI."""
    from cli import __version__
    if version:
        click.echo(f"Version: {__version__}")
    else:
        click.echo("Colab-GitHub Bridge CLI")
        click.echo(f"Version: {__version__}")


if __name__ == "__main__":
    cli()
