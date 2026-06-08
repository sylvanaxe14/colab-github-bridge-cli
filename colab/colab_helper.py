"""High-level helper functions for common Colab tasks."""

import os
from pathlib import Path
from git import Repo
import requests


class ColabGitHelper:
    \"\"\"Helper class for Git operations in Colab.\"\"\"
    
    def __init__(self, repo_path=\".\"):
        self.repo_path = repo_path
        self.repo = Repo(repo_path)
    
    def clone(self, url, target_path=None):
        \"\"\"Clone a repository.\"\"\"
        if target_path is None:
            target_path = url.split(\"/\")[-1].replace(\".git\", \"\")
        
        print(f\"Cloning {url}...\")
        self.repo = Repo.clone_from(url, target_path)
        self.repo_path = target_path
        print(f\"✓ Cloned to {target_path}\")
        return self.repo
    
    def commit(self, message):
        \"\"\"Commit all changes.\"\"\"
        self.repo.index.add(A=True)
        self.repo.index.commit(message)
        print(f\"✓ Committed: {message}\")
    
    def push(self, remote=\"origin\", branch=None):
        \"\"\"Push to remote repository.\"\"\"
        if branch is None:
            branch = self.repo.active_branch.name
        
        self.repo.remotes[remote].push(branch)
        print(f\"✓ Pushed to {remote}/{branch}\")
    
    def pull(self, remote=\"origin\", branch=None):
        \"\"\"Pull from remote repository.\"\"\"
        if branch is None:
            branch = self.repo.active_branch.name
        
        self.repo.remotes[remote].pull(branch)\n        print(f\"✓ Pulled from {remote}/{branch}\")
    
    def status(self):
        \"\"\"Get repository status.\"\"\"
        return {
            \"branch\": self.repo.active_branch.name,
            \"untracked\": len(self.repo.untracked_files),
            \"modified\": len(list(self.repo.index.diff(None))),
        }
    
    def create_branch(self, branch_name):
        \"\"\"Create and checkout a new branch.\"\"\"
        new_branch = self.repo.create_head(branch_name)
        new_branch.checkout()
        print(f\"✓ Created and checked out branch: {branch_name}\")
    
    def switch_branch(self, branch_name):
        \"\"\"Switch to an existing branch.\"\"\"
        self.repo.heads[branch_name].checkout()
        print(f\"✓ Switched to branch: {branch_name}\")


class GitHubAPIHelper:
    \"\"\"Helper for GitHub API operations.\"\"\"
    
    def __init__(self, token=None):
        self.token = token or self._load_token()
        self.base_url = \"https://api.github.com\"
        self.headers = {
            \"Authorization\": f\"token {self.token}\",
            \"Accept\": \"application/vnd.github.v3+json\"
        }
    
    def _load_token(self):
        \"\"\"Load token from config file.\"\"\"
        config_dir = Path.home() / \".colab-github-bridge\"
        token_file = config_dir / \"github_token\"
        
        if token_file.exists():
            return token_file.read_text().strip()
        else:
            raise ValueError(\"GitHub token not found. Run auth setup first.\")
    
    def get_user(self):
        \"\"\"Get authenticated user info.\"\"\"
        response = requests.get(f\"{self.base_url}/user\", headers=self.headers)
        return response.json()
    
    def get_repos(self):
        \"\"\"Get user's repositories.\"\"\"
        response = requests.get(f\"{self.base_url}/user/repos\", headers=self.headers)
        return response.json()
    
    def create_pr(self, owner, repo, title, body, head, base=\"main\"):\n        \"\"\"Create a pull request.\"\"\"
        url = f\"{self.base_url}/repos/{owner}/{repo}/pulls\"
        data = {
            \"title\": title,
            \"body\": body,
            \"head\": head,
            \"base\": base,
        }
        response = requests.post(url, json=data, headers=self.headers)
        return response.json()


# Convenience functions
git_helper = None

def init(repo_path=\".\"):
    \"\"\"Initialize Git helper.\"\"\"
    global git_helper
    git_helper = ColabGitHelper(repo_path)
    return git_helper


def clone(url, target_path=None):
    \"\"\"Clone a repository.\"\"\"
    helper = ColabGitHelper()
    return helper.clone(url, target_path)


def commit(message):
    \"\"\"Commit changes.\"\"\"
    if git_helper is None:
        raise RuntimeError(\"Git helper not initialized. Call init() first.\")
    git_helper.commit(message)


def push(remote=\"origin\", branch=None):
    \"\"\"Push changes.\"\"\"
    if git_helper is None:
        raise RuntimeError(\"Git helper not initialized. Call init() first.\")
    git_helper.push(remote, branch)


def pull(remote=\"origin\", branch=None):
    \"\"\"Pull changes.\"\"\"
    if git_helper is None:
        raise RuntimeError(\"Git helper not initialized. Call init() first.\")
    git_helper.pull(remote, branch)


def status():
    \"\"\"Get repository status.\"\"\"
    if git_helper is None:
        raise RuntimeError(\"Git helper not initialized. Call init() first.\")
    return git_helper.status()
