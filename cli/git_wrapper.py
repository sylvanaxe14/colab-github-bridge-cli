"""Safe git operations wrapper for clone, push, and pull."""

import os
import click
from git import Repo
from pathlib import Path


@click.group()
def git_group():
    """Git operations: clone, push, pull."""
    pass


@git_group.command()
@click.argument("url")
@click.option("--path", "-p", type=str, default=None, help="Local path for cloned repo")
def clone(url, path):
    """Clone a GitHub repository safely."""
    try:
        if path is None:
            path = url.split("/")[-1].replace(".git", "")
        
        click.echo(f"Cloning {url} into {path}...")
        repo = Repo.clone_from(url, path)
        click.echo(f"✓ Successfully cloned to {path}")
        return repo
    except Exception as e:
        click.echo(f"✗ Clone failed: {str(e)}", err=True)
        raise


@git_group.command()
@click.option("--path", "-p", type=str, default=".", help="Repository path")
def pull(path):
    """Pull latest changes from remote repository."""
    try:
        repo = Repo(path)
        origin = repo.remotes.origin
        origin.pull()
        click.echo(f"✓ Successfully pulled latest changes from {path}")
    except Exception as e:
        click.echo(f"✗ Pull failed: {str(e)}", err=True)
        raise


@git_group.command()
@click.option("--path", "-p", type=str, default=".", help="Repository path")
@click.option("--message", "-m", type=str, required=True, help="Commit message")
def commit(path, message):
    """Commit changes to the repository."""
    try:
        repo = Repo(path)
        repo.index.add(A=True)
        repo.index.commit(message)
        click.echo(f"✓ Successfully committed with message: {message}")
    except Exception as e:
        click.echo(f"✗ Commit failed: {str(e)}", err=True)
        raise


@git_group.command()
@click.option("--path", "-p", type=str, default=".", help="Repository path")
@click.option("--remote", "-r", type=str, default="origin", help="Remote name")
@click.option("--branch", "-b", type=str, default=None, help="Branch name")
def push(path, remote, branch):
    """Push changes to remote repository."""
    try:
        repo = Repo(path)
        if branch is None:
            branch = repo.active_branch.name
        
        remote_obj = repo.remotes[remote]
        remote_obj.push(branch)
        click.echo(f"✓ Successfully pushed to {remote}/{branch}")
    except Exception as e:
        click.echo(f"✗ Push failed: {str(e)}", err=True)
        raise


@git_group.command()
@click.option("--path", "-p", type=str, default=".", help="Repository path")
def status(path):
    """Show git repository status."""
    try:
        repo = Repo(path)
        click.echo(f"Repository: {repo.working_dir}")
        click.echo(f"Branch: {repo.active_branch.name}")
        click.echo(f"Untracked files: {len(repo.untracked_files)}")
        click.echo(f"Modified files: {len(repo.index.diff(None))}")
    except Exception as e:
        click.echo(f"✗ Status check failed: {str(e)}", err=True)
        raise
