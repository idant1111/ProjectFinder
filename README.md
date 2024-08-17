


# ProjectFinder
a TUI tool for finding the code project lost in your system

**ProjectFinder** is a command-line tool designed to scan your system for project directories, index them, and provide various management options. The tool supports searching, sorting, and managing projects, including opening directories, retrieving paths, and moving directories to the recycle bin.

![image](https://github.com/user-attachments/assets/7287b0d8-49b4-4d2d-8dd2-94b634144b08)

![image](https://github.com/user-attachments/assets/971be65a-7cac-4fc4-8659-5bc4ddd19bf0)

## Features

- **System-Wide Scanning:** Scan your entire system or specific directories for project folders.
- **Search and Sort:** Easily search and sort your indexed projects by name, type, or path.
- **Manage Projects:** Open project folders, print their paths, or move them to the recycle bin—all from the CLI.

## Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/idant1111/ProjectFinder.git
cd ProjectFinder
```

Install Dependencies
Install the required Python packages using pip:

```
pip install -r requirements.txt
```
Note: The tool uses send2trash for safely moving directories to the recycle bin. This package will be installed with the dependencies.

Install tool:
```
from inside the dir where setup.py is:

python3 -m pip install -e . 

```
## Usage
### Scan for Projects
You can scan your system or a specific directory for projects:

- System-Wide Scan:
```
projectfinder scan --system-wide

```
- Scan a Specific Directory:
```
projectfinder scan /path/to/directory
```

- View Indexed Projects
-- Once you have scanned for projects, you can view the indexed projects:


- Show All Indexed Projects:

```
projectfinder show_index
```
Search Indexed Projects:
```
projectfinder show_index --search "keyword"
```

Sort Indexed Projects:

```
projectfinder show_index --sort-by name
```

### Manage Projects
- After viewing the indexed projects, you can select a project to manage:

Open Folder in File Explorer:

- After selecting a project ID, choose open to open the directory in your system's file explorer.

Print Working Directory (pwd):

- After selecting a project ID, choose pwd to print the absolute path of the project.

Move Directory to Recycle Bin:

After selecting a project ID, choose remove to move the directory to the recycle bin. You will be prompted for confirmation.

Clear the Project Index
You can clear the entire project index if needed:

```
projectfinder clear
```
## Dependencies
```
Rich: For formatting the CLI output.
TQDM: For showing progress bars during scanning.
Send2Trash: For safely moving files and directories to the recycle bin.
Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss your ideas.
```
## License
This project is licensed under the MIT License.
