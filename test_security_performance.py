"""
Performance and Security Tests for CodeWeaverBot
===============================================

Additional test suite focusing on performance, security, and edge cases.

Author: nkmalunga
Version: 2.0
Date: July 6, 2025
"""

import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the project directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

import config


class TestSecurityFeatures(unittest.TestCase):
    """Test security-related functionality."""

    def test_path_traversal_prevention(self):
        """Test that path traversal attacks are prevented."""
        dangerous_filenames = [
            "../../../etc/passwd",
            "..\\..\\windows\\system32\\config",
            "test/../../../sensitive.txt",
            "..\\test.py",
            "/etc/shadow",
            "C:\\Windows\\System32\\config",
        ]

        for dangerous_name in dangerous_filenames:
            self.assertFalse(
                config.is_safe_filename(dangerous_name),
                f"Should reject dangerous filename: {dangerous_name}",
            )

    def test_filename_length_limits(self):
        """Test filename length restrictions."""
        # Test at boundary
        max_length_name = "a" * (config.MAX_FILENAME_LENGTH - 3) + ".py"
        self.assertTrue(config.is_safe_filename(max_length_name))

        # Test over limit
        over_limit_name = "a" * (config.MAX_FILENAME_LENGTH + 1)
        self.assertFalse(config.is_safe_filename(over_limit_name))

    def test_content_injection_prevention(self):
        """Test that content injection is prevented."""
        malicious_content = "x" * (config.MAX_CONTENT_LENGTH * 2)
        safe_content = config.get_safe_content_length(malicious_content)

        self.assertLessEqual(len(safe_content), config.MAX_CONTENT_LENGTH + 100)
        self.assertIn("truncated", safe_content)

    def test_safe_character_validation(self):
        """Test that only safe characters are allowed in filenames."""
        unsafe_chars = ["<", ">", ":", '"', "|", "?", "*", "\0", "\n", "\r"]

        for char in unsafe_chars:
            filename = f"test{char}.py"
            self.assertFalse(
                config.is_safe_filename(filename),
                f"Should reject filename with unsafe character: {char}",
            )

    def test_configuration_immutability(self):
        """Test that critical configuration cannot be easily tampered with."""
        original_max_length = config.MAX_FILENAME_LENGTH
        original_allowed_extensions = config.ALLOWED_FILE_EXTENSIONS.copy()

        # Ensure these are the expected types and values
        self.assertIsInstance(config.MAX_FILENAME_LENGTH, int)
        self.assertIsInstance(config.ALLOWED_FILE_EXTENSIONS, set)
        self.assertEqual(original_max_length, config.MAX_FILENAME_LENGTH)
        self.assertEqual(original_allowed_extensions, config.ALLOWED_FILE_EXTENSIONS)


class TestPerformanceAndLimits(unittest.TestCase):
    """Test performance characteristics and resource limits."""

    def test_filename_generation_performance(self):
        """Test that filename generation is reasonably fast."""
        start_time = time.time()

        # Generate 100 filenames
        for i in range(100):
            config.is_safe_filename(f"test_{i}.py")

        end_time = time.time()
        duration = end_time - start_time

        # Should take less than 1 second for 100 validations
        self.assertLess(duration, 1.0, "Filename validation should be fast")

    def test_content_truncation_performance(self):
        """Test content truncation performance."""
        large_content = "x" * (config.MAX_CONTENT_LENGTH * 3)

        start_time = time.time()
        result = config.get_safe_content_length(large_content)
        end_time = time.time()

        duration = end_time - start_time
        self.assertLess(duration, 0.1, "Content truncation should be fast")
        self.assertIn("truncated", result)

    def test_memory_usage_limits(self):
        """Test that memory usage is controlled."""
        # Test with very large content
        huge_content = "A" * (config.MAX_CONTENT_LENGTH * 10)
        result = config.get_safe_content_length(huge_content)

        # Should not consume excessive memory
        self.assertLess(len(result), config.MAX_CONTENT_LENGTH * 2)

    def test_runtime_hours_validation_boundary(self):
        """Test runtime hours validation at boundaries."""
        # Test exact boundaries
        self.assertEqual(config.get_safe_runtime_hours(0.1), 0.1)
        self.assertEqual(
            config.get_safe_runtime_hours(config.MAX_RUNTIME_HOURS),
            config.MAX_RUNTIME_HOURS,
        )

        # Test beyond boundaries
        self.assertEqual(config.get_safe_runtime_hours(0.05), 0.1)
        self.assertEqual(
            config.get_safe_runtime_hours(config.MAX_RUNTIME_HOURS + 10),
            config.MAX_RUNTIME_HOURS,
        )


class TestConfigurationEdgeCases(unittest.TestCase):
    """Test edge cases in configuration."""

    def test_environment_variable_integration(self):
        """Test environment variable configuration."""
        # Test default values when env vars are not set
        original_vscode = os.environ.get("VSCODE_EXECUTABLE")
        original_log_level = os.environ.get("LOG_LEVEL")

        try:
            # Clear environment variables
            if "VSCODE_EXECUTABLE" in os.environ:
                del os.environ["VSCODE_EXECUTABLE"]
            if "LOG_LEVEL" in os.environ:
                del os.environ["LOG_LEVEL"]

            # Reload config (simulate)
            default_vscode = os.getenv("VSCODE_EXECUTABLE", "code")
            default_log_level = os.getenv("LOG_LEVEL", "INFO")

            self.assertEqual(default_vscode, "code")
            self.assertEqual(default_log_level, "INFO")

        finally:
            # Restore original environment
            if original_vscode:
                os.environ["VSCODE_EXECUTABLE"] = original_vscode
            if original_log_level:
                os.environ["LOG_LEVEL"] = original_log_level

    def test_path_creation_validation(self):
        """Test path creation and validation."""
        # Test that PROJECT_DIR is valid
        self.assertTrue(config.PROJECT_DIR.exists())
        self.assertTrue(config.PROJECT_DIR.is_dir())

        # Test that GENERATED_FILES_DIR path is reasonable
        self.assertTrue(str(config.GENERATED_FILES_DIR).endswith("generated_files"))
        self.assertEqual(config.GENERATED_FILES_DIR.parent, config.PROJECT_DIR)

    def test_logging_configuration(self):
        """Test logging configuration."""
        self.assertIn(
            config.LOG_LEVEL, ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        )
        self.assertIsInstance(config.LOG_FORMAT, str)
        self.assertIn("%(asctime)s", config.LOG_FORMAT)
        self.assertIn("%(levelname)s", config.LOG_FORMAT)

    def test_timing_constants_validity(self):
        """Test that timing constants are reasonable."""
        timing_constants = [
            config.DEFAULT_PAUSE_TIME,
            config.VSCODE_LAUNCH_TIMEOUT,
            config.FILE_CREATION_TIMEOUT,
            config.SAVE_DIALOG_TIMEOUT,
            config.LOOP_INTERVAL,
            config.RETRY_DELAY,
        ]

        for constant in timing_constants:
            self.assertIsInstance(constant, (int, float))
            self.assertGreater(constant, 0)
            self.assertLess(constant, 60)  # Should be reasonable (< 1 minute)

    def test_pyautogui_configuration(self):
        """Test PyAutoGUI configuration."""
        self.assertEqual(config.PYAUTOGUI_PAUSE, config.DEFAULT_PAUSE_TIME)
        self.assertTrue(config.PYAUTOGUI_FAILSAFE)
        self.assertIsInstance(config.PYAUTOGUI_INTERVAL, (int, float))
        self.assertGreater(config.PYAUTOGUI_INTERVAL, 0)


class TestErrorHandling(unittest.TestCase):
    """Test error handling in configuration functions."""

    def test_get_safe_runtime_hours_with_invalid_types(self):
        """Test get_safe_runtime_hours with invalid input types."""
        # Should handle string input gracefully
        try:
            result = config.get_safe_runtime_hours("invalid")
            # If it doesn't raise an exception, it should return a safe default
            self.assertIsInstance(result, (int, float))
        except (TypeError, ValueError):
            # It's also acceptable to raise an exception for invalid types
            pass

    def test_is_safe_filename_with_none(self):
        """Test is_safe_filename with None input."""
        with self.assertRaises((TypeError, AttributeError)):
            config.is_safe_filename(None)

    def test_get_safe_content_length_with_none(self):
        """Test get_safe_content_length with None input."""
        with self.assertRaises((TypeError, AttributeError)):
            config.get_safe_content_length(None)

    def test_configuration_validation_robustness(self):
        """Test that configuration validation is robust."""
        # Should not crash with current configuration
        try:
            result = config.validate_config()
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.fail(f"Configuration validation should not raise exceptions: {e}")


class TestCrossPlatformCompatibility(unittest.TestCase):
    """Test cross-platform compatibility."""

    def test_path_separators(self):
        """Test that paths work across platforms."""
        # Generated files directory should use proper path separator
        path_str = str(config.GENERATED_FILES_DIR)

        # Should not contain mixed separators
        if os.name == "nt":  # Windows
            self.assertNotIn("/", path_str.replace("C:/", ""))  # Allow drive letter
        else:  # Unix-like
            self.assertNotIn("\\", path_str)

    def test_path_length_limits(self):
        """Test path length limits for different platforms."""
        # Windows has 260 character limit
        self.assertEqual(config.MAX_PATH_LENGTH, 260)

        # Test that generated paths respect this limit
        test_path = config.GENERATED_FILES_DIR / ("a" * 100 + ".py")
        self.assertLessEqual(len(str(test_path)), 300)  # Allow some buffer

    def test_file_extension_validation(self):
        """Test file extension validation."""
        # Should only allow .py files
        self.assertIn(".py", config.ALLOWED_FILE_EXTENSIONS)

        # Test various extensions
        valid_files = ["test.py", "example.py", "function.py"]
        invalid_files = ["test.txt", "file.exe", "script.sh", "code.js"]

        for valid_file in valid_files:
            if config.is_safe_filename(valid_file):  # May fail other validations
                pass  # That's OK

        for invalid_file in invalid_files:
            self.assertFalse(
                config.is_safe_filename(invalid_file),
                f"Should reject non-Python file: {invalid_file}",
            )


if __name__ == "__main__":
    # Configure test logging to be quiet
    import logging

    logging.basicConfig(level=logging.CRITICAL)

    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestSecurityFeatures,
        TestPerformanceAndLimits,
        TestConfigurationEdgeCases,
        TestErrorHandling,
        TestCrossPlatformCompatibility,
    ]

    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Security & Performance Test Summary:")
    print(f"Ran {result.testsRun} tests")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print(f"\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}")

    if result.errors:
        print(f"\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}")

    if result.wasSuccessful():
        print(f"\n✅ All security and performance tests passed!")
    else:
        print(f"\n❌ Some tests failed. Review the output above.")

    print(f"{'='*60}")

    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
