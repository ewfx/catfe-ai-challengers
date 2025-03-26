import os
import subprocess
import sys
from pathlib import Path

def create_env_file():
    """Create a .env file from .env.example if it doesn't exist."""
    root_dir = Path(__file__).parent.parent
    env_example = root_dir / ".env.example"
    env_file = root_dir / ".env"
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        with open(env_example, "r") as example:
            with open(env_file, "w") as env:
                env.write(example.read())
        print("Created .env file. Please update it with your actual values.")
    elif not env_example.exists():
        print("Warning: .env.example file not found.")
    else:
        print(".env file already exists.")

def install_dependencies():
    """Install dependencies from requirements.txt."""
    root_dir = Path(__file__).parent.parent
    req_file = root_dir / "requirements.txt"
    
    if req_file.exists():
        print("Installing dependencies from requirements.txt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
        print("Dependencies installed successfully.")
    else:
        print("Warning: requirements.txt file not found.")

def create_directories():
    """Create necessary directories if they don't exist."""
    root_dir = Path(__file__).parent.parent
    dirs = [
        root_dir / "repo",
        root_dir / "logs"
    ]
    
    for directory in dirs:
        if not directory.exists():
            print(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)

def main():
    """Main setup function."""
    print("Setting up environment for GenAI Testing System...")
    create_env_file()
    install_dependencies()
    create_directories()
    print("Environment setup complete!")

if __name__ == "__main__":
    main()
