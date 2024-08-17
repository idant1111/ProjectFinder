"""
Scanner.py

"""
import os
import json
from tqdm import tqdm

INDEX_FILE = "project_index.json"

# Directories and files to ignore
IGNORED_DIRS = {
    'node_modules', 'vendor', '.venv', 'env', '__pycache__',
    'dist', 'build', 'Library', 'System', 'bin', 'usr', 'Applications',
    '.git', '.idea', '.vscode', 'anaconda3', '.npm', '.nvm', '.cache',
    '.local', '.conda', 'AppData', 'Program Files', 'Visual Studio Code.app'
}

# Directories where paths should be truncated
TRUNCATE_AT_DIRS = {'lib'}

# Project indicators and their corresponding types
PROJECT_INDICATORS = {
    'package.json': 'Node.js',
    'pyproject.toml': 'Python',
    'setup.py': 'Python',
    'Cargo.toml': 'Rust',
    'go.mod': 'Go',
    'pom.xml': 'Java (Maven)',
    'build.gradle': 'Java (Gradle)',
    'CMakeLists.txt': 'CMake',
    'composer.json': 'PHP',
    'Gemfile': 'Ruby',
    'mix.exs': 'Elixir',
    '.git': 'Git Repository',
    'Makefile': 'C/C++',
    'main.c': 'C',
    'main.cpp': 'C++',
    'build.xml': 'Ant',
    'build.sbt': 'Scala (SBT)',
    'pubspec.yaml': 'Dart (Flutter)',
    'Project.swift': 'Swift',
    'Package.swift': 'Swift',
    'Main.swift': 'Swift',
    'init.lua': 'Lua',
    'main.lua': 'Lua',
    'rockspec': 'Lua (Luarocks)',
}

def get_project_type(path):
    """Determine the project type based on known project files."""
    for indicator, project_type in PROJECT_INDICATORS.items():
        if os.path.exists(os.path.join(path, indicator)):
            return project_type
    return 'Unknown'

def should_truncate_path(path):
    """Check if the path should be truncated based on predefined directories."""
    return any(dir_name in path.split(os.sep) for dir_name in TRUNCATE_AT_DIRS)

def save_index(projects):
    """Save the project index to a JSON file."""
    with open(INDEX_FILE, 'w', encoding='utf-8') as file:
        json.dump(projects, file, indent=4)

def load_index():
    """Load the project index from a JSON file."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def clear_index():
    """Clear the project index file."""
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

def is_duplicate(project, existing_projects):
    """Check if the project is already in the index."""
    return any(
        project["path"] == existing_project["path"] for existing_project in existing_projects
        )

def scan_directories(base_directory):
    """
    Recursively scan the base directory to find
    top-level project directories with a progress bar.
     """
    projects = load_index()  # Load existing index
    unique_projects = set()
    # Counting total directories for the progress bar
    total_dirs = sum(len(dirs) for _, dirs, _ in os.walk(base_directory)) + 1  
    with tqdm(total=total_dirs, desc="Scanning directories", unit="dir") as pbar:
        for root, dirs, _ in os.walk(base_directory):
            pbar.set_postfix(current_directory=root)
            # Skip ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
            # Truncate paths at specified directories
            if should_truncate_path(root):
                continue
            # Check current directory for project indicators
            project_type = get_project_type(root)
            # If current directory is a project directory, add it to the list
            if project_type != 'Unknown':
                project_path = os.path.abspath(root)
                new_project = {
                    "directory_name": os.path.basename(project_path),
                    "project_type": project_type,
                    "path": project_path
                }
                # Check for duplicates before adding to the list
                if not is_duplicate(new_project, projects):
                    unique_projects.add(project_path)
                    projects.append(new_project)
            pbar.update(1)
    save_index(projects)  # Save updated index
    return projects
