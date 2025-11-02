import os
import re
import shutil
import stat
import time
from pathlib import Path

from git import Repo

# Template repository URLs
TEMPLATES = {
    "default": "https://github.com/NSCodeDev/rs_Template.git",
}


def create_project(project_name, target_folder, template="default"):
    """
    Main function to generate Django project
    """

    # Validate project name
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", project_name):
        raise ValueError(
            "Invalid project name. Use letters, numbers, underscores only."
        )

    template_url = TEMPLATES.get(template)
    if not template_url:
        raise ValueError(f"Template '{template}' not found")

    #  Clone template
    temp_dir = Path(f".temp_{project_name}")
    print(f"📦 Cloning template from {template_url}...")
    Repo.clone_from(template_url, temp_dir)

    # Remove .git folder with proper permissions handling
    git_dir = temp_dir / ".git"
    if git_dir.exists():
        remove_readonly(git_dir)
        time.sleep(0.5)  # Wait for file handles to release

    #  Rename and replace placeholders
    print(f"🔧 Configuring project...")
    replace_placeholders(temp_dir, project_name)

    # Move to target folder
    target_path = Path(target_folder)
    if target_path.exists():
        raise FileExistsError(f"Folder '{target_folder}' already exists")

    try:
        # Retry move operation (Windows file locking issues)
        for attempt in range(3):
            try:
                shutil.move(str(temp_dir), str(target_path))
                break
            except PermissionError:
                if attempt < 2:
                    time.sleep(1)
                else:
                    raise
        print(f"✅ Done!")
    except Exception as e:
        # Clean up temp directory if move fails
        if temp_dir.exists():
            remove_readonly(temp_dir)
        raise e
    finally:
        # Clean up any remaining temp directory
        if temp_dir.exists():
            remove_readonly(temp_dir)


def remove_readonly(path):
    """Remove a directory tree, handling read-only files on Windows"""

    def handle_remove_readonly(func, path, exc):
        """Error handler for Windows read-only files"""
        os.chmod(path, stat.S_IWRITE)
        func(path)

    shutil.rmtree(path, onerror=handle_remove_readonly)


def replace_placeholders(project_path, project_name):
    """
    Replace template placeholders with actual project name
    """

    # replace projectname inside files
    placeholder = "{{project_name}}"

    for root, dirs, files in os.walk(project_path):
        # Skip venv, __pycache__ etc
        dirs[:] = [
            d for d in dirs if d not in [".git", "venv", "__pycache__", "node_modules"]
        ]

        for filename in files:
            filepath = Path(root) / filename

            # Skip binary files
            if filepath.suffix in [".pyc", ".png", ".jpg", ".pdf"]:
                continue

            try:
                # Read and replace content
                content = filepath.read_text(encoding="utf-8")
                if placeholder in content:
                    new_content = content.replace(placeholder, project_name)
                    filepath.write_text(new_content, encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue  # Skip files that can't be read

    # Rename folders if needed
    rename_directories(project_path, placeholder, project_name)


def rename_directories(base_path, old_name, new_name):
    """
    Rename directories that match placeholder
    """
    for root, dirs, files in os.walk(base_path, topdown=False):
        for dir_name in dirs:
            if old_name in dir_name:
                old_path = Path(root) / dir_name
                new_dir_name = dir_name.replace(old_name, new_name)
                new_path = Path(root) / new_dir_name
                old_path.rename(new_path)
