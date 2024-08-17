from rich.table import Table
from rich.console import Console

def display_projects(projects):
    """
    Display the list of projects in a TUI with their type and path.
    
    Args:
        projects (list): List of project dictionaries containing 
        'directory_name', 'project_type', and 'path'.
    
    Returns:
        int: The index of the selected project.
    """
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Directory Name", style="cyan", no_wrap=True)
    table.add_column("Project Type", style="green", no_wrap=True)
    table.add_column("Path", style="magenta")

    for project in projects:
        table.add_row(project["directory_name"], project["project_type"], project["path"])

    console.print(table)

    while True:
        try:
            selected_index = int(console.input("[bold green]Select a project by index: [/bold green]"))
            if 0 <= selected_index < len(projects):
                return selected_index
            console.print(f"""[bold red]Invalid index.
                          Please enter a number between 0 and {len(projects) - 1}.[/bold red]
                          """
                          )
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")
