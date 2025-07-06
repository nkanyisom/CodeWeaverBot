"""
Unit Tests for CodeWeaverBot
============================

Comprehensive test suite for CodeWeaverBot functionality including:
- Configuration validation
- File tracking and security
- VS Code integration
- Content generation
- Error handling

Author: nkmalunga
Version: 2.0
Date: July 6, 2025
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the project directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

import config
from app import (
    FileTracker,
    validate_vscode_executable,
    ensure_generated_files_dir,
    write_function_improved,
)


class TestConfig(unittest.TestCase):
    """Test cases for the config module."""

    def test_version_info(self):
        """Test that version information is properly defined."""
        self.assertEqual(config.VERSION, "2.0")
        self.assertEqual(config.APP_NAME, "CodeWeaverBot")
        self.assertEqual(config.AUTHOR, "nkmalunga")

    def test_security_constants(self):
        """Test security-related constants."""
        self.assertIsInstance(config.MAX_FILENAME_LENGTH, int)
        self.assertGreater(config.MAX_FILENAME_LENGTH, 0)
        self.assertEqual(config.MAX_PATH_LENGTH, 260)  # Windows limit
        self.assertIn(".py", config.ALLOWED_FILE_EXTENSIONS)
        self.assertIsInstance(config.SAFE_FILENAME_CHARS, set)

    def test_timing_constants(self):
        """Test timing configuration constants."""
        self.assertIsInstance(config.DEFAULT_PAUSE_TIME, (int, float))
        self.assertGreater(config.DEFAULT_PAUSE_TIME, 0)
        self.assertIsInstance(config.VSCODE_LAUNCH_TIMEOUT, (int, float))
        self.assertGreater(config.VSCODE_LAUNCH_TIMEOUT, 0)

    def test_runtime_configuration(self):
        """Test runtime configuration constants."""
        self.assertIsInstance(config.DEFAULT_RUNTIME_HOURS, (int, float))
        self.assertGreater(config.DEFAULT_RUNTIME_HOURS, 0)
        self.assertLessEqual(config.DEFAULT_RUNTIME_HOURS, config.MAX_RUNTIME_HOURS)
        self.assertGreater(config.MAX_RUNTIME_HOURS, 0)

    def test_path_configuration(self):
        """Test path-related configuration."""
        self.assertIsInstance(config.PROJECT_DIR, Path)
        self.assertTrue(config.PROJECT_DIR.exists())
        self.assertIsInstance(config.GENERATED_FILES_DIR, Path)
        self.assertIsInstance(config.LOG_FILE, Path)

    def test_content_limits(self):
        """Test content limitation constants."""
        self.assertGreater(config.MAX_CONTENT_LENGTH, 0)
        self.assertGreater(config.MAX_DESCRIPTION_LENGTH, 0)
        self.assertGreater(config.MAX_EXAMPLE_LENGTH, 0)

    def test_validate_config(self):
        """Test config validation function."""
        self.assertTrue(config.validate_config())

    def test_validate_config_with_invalid_values(self):
        """Test config validation with invalid values."""
        # Test with monkey patching invalid values
        original_runtime = config.DEFAULT_RUNTIME_HOURS
        original_max_runtime = config.MAX_RUNTIME_HOURS

        try:
            # Test invalid runtime hours
            config.DEFAULT_RUNTIME_HOURS = -1
            self.assertFalse(config.validate_config())

            config.DEFAULT_RUNTIME_HOURS = config.MAX_RUNTIME_HOURS + 1
            self.assertFalse(config.validate_config())

        finally:
            # Restore original values
            config.DEFAULT_RUNTIME_HOURS = original_runtime
            config.MAX_RUNTIME_HOURS = original_max_runtime

    def test_get_safe_runtime_hours(self):
        """Test safe runtime hours validation."""
        # Test normal case
        self.assertEqual(config.get_safe_runtime_hours(1.0), 1.0)

        # Test minimum enforcement
        self.assertEqual(config.get_safe_runtime_hours(0.05), 0.1)

        # Test maximum enforcement
        result = config.get_safe_runtime_hours(50)
        self.assertLessEqual(result, config.MAX_RUNTIME_HOURS)

    def test_is_safe_filename(self):
        """Test filename safety validation."""
        # Valid filenames
        self.assertTrue(config.is_safe_filename("test.py"))
        self.assertTrue(config.is_safe_filename("len_example_001.py"))
        self.assertTrue(config.is_safe_filename("function_test.py"))

        # Invalid filenames
        self.assertFalse(config.is_safe_filename("../test.py"))  # Path traversal
        self.assertFalse(config.is_safe_filename("test.txt"))  # Wrong extension
        self.assertFalse(config.is_safe_filename("test<>.py"))  # Invalid chars
        self.assertFalse(config.is_safe_filename("a" * 200))  # Too long

    def test_get_safe_content_length(self):
        """Test content length safety validation."""
        short_content = "print('hello')"
        self.assertEqual(config.get_safe_content_length(short_content), short_content)

        long_content = "x" * (config.MAX_CONTENT_LENGTH + 100)
        result = config.get_safe_content_length(long_content)
        self.assertLessEqual(
            len(result), config.MAX_CONTENT_LENGTH + 50
        )  # Account for truncation message
        self.assertIn("truncated", result)


class TestFileTracker(unittest.TestCase):
    """Test cases for the FileTracker class."""

    def setUp(self):
        """Set up test fixtures."""
        self.tracker = FileTracker()

    def test_initialization(self):
        """Test FileTracker initialization."""
        self.assertEqual(self.tracker._counter, 1)
        self.assertEqual(len(self.tracker._used_names), 0)

    def test_get_unique_filename_basic(self):
        """Test basic unique filename generation."""
        filename, path = self.tracker.get_unique_filename("len()")
        self.assertTrue(filename.endswith(".py"))
        self.assertIn("len", filename)
        self.assertIn("001", filename)
        self.assertIsInstance(path, Path)

    def test_get_unique_filename_increment(self):
        """Test that filenames increment properly."""
        filename1, _ = self.tracker.get_unique_filename("print()")
        filename2, _ = self.tracker.get_unique_filename("print()")

        self.assertNotEqual(filename1, filename2)
        self.assertIn("001", filename1)
        self.assertIn("002", filename2)

    def test_get_unique_filename_collision_prevention(self):
        """Test collision prevention in filename generation."""
        filenames = set()
        for i in range(10):
            filename, _ = self.tracker.get_unique_filename("test()")
            self.assertNotIn(filename, filenames)
            filenames.add(filename)

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test parentheses removal
        result = FileTracker._sanitize_filename("len()")
        self.assertEqual(result, "len")

        # Test space replacement
        result = FileTracker._sanitize_filename("string method")
        self.assertEqual(result, "string_method")

        # Test unsafe character removal
        result = FileTracker._sanitize_filename("test<>function")
        self.assertEqual(result, "testfunction")

    def test_sanitize_filename_empty_input(self):
        """Test sanitization with empty or invalid input."""
        result = FileTracker._sanitize_filename("")
        self.assertEqual(result, "function")

        result = FileTracker._sanitize_filename("!@#$%")
        self.assertEqual(result, "function")

    def test_is_valid_filename(self):
        """Test filename validation logic."""
        # Valid filename
        self.assertTrue(FileTracker._is_valid_filename("test.py"))

        # Too long
        long_name = "a" * (config.MAX_FILENAME_LENGTH + 1)
        self.assertFalse(FileTracker._is_valid_filename(long_name))

        # Path traversal
        self.assertFalse(FileTracker._is_valid_filename("../test.py"))
        self.assertFalse(FileTracker._is_valid_filename("test/../file.py"))

        # Wrong extension
        self.assertFalse(FileTracker._is_valid_filename("test.txt"))

    def test_get_unique_filename_invalid_input(self):
        """Test error handling for invalid input."""
        with self.assertRaises(ValueError):
            self.tracker.get_unique_filename("")

        with self.assertRaises(ValueError):
            self.tracker.get_unique_filename("   ")


class TestVSCodeValidation(unittest.TestCase):
    """Test cases for VS Code validation functions."""

    def test_validate_vscode_executable_valid(self):
        """Test validation with valid executables."""
        self.assertTrue(validate_vscode_executable("code"))
        self.assertTrue(validate_vscode_executable("/usr/bin/code"))
        self.assertTrue(
            validate_vscode_executable("C:\\Program Files\\Microsoft VS Code\\Code.exe")
        )

    def test_validate_vscode_executable_invalid(self):
        """Test validation with invalid executables."""
        # Empty or None
        self.assertFalse(validate_vscode_executable(""))
        self.assertFalse(validate_vscode_executable("   "))

        # Dangerous characters
        self.assertFalse(validate_vscode_executable("code & rm -rf /"))
        self.assertFalse(validate_vscode_executable("code | malicious"))
        self.assertFalse(validate_vscode_executable("code; evil_command"))
        self.assertFalse(validate_vscode_executable("code`whoami`"))

        # Too long
        long_path = "x" * 600
        self.assertFalse(validate_vscode_executable(long_path))

    def test_validate_vscode_executable_type_error(self):
        """Test validation with wrong type input."""
        self.assertFalse(validate_vscode_executable(None))
        self.assertFalse(validate_vscode_executable(123))
        self.assertFalse(validate_vscode_executable(["code"]))


class TestDirectoryManagement(unittest.TestCase):
    """Test cases for directory management functions."""

    def setUp(self):
        """Set up test fixtures with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_generated_dir = config.GENERATED_FILES_DIR

    def tearDown(self):
        """Clean up test fixtures."""
        config.GENERATED_FILES_DIR = self.original_generated_dir

    @patch("app.GENERATED_FILES_DIR")
    def test_ensure_generated_files_dir_success(self, mock_dir):
        """Test successful directory creation."""
        mock_dir.mkdir = Mock()
        mock_dir.exists.return_value = True

        # Mock the test file operations
        test_file_mock = Mock()
        test_file_mock.write_text = Mock()
        test_file_mock.unlink = Mock()
        mock_dir.__truediv__ = Mock(return_value=test_file_mock)

        # Should not raise an exception
        ensure_generated_files_dir()
        mock_dir.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    @patch("app.GENERATED_FILES_DIR")
    def test_ensure_generated_files_dir_permission_error(self, mock_dir):
        """Test directory creation with permission error."""
        mock_dir.mkdir.side_effect = PermissionError("Permission denied")

        with self.assertRaises(PermissionError):
            ensure_generated_files_dir()


class TestContentGeneration(unittest.TestCase):
    """Test cases for content generation functions."""

    @patch("app.pyautogui")
    @patch("app.file_tracker")
    @patch("app.time.sleep")
    def test_write_function_improved_success(
        self, mock_sleep, mock_tracker, mock_pyautogui
    ):
        """Test successful function writing."""
        # Setup mocks
        mock_tracker.get_unique_filename.return_value = ("test.py", Path("test.py"))
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_tracker.get_unique_filename.return_value = ("test.py", mock_path)

        # Mock PyAutoGUI calls
        mock_pyautogui.hotkey = Mock()
        mock_pyautogui.write = Mock()
        mock_pyautogui.press = Mock()

        result = write_function_improved(
            "len()", "Test function", "print(len([1,2,3]))"
        )
        self.assertTrue(result)

    def test_write_function_improved_invalid_input(self):
        """Test function writing with invalid input."""
        # Empty strings
        self.assertFalse(write_function_improved("", "desc", "example"))
        self.assertFalse(write_function_improved("func", "", "example"))
        self.assertFalse(write_function_improved("func", "desc", ""))

        # Non-string inputs
        self.assertFalse(write_function_improved(None, "desc", "example"))
        self.assertFalse(write_function_improved("func", 123, "example"))

    @patch("app.pyautogui")
    @patch("app.file_tracker")
    def test_write_function_improved_pyautogui_error(
        self, mock_tracker, mock_pyautogui
    ):
        """Test function writing with PyAutoGUI error."""
        mock_tracker.get_unique_filename.return_value = ("test.py", Path("test.py"))
        mock_pyautogui.hotkey.side_effect = RuntimeError("PyAutoGUI error")

        result = write_function_improved(
            "len()", "Test function", "print(len([1,2,3]))"
        )
        self.assertFalse(result)


class TestEnvironmentValidation(unittest.TestCase):
    """Test cases for environment validation."""

    @patch("app.validate_vscode_executable")
    @patch("app.ensure_generated_files_dir")
    @patch("app.pyautogui.position")
    def test_validate_environment_success(
        self, mock_position, mock_ensure_dir, mock_validate_vs
    ):
        """Test successful environment validation."""
        mock_validate_vs.return_value = True
        mock_ensure_dir.return_value = None
        mock_position.return_value = (100, 100)

        from app import validate_environment

        self.assertTrue(validate_environment())

    @patch("app.validate_vscode_executable")
    def test_validate_environment_invalid_vscode(self, mock_validate_vs):
        """Test environment validation with invalid VS Code."""
        mock_validate_vs.return_value = False

        from app import validate_environment

        self.assertFalse(validate_environment())

    @patch("app.validate_vscode_executable")
    @patch("app.ensure_generated_files_dir")
    def test_validate_environment_directory_error(
        self, mock_ensure_dir, mock_validate_vs
    ):
        """Test environment validation with directory creation error."""
        mock_validate_vs.return_value = True
        mock_ensure_dir.side_effect = PermissionError("Cannot create directory")

        from app import validate_environment

        self.assertFalse(validate_environment())


class TestIntegration(unittest.TestCase):
    """Integration tests for CodeWeaverBot."""

    def test_functions_list_integrity(self):
        """Test that the FUNCTIONS list is properly structured."""
        from app import FUNCTIONS

        self.assertIsInstance(FUNCTIONS, list)
        self.assertGreater(len(FUNCTIONS), 0)

        for func_tuple in FUNCTIONS:
            self.assertIsInstance(func_tuple, tuple)
            self.assertEqual(len(func_tuple), 3)
            func_name, description, example = func_tuple
            self.assertIsInstance(func_name, str)
            self.assertIsInstance(description, str)
            self.assertIsInstance(example, str)
            self.assertGreater(len(func_name.strip()), 0)
            self.assertGreater(len(description.strip()), 0)
            self.assertGreater(len(example.strip()), 0)

    def test_config_integration(self):
        """Test integration between config and app modules."""
        # Test that config constants are accessible and valid
        self.assertIsInstance(config.MAX_FILENAME_LENGTH, int)
        self.assertGreater(config.MAX_FILENAME_LENGTH, 0)

        # Test that config validation works
        self.assertTrue(config.validate_config())

    def test_file_tracker_with_config(self):
        """Test FileTracker integration with config constants."""
        tracker = FileTracker()
        filename, path = tracker.get_unique_filename("test")

        # Should respect config limits
        self.assertLessEqual(len(filename), config.MAX_FILENAME_LENGTH)
        self.assertTrue(config.is_safe_filename(filename))


if __name__ == "__main__":
    # Configure test logging
    import logging

    logging.basicConfig(level=logging.CRITICAL)  # Suppress logs during testing

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestConfig,
        TestFileTracker,
        TestVSCodeValidation,
        TestDirectoryManagement,
        TestContentGeneration,
        TestEnvironmentValidation,
        TestIntegration,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")

    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")

    print(f"{'='*50}")

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
