"""Bootstrap script - runnable version of the Colab notebook cell."""

import os
import sys
import subprocess
from pathlib import Path


def install_dependencies():
    """Install required Python packages."""
    packages = ["gitpython", "requests", "pyyaml", "click"]
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + packages)
    print("✓ Dependencies installed")


def clone_bridge_cli():
    """Clone the bridge CLI repository."""
    print("Cloning colab-github-bridge-cli...")
    cli_path = Path("/tmp/bridge-cli")
    
    if cli_path.exists():
        print(f"✓ Already cloned to {cli_path}")
        return cli_path
    
    subprocess.check_call([
        "git", "clone",
        "https://github.com/sylvanaxe14/colab-github-bridge-cli.git",
        str(cli_path)
    ])
    print(f"✓ Cloned to {cli_path}")
    return cli_path


def setup_path(cli_path):
    """Add bridge CLI to Python path."""
    if str(cli_path) not in sys.path:
        sys.path.insert(0, str(cli_path))
    print(f"✓ Added {cli_path} to Python path")


def bootstrap():
    """Run complete bootstrap process."""
    print("=== Colab-GitHub Bridge Bootstrap ===\n")
    
    try:
        install_dependencies()
        cli_path = clone_bridge_cli()
        setup_path(cli_path)
        
        print("\n✓ Bootstrap complete!")
        print("\nYou can now import and use:")
        print("  from colab.colab_helper import *")
        print("  from cli.colab_integration import *")
        
        return True
    
    except Exception as e:
        print(f"✗ Bootstrap failed: {e}", file=sys.stderr)
        return False


if __name__ == "__main__":
    success = bootstrap()
    sys.exit(0 if success else 1)
