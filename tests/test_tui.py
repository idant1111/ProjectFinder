import unittest
from unittest.mock import patch
import tui

class TestTUI(unittest.TestCase):

    @patch('tui.Console.print')
    @patch('tui.Console.input', return_value='0')
    def test_display_projects(self, mock_input, mock_print):
        projects = [
            {"directory_name": "test_dir", "project_type": "Python", "path": "/test/path"}
        ]
        selected_index = tui.display_projects(projects)
        mock_print.assert_called()
        mock_input.assert_called_once_with("[bold green]Select a project by index: [/bold green]")
        self.assertEqual(selected_index, 0)

    @patch('tui.Console.input', return_value='invalid')
    @patch('tui.Console.print')
    def test_display_projects_invalid_input(self, mock_print, mock_input):
        projects = [
            {"directory_name": "test_dir", "project_type": "Python", "path": "/test/path"}
        ]
        with patch('tui.Console.input', side_effect=['invalid', '0']):
            selected_index = tui.display_projects(projects)
            self.assertEqual(selected_index, 0)
            self.assertIn("[bold red]Invalid input. Please enter a valid number.[/bold red]", mock_print.call_args_list[-1][0][0])

if __name__ == '__main__':
    unittest.main()
