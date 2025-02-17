import subprocess
import os
from datetime import datetime

def run_command(command):
    """Execute a shell command and return the output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error message: {e.stderr}")
        return None

def create_backup(file_path):
    """Create a backup of the existing file if it exists."""
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"
        os.rename(file_path, backup_path)
        print(f"Created backup: {backup_path}")

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def main():
    # Define directory and file paths
    dependencies_dir = "core_dependencies"
    ensure_directory_exists(dependencies_dir)

    environment_file = os.path.join(dependencies_dir, "environment.yml")
    requirements_file = os.path.join(dependencies_dir, "requirements.txt")

    # Create backups of existing files
    create_backup(environment_file)
    create_backup(requirements_file)

    # Export conda environment
    print("Exporting conda environment...")
    conda_output = run_command(f"conda env export > {environment_file}")
    if conda_output is not None:
        print(f"Successfully created {environment_file}")

    # Export pip requirements
    print("Exporting pip requirements...")
    pip_output = run_command(f"pip freeze > {requirements_file}")
    if pip_output is not None:
        print(f"Successfully created {requirements_file}")

if __name__ == "__main__":
    main()