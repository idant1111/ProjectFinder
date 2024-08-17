import os
import platform
import shutil
import subprocess
from send2trash import send2trash

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from .scanner import scan_directories, load_index, save_index, clear_index
from .tui import display_projects

ASCII_ART = """
 _____                                                                     _____ 
( ___ )                                                                   ( ___ )
 |   |~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|   | 
 |   | ooooooooo.                          o8o                         .   |   | 
 |   | `888   `Y88.                        `"'                       .o8   |   | 
 |   |  888   .d88' oooo d8b  .ooooo.     oooo  .ooooo.   .ooooo.  .o888oo |   | 
 |   |  888ooo88P'  `888""8P d88' `88b    `888 d88' `88b d88' `"Y8   888   |   | 
 |   |  888          888     888   888     888 888ooo888 888         888   |   | 
 |   |  888          888     888   888     888 888    .o 888   .o8   888 . |   | 
 |   | o888o        d888b    `Y8bod8P'     888 `Y8bod8P' `Y8bod8P'   "888" |   | 
 |   |                                     888                             |   | 
 |   |                                 .o. 88P                             |   | 
 |   | oooooooooooo  o8o               `Y888.o8                            |   | 
 |   | `888'     `8  `"'                   "888                            |   | 
 |   |  888         oooo  ooo. .oo.    .oooo888   .ooooo.  oooo d8b        |   | 
 |   |  888oooo8    `888  `888P"Y88b  d88' `888  d88' `88b `888""8P        |   | 
 |   |  888    "     888   888   888  888   888  888ooo888  888            |   | 
 |   |  888          888   888   888  888   888  888    .o  888            |   | 
 |   | o888o        o888o o888o o888o `Y8bod88P" `Y8bod8P' d888b           |   | 
 |___|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|___| 
(_____)                                                                   (_____)
"""

@click.group()
def cli():
    """Main command group for the ProjectFinder CLI."""
    console = Console()
    console.print(Panel(Text(ASCII_ART, justify="center", style="bold cyan")))
    console.print("Welcome to ProjectFinder!\n", style="bold green")

@cli.command()
@click.option('--system-wide', is_flag=True, help="Scan the entire system starting from the home directory.")
@click.argument('directory', required=False, type=click.Path(exists=True))
def scan(system_wide, directory):
    """
    Scan for project directories either from the root directory or from a specified directory.
    """
    console = Console()

    # Determine base directory for scanning
    if system_wide:
        base_directory = os.path.expanduser("~")  # Start scanning from the home directory
    elif directory:
        base_directory = directory  # Scan from the user-specified directory
    else:
        console.print("[bold red]Error:[/bold red] You must specify either --system-wide for a full scan or provide a directory to scan.")
        return

    # Scan directories and index projects
    projects = scan_directories(base_directory)

    if not projects:
        console.print(f"[bold red]No projects found in {base_directory}.[/bold red]")
        return

    display_index(console, projects)

@cli.command()
def clear():
    """
    Clear the stored project index.
    """
    clear_index()
    console = Console()
    console.print("Project index has been cleared.", style="bold green")

@cli.command()
@click.option('--search', '-s', help="Search the index by directory name, project type, or path.")
@click.option('--sort-by', '-b', type=click.Choice(['name', 'type', 'path'], case_sensitive=False), help="Sort the index by directory name, project type, or path.")
def show_index(search, sort_by):
    """
    Display the current project index in a table, with options to search and sort.
    """
    console = Console()
    projects = load_index()

    if not projects:
        console.print("[bold red]No projects are currently indexed.[/bold red]")
        return

    # Apply search filter if specified
    if search:
        search_lower = search.lower()
        projects = [project for project in projects if search_lower in project["directory_name"].lower() or search_lower in project["project_type"].lower() or search_lower in project["path"].lower()]

    # Apply sorting if specified
    if sort_by:
        projects = sorted(projects, key=lambda x: x[sort_by].lower())

    display_index(console, projects)

def display_index(console, projects):
    """
    Display the indexed projects in a table.
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=6)
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Project Type", style="green", no_wrap=True)
    table.add_column("Path", style="magenta")

    for idx, project in enumerate(projects):
        table.add_row(str(idx), project["directory_name"], project["project_type"], project["path"])

    console.print(table)

    if projects:
        selected_id = Prompt.ask("[bold green]Select the project ID to manage[/bold green]", choices=[str(i) for i in range(len(projects))])
        selected_project = projects[int(selected_id)]
        
        action = Prompt.ask(
            f"[bold green]Selected project:[/bold green] {selected_project['directory_name']} [bold green]({selected_project['path']})[/bold green]\n[bold yellow]Choose an action[/bold yellow]",
            choices=["open", "pwd", "remove"]
        )

        if action == "open":
            open_folder(selected_project["path"])
        elif action == "pwd":
            console.print(f"[bold green]Path:[/bold green] {selected_project['path']}")
        elif action == "remove":
            confirm = Prompt.ask("[bold red]Are you sure you want to move this directory to the recycle bin? (yes/no)[/bold red]", choices=["yes", "no"])
            if confirm == "yes":
                move_to_recycle_bin(selected_project["path"], console)
            else:
                console.print("[bold green]Operation cancelled.[/bold green]")

def open_folder(path):
    """
    Open the selected folder in the system's file explorer.
    """
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])

def move_to_recycle_bin(path, console):
    """
    Move the selected folder to the recycle bin.
    """
    try:
        send2trash(path)
        console.print(f"[bold red]Moved to recycle bin:[/bold red] {path}")
    except Exception as e:
        console.print(f"[bold red]Error moving to recycle bin:[/bold red] {e}")

if __name__ == "__main__":
    cli()
