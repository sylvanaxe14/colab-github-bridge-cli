"""Authentication helpers for PAT and SSH key management."""

import os
import getpass
import click
from pathlib import Path


@click.group()
def auth_group():
    """Authentication: setup, configure PAT, SSH keys."""
    pass


@auth_group.command()
def setup():
    """Interactive setup for GitHub authentication."""
    click.echo("=== GitHub Authentication Setup ===\n")
    
    auth_type = click.prompt(
        "Choose authentication method",
        type=click.Choice(["pat", "ssh"]),
        default="pat"
    )
    
    if auth_type == "pat":
        _setup_pat()
    else:
        _setup_ssh()


def _setup_pat():
    """Setup Personal Access Token authentication."""
    click.echo("\n--- GitHub Personal Access Token (PAT) ---")
    click.echo("1. Go to https://github.com/settings/tokens")
    click.echo("2. Create a new token with 'repo' and 'workflow' scopes")
    click.echo("3. Paste the token below (it will be stored securely)")
    
    token = getpass.getpass("\nEnter your GitHub PAT: ")
    
    config_dir = Path.home() / ".colab-github-bridge"
    config_dir.mkdir(exist_ok=True)
    
    token_file = config_dir / "github_token"
    with open(token_file, "w") as f:
        f.write(token)
    
    os.chmod(token_file, 0o600)
    
    click.echo(f"✓ Token saved to {token_file}")
    click.echo("✓ Authentication setup complete!")


def _setup_ssh():
    """Setup SSH key authentication."""
    click.echo("\n--- SSH Key Authentication ---")
    
    ssh_key_path = click.prompt(
        "SSH key path",
        type=click.Path(exists=True),
        default=str(Path.home() / ".ssh" / "id_rsa")
    )
    
    config_dir = Path.home() / ".colab-github-bridge"
    config_dir.mkdir(exist_ok=True)
    
    config_file = config_dir / "ssh_config"
    with open(config_file, "w") as f:
        f.write(f"ssh_key_path={ssh_key_path}\n")
    
    os.chmod(config_file, 0o600)
    
    click.echo(f"✓ SSH configuration saved to {config_file}")
    click.echo("✓ Authentication setup complete!")


@auth_group.command()
def verify():
    """Verify GitHub authentication is working."""
    try:
        import requests
        
        config_dir = Path.home() / ".colab-github-bridge"
        token_file = config_dir / "github_token"
        
        if not token_file.exists():
            click.echo("✗ No authentication token found. Run 'auth setup' first.", err=True)
            return
        
        with open(token_file, "r") as f:
            token = f.read().strip()
        
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            click.echo(f"✓ Authentication verified for user: {user['login']}")
        else:
            click.echo("✗ Authentication failed. Check your token.", err=True)
    
    except Exception as e:
        click.echo(f"✗ Verification error: {str(e)}", err=True)


@auth_group.command()
def clear():
    """Clear stored authentication credentials."""
    config_dir = Path.home() / ".colab-github-bridge"
    
    if config_dir.exists():
        import shutil
        shutil.rmtree(config_dir)
        click.echo("✓ Authentication credentials cleared")
    else:
        click.echo("No stored credentials found")
