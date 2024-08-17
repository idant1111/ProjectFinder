import os
import json
from tqdm import tqdm

INDEX_FILE = "project_index.json"

# Directories and files to ignore
IGNORED_DIRS = {
    'node_modules', 'vendor', '.venv', 'env', '__pycache__',
    'dist', 'build', 'Library', 'System', 'bin', 'usr', 'Applications',
    '.git', '.idea', '.vscode', 'venv', 'env', '.env', 'anaconda3',
    '.npm', '.nvm', '.cache', '.local', '.conda', 'AppData', 'Program Files',
    'Visual Studio Code.app'
}


TRUNCATE_AT_DIRS = {'lib'}

# Project indicators
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
}

def get_project_type(path):
    """Determine the project type based on known project files."""
    for indicator, project_type in PROJECT_INDICATORS.items():
        if os.path.exists(os.path.join(path, indicator)):
            return project_type
    return 'Unknown'

def should_truncate_path(path):
    """Check if the path should be truncated based on predefined directories."""
    for dir_name in TRUNCATE_AT_DIRS:
        if dir_name in path.split(os.sep):
            return True
    return False

def save_index(projects):
    """Save the project index to a JSON file."""
    with open(INDEX_FILE, 'w') as f:
        json.dump(projects, f, indent=4)

def load_index():
    """Load the project index from a JSON file."""
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as f:
            return json.load(f)
    return []

def clear_index():
    """Clear the project index file."""
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

def is_duplicate(project, existing_projects):
    """Check if the project is already in the index."""
    for existing_project in existing_projects:
        if project["path"] == existing_project["path"]:
            return True
    return False

def scan_directories(base_directory):
    """Recursively scan the base directory to find top-level project directories with a progress bar."""
    projects = load_index()  # Load existing index
    unique_projects = set()

    total_dirs = sum([len(dirs) for _, dirs, _ in os.walk(base_directory)]) + 1  # Counting total directories for the progress bar

    with tqdm(total=total_dirs, desc="Scanning directories", unit="dir") as pbar:
        for root, dirs, files in os.walk(base_directory):
            pbar.set_postfix(current_directory=root)

            # Skip ignored dirs
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            # Truncate paths
            if should_truncate_path(root):
                continue

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
    
    save_index(projects) 
    return projects
