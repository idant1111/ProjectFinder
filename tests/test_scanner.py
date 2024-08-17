import unittest
from unittest.mock import patch, mock_open, MagicMock
import os
import scanner

class TestScanner(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='[{"path":"/test/path"}]')
    def test_load_index(self, mock_open, mock_exists):
        result = scanner.load_index()
        mock_open.assert_called_once_with(scanner.INDEX_FILE, 'r', encoding='utf-8')
        self.assertEqual(result, [{"path":"/test/path"}])

    @patch('os.path.exists', return_value=True)
    @patch('os.remove')
    def test_clear_index(self, mock_remove, mock_exists):
        scanner.clear_index()
        mock_exists.assert_called_once_with(scanner.INDEX_FILE)
        mock_remove.assert_called_once_with(scanner.INDEX_FILE)

    @patch('scanner.save_index')
    @patch('scanner.get_project_type', return_value='Python')
    @patch('os.walk')
    def test_scan_directories(self, mock_walk, mock_get_project_type, mock_save_index):
        mock_walk.return_value = [('/test/root', ['dir1'], ['setup.py'])]
        projects = scanner.scan_directories('/test')
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]["project_type"], 'Python')
        mock_save_index.assert_called_once()

    def test_is_duplicate(self):
        project = {"path": "/test/path"}
        existing_projects = [{"path": "/test/path"}]
        result = scanner.is_duplicate(project, existing_projects)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
