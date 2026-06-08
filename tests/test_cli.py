"""Tests for the CLI module."""

import pytest
from click.testing import CliRunner
from cli.main import cli
from cli.auth import auth_group
from cli.git_wrapper import git_group


class TestMainCLI:
    \"\"\"Test main CLI commands.\"\"\"
    
    def test_cli_info(self):
        \"\"\"Test info command.\"\"\"
        runner = CliRunner()
        result = runner.invoke(cli, ["info"])
        assert result.exit_code == 0
        assert "Colab-GitHub Bridge CLI" in result.output
    
    def test_cli_info_version(self):
        \"\"\"Test info command with version flag.\"\"\"
        runner = CliRunner()
        result = runner.invoke(cli, ["info", "--version"])
        assert result.exit_code == 0
        assert "Version:" in result.output
    
    def test_cli_status(self):
        \"\"\"Test status command.\"\"\"
        runner = CliRunner()
        result = runner.invoke(cli, ["status"])
        assert result.exit_code == 0
        assert "Status: OK" in result.output


class TestAuthCommands:
    \"\"\"Test authentication commands.\"\"\"
    
    def test_auth_verify_no_token(self):
        \"\"\"Test verify command without token configured.\"\"\"
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(auth_group, ["verify"])
            # Expected to fail or show warning
            assert result.exit_code != 0 or "not found" in result.output.lower()


class TestGitCommands:
    \"\"\"Test git wrapper commands.\"\"\"
    
    def test_git_status(self):
        \"\"\"Test git status command.\"\"\"
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Initialize a git repo first
            import subprocess
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "config", "user.name", "Test"], check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
            
            result = runner.invoke(git_group, ["status"])
            assert result.exit_code == 0


class TestIntegration:
    \"\"\"Integration tests.\"\"\"
    
    def test_cli_help(self):
        \"\"\"Test that help works.\"\"\"
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
    
    def test_auth_help(self):
        \"\"\"Test auth subcommand help.\"\"\"
        runner = CliRunner()
        result = runner.invoke(auth_group, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output
    
    def test_git_help(self):
        \"\"\"Test git subcommand help.\"\"\"
        runner = CliRunner()
        result = runner.invoke(git_group, ["--help"])
        assert result.exit_code == 0
        assert "Usage:" in result.output


if __name__ == \"__main__\":
    pytest.main([__file__, \"-v\"])
