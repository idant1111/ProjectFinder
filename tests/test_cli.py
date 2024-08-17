import unittest
from unittest.mock import patch, MagicMock
import cli

class TestCLI(unittest.TestCase):

    @patch('cli.Console.print')
    def test_welcome_message(self, mock_print):
        with patch('cli.Panel') as mock_panel, patch('cli.Text') as mock_text:
            cli.cli()
            mock_panel.assert_called()
            mock_text.assert_called()
            mock_print.assert_any_call("Welcome to ProjectFinder!\n", style="bold green")

    @patch('cli.scan_directories')
    @patch('cli.display_index')
    @patch('cli.Console.print')
    def test_scan_system_wide(self, mock_print, mock_display_index, mock_scan_directories):
        mock_scan_directories.return_value = ["project1", "project2"]
        
        result = self.runner.invoke(cli.cli, ['scan', '--system-wide'])
        
        mock_scan_directories.assert_called_once()
        mock_display_index.assert_called_once_with(mock.ANY, ["project1", "project2"])
        self.assertIn("No projects found", result.output)

    @patch('cli.clear_index')
    @patch('cli.Console.print')
    def test_clear_index(self, mock_print, mock_clear_index):
        result = self.runner.invoke(cli.cli, ['clear'])
        mock_clear_index.assert_called_once()
        mock_print.assert_any_call("Project index has been cleared.", style="bold green")

    @patch('cli.load_index')
    @patch('cli.display_index')
    @patch('cli.Console.print')
    def test_show_index_no_projects(self, mock_print, mock_display_index, mock_load_index):
        mock_load_index.return_value = []
        result = self.runner.invoke(cli.cli, ['show-index'])
        mock_load_index.assert_called_once()
        mock_print.assert_any_call("[bold red]No projects are currently indexed.[/bold red]")

if __name__ == '__main__':
    unittest.main()
