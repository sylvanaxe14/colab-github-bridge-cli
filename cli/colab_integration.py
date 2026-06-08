"""Helpers and utilities for use within Colab notebooks."""

import os
from pathlib import Path
from git import Repo
import requests


def setup_colab_environment():
    """Initialize Colab environment for GitHub integration."""
    config_dir = Path.home() / ".colab-github-bridge"
    config_dir.mkdir(exist_ok=True)
    
    # Configure git if not already done
    try:
        os.system("git config --global user.name 'Colab User'")
        os.system("git config --global user.email 'colab@notebook.local'")
    except Exception as e:
        print(f"Warning: Could not configure git: {e}")
    
    print("✓ Colab environment initialized")


def clone_repo(repo_url, target_path=None):
    """Clone a GitHub repository in Colab."""
    if target_path is None:
        target_path = repo_url.split("/")[-1].replace(".git", "")
    
    print(f"Cloning {repo_url}...")
    repo = Repo.clone_from(repo_url, target_path)
    print(f"✓ Cloned to {target_path}")
    return repo


def commit_changes(repo_path, message):
    """Commit changes in Colab."""
    repo = Repo(repo_path)
    repo.index.add(A=True)
    repo.index.commit(message)
    print(f"✓ Committed: {message}")


def push_changes(repo_path, remote="origin", branch=None):
    """Push changes to GitHub from Colab."""
    repo = Repo(repo_path)
    if branch is None:
        branch = repo.active_branch.name
    
    remote_obj = repo.remotes[remote]
    remote_obj.push(branch)
    print(f"✓ Pushed to {remote}/{branch}")


def get_current_branch(repo_path="."):
    """Get the current git branch."""
    repo = Repo(repo_path)
    return repo.active_branch.name


def get_repo_status(repo_path="."):
    """Get repository status information."""
    repo = Repo(repo_path)
    return {
        "branch": repo.active_branch.name,
        "untracked": len(repo.untracked_files),
        "modified": len(repo.index.diff(None)),
        "remote": "origin" if "origin" in [r.name for r in repo.remotes] else None,
    }


def install_dependencies():
    """Install dependencies in Colab environment."""
    print("Installing dependencies...")
    os.system("pip install gitpython requests pyyaml click")
    print("✓ Dependencies installed")
