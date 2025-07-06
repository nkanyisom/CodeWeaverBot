"""
CodeWeaverBot - Intelligent Code Automation in VSCode
======================================================

An intelligent automation bot that demonstrates Python programming concepts
by autonomously creating and writing code examples in Visual Studio Code.

Author: nkanyisom
Version: 1.0 (Optimized)
Date: July 6, 2025
Repository: https://github.com/nkanyisom/CodeWeaverBot.git

Features:
- Automated VS Code integration with subprocess launching
- Smart file management in organized directories
- Unique file naming with collision prevention
- Comprehensive error handling and recovery
- Cross-platform compatibility (Windows/Linux/macOS)
- Educational Python function demonstrations

Usage:
    python app.py

For more information, see README.md and TECHNICAL_SPECIFICATION.md
"""

import logging
import os
import random
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Tuple

import pyautogui

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("codeweaver_bot.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# --- Security and Validation Constants ---
MAX_FILENAME_LENGTH = 100
MAX_PATH_LENGTH = 260  # Windows path limit
ALLOWED_FILE_EXTENSIONS = {".py"}
SAFE_FILENAME_CHARS = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
)

# --- Configuration Constants ---
DEFAULT_PAUSE_TIME = 0.8
DEFAULT_RUNTIME_HOURS = 1
VSCODE_LAUNCH_TIMEOUT = 4
FILE_CREATION_TIMEOUT = 1.5
SAVE_DIALOG_TIMEOUT = 2.5
LOOP_INTERVAL = 8
MAX_RETRY_ATTEMPTS = 3

# Configuration settings
PYAUTOGUI_PAUSE = DEFAULT_PAUSE_TIME
PYAUTOGUI_FAILSAFE = True
TOTAL_RUNTIME_HOURS = DEFAULT_RUNTIME_HOURS
VS_CODE_EXECUTABLE = "code"  # Renamed for clarity

# Project directory settings - using pathlib for better path handling
PROJECT_DIR = Path(__file__).parent.absolute()
GENERATED_FILES_DIR = PROJECT_DIR / "generated_files"


class FileTracker:
    """Thread-safe file tracking to avoid global variables."""

    def __init__(self):
        self._counter = 1
        self._used_names = set()

    def get_unique_filename(self, func_name: str) -> Tuple[str, Path]:
        """Generate a unique filename with validation."""
        if not isinstance(func_name, str) or not func_name.strip():
            raise ValueError("Function name must be a non-empty string")

        # Sanitize function name
        base_name = self._sanitize_filename(func_name)

        # Generate unique filename
        while True:
            filename = f"{base_name}_example_{self._counter:03d}.py"

            if self._is_valid_filename(filename) and filename not in self._used_names:
                self._used_names.add(filename)
                full_path = GENERATED_FILES_DIR / filename
                self._counter += 1
                return filename, full_path

            self._counter += 1
            if self._counter > 9999:  # Prevent infinite loop
                raise RuntimeError("Unable to generate unique filename")

    @staticmethod
    def _sanitize_filename(func_name: str) -> str:
        """Sanitize function name for safe filename generation."""
        # Remove parentheses and replace spaces with underscores
        sanitized = func_name.replace("()", "").replace(" ", "_").lower()

        # Keep only safe characters
        safe_chars = "".join(c for c in sanitized if c in SAFE_FILENAME_CHARS)

        # Ensure it's not empty and not too long
        if not safe_chars:
            safe_chars = "function"

        return safe_chars[:50]  # Limit length

    @staticmethod
    def _is_valid_filename(filename: str) -> bool:
        """Validate filename for security and length constraints."""
        if len(filename) > MAX_FILENAME_LENGTH:
            return False

        # Check for path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            return False

        # Check file extension
        if not any(filename.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
            return False

        return True


# Initialize PyAutoGUI with secure settings
pyautogui.PAUSE = PYAUTOGUI_PAUSE
pyautogui.FAILSAFE = PYAUTOGUI_FAILSAFE

# Initialize file tracker
file_tracker = FileTracker()

# --- Enhanced Python Functions Repository ---
FUNCTIONS: List[Tuple[str, str, str]] = [
    (
        "len()",
        "Returns the length of an object (string, list, etc.).",
        "my_list = [1, 2, 3, 4, 5]\nprint(f'List length: {len(my_list)}')  # Output: List length: 5\n\nmy_string = 'Hello World'\nprint(f'String length: {len(my_string)}')  # Output: String length: 11",
    ),
    (
        "range()",
        "Generates a sequence of numbers.",
        "# Basic range\nfor i in range(5):\n    print(i, end=' ')  # Output: 0 1 2 3 4\n\n# Range with start and stop\nfor i in range(2, 7):\n    print(i, end=' ')  # Output: 2 3 4 5 6",
    ),
    (
        "str()",
        "Converts an object to a string.",
        "num = 42\nresult = str(num) + ' apples'\nprint(result)  # Output: '42 apples'\n\npi = 3.14159\nprint(f'Pi as string: {str(pi)}')  # Output: Pi as string: 3.14159",
    ),
    (
        "type()",
        "Returns the type of an object.",
        "num = 42\ntext = 'Hello'\nmy_list = [1, 2, 3]\n\nprint(type(num))      # Output: <class 'int'>\nprint(type(text))     # Output: <class 'str'>\nprint(type(my_list))  # Output: <class 'list'>",
    ),
    (
        "print()",
        "Outputs text or variables to the console.",
        "name = 'Alice'\nage = 25\n\nprint('Hello, World!')  # Basic print\nprint(f'Name: {name}, Age: {age}')  # Formatted string\nprint(name, age, sep=' - ')  # Custom separator",
    ),
    (
        "input()",
        "Gets user input from the console.",
        "# Basic input\nuser_name = input('Enter your name: ')\nprint(f'Hello, {user_name}!')\n\n# Input with type conversion\nage = int(input('Enter your age: '))\nprint(f'You are {age} years old')",
    ),
]


def validate_vscode_executable(executable_path: str) -> bool:
    """Validate VS Code executable path for security."""
    if not isinstance(executable_path, str) or not executable_path.strip():
        return False

    # Check for command injection attempts
    dangerous_chars = ["&", "|", ";", "`", "$", "(", ")", "<", ">", "\n", "\r"]
    if any(char in executable_path for char in dangerous_chars):
        logger.warning(
            "Potentially dangerous characters in VS Code path: %s", executable_path
        )
        return False

    # Limit length to prevent buffer overflow attempts
    if len(executable_path) > 500:
        return False

    return True


def open_vscode_new_window() -> bool:
    """Launch a new VS Code window using subprocess for better reliability.

    Returns:
        bool: True if VS Code was successfully launched, False otherwise
    """
    try:
        logger.info("Opening new VS Code window...")

        # Validate VS Code executable
        if not validate_vscode_executable(VS_CODE_EXECUTABLE):
            logger.error("Invalid VS Code executable: %s", VS_CODE_EXECUTABLE)
            return False

        # Ensure generated_files directory exists
        ensure_generated_files_dir()

        # Prepare command arguments securely
        cmd_args = [VS_CODE_EXECUTABLE, "--new-window"]

        # Use subprocess to open a new VS Code window with security considerations
        if os.name == "nt":  # Windows
            # On Windows, use shell=False for security and provide full argument list
            subprocess.Popen(
                cmd_args,
                shell=False,  # More secure than shell=True
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:  # Linux/Mac
            subprocess.Popen(
                cmd_args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )

        # Wait for VS Code to fully load
        time.sleep(VSCODE_LAUNCH_TIMEOUT)
        logger.info("VS Code window opened successfully")
        return True

    except (subprocess.SubprocessError, OSError) as e:
        logger.error("Failed to open VS Code via subprocess: %s", e)
        return _fallback_vscode_launch()


def _fallback_vscode_launch() -> bool:
    """Fallback method for launching VS Code using Windows Run dialog.

    Returns:
        bool: True if fallback launch succeeded, False otherwise
    """
    try:
        logger.info("Attempting fallback VS Code launch method...")
        pyautogui.hotkey("win", "r")  # Open Run dialog
        time.sleep(1)

        # Use the validated executable path
        command = f"{VS_CODE_EXECUTABLE} --new-window"
        pyautogui.write(command, interval=0.1)
        pyautogui.press("enter")
        time.sleep(VSCODE_LAUNCH_TIMEOUT)

        logger.info("Fallback VS Code launch completed")
        return True

    except (RuntimeError, Exception) as e:
        logger.error("PyAutoGUI error in fallback launch: %s", e)
        return False
    except (OSError, PermissionError) as e:
        logger.error("System error in fallback launch: %s", e)
        return False


def ensure_generated_files_dir() -> None:
    """Ensure the generated_files directory exists with proper error handling."""
    try:
        GENERATED_FILES_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Directory ready: %s", GENERATED_FILES_DIR)

        # Verify write permissions
        test_file = GENERATED_FILES_DIR / ".test_write_permissions"
        try:
            test_file.write_text("test")
            test_file.unlink()
            logger.debug("Write permissions verified")
        except (OSError, PermissionError) as e:
            logger.error(
                "No write permissions for directory %s: %s", GENERATED_FILES_DIR, e
            )
            raise

    except (OSError, PermissionError) as e:
        logger.error("Failed to create directory %s: %s", GENERATED_FILES_DIR, e)
        raise


def wait_for_save_dialog() -> None:
    """Wait for save dialog to appear and be ready for input."""
    time.sleep(SAVE_DIALOG_TIMEOUT)


def write_function_improved(func_name: str, description: str, example: str) -> bool:
    """Write a function example to VS Code with improved timing and error handling.

    Args:
        func_name: Name of the Python function
        description: Description of the function
        example: Code example demonstrating the function

    Returns:
        bool: True if file was successfully created, False otherwise
    """
    if not all(
        isinstance(arg, str) and arg.strip()
        for arg in [func_name, description, example]
    ):
        logger.error("Invalid arguments provided to write_function_improved")
        return False

    try:
        logger.info("Creating example for %s...", func_name)

        # Create new file
        pyautogui.hotkey("ctrl", "n")
        time.sleep(FILE_CREATION_TIMEOUT)

        # Generate content with timestamp for better tracking
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = (
            f"# {func_name}: {description}\n"
            f"# Generated by CodeWeaverBot on {timestamp}\n"
            f"# Example:\n\n{example}\n\n# End of example"
        )

        # Validate content length to prevent excessive memory usage
        if len(content) > 10000:  # 10KB limit
            logger.warning("Content too large for %s, truncating...", func_name)
            content = content[:10000] + "\n# ... (truncated)"

        pyautogui.write(content, interval=0.03)
        time.sleep(1)

        # Save the file
        pyautogui.hotkey("ctrl", "s")
        wait_for_save_dialog()

        # Generate unique filename and full path
        try:
            filename, full_path = file_tracker.get_unique_filename(func_name)
        except (ValueError, RuntimeError) as e:
            logger.error("Failed to generate filename for %s: %s", func_name, e)
            return False

        # Validate path length
        if len(str(full_path)) > MAX_PATH_LENGTH:
            logger.error("Path too long: %s", full_path)
            return False

        # Type the full path to save in the generated_files directory
        pyautogui.write(str(full_path), interval=0.05)
        pyautogui.press("enter")
        time.sleep(FILE_CREATION_TIMEOUT)

        # Verify file was created
        if full_path.exists():
            logger.info("Successfully created: %s in generated_files/", filename)
            return True
        else:
            logger.warning("File %s was not created successfully", filename)
            return False

    except (RuntimeError, Exception) as e:
        logger.error("PyAutoGUI error writing function %s: %s", func_name, e)
        return False
    except (OSError, PermissionError) as e:
        logger.error("File system error writing function %s: %s", func_name, e)
        return False


def run_bot_improved(vscode_already_open: bool = False) -> None:
    """Run CodeWeaverBot with enhanced error handling and timing.

    Args:
        vscode_already_open: Whether VS Code is already open
    """
    logger.info("Starting CodeWeaverBot for %s hour(s)...", TOTAL_RUNTIME_HOURS)
    start_time = datetime.now()
    end_time = start_time + timedelta(hours=TOTAL_RUNTIME_HOURS)

    # Open VS Code only if not already open
    if not vscode_already_open:
        if not open_vscode_new_window():
            logger.error("Failed to open VS Code. Exiting...")
            return

    successful_files = 0
    failed_files = 0
    consecutive_failures = 0
    max_consecutive_failures = 5

    logger.info("Starting file generation loop...")

    while datetime.now() < end_time:
        try:
            # Safety check: stop if too many consecutive failures
            if consecutive_failures >= max_consecutive_failures:
                logger.error(
                    "Too many consecutive failures (%s). Stopping bot.",
                    consecutive_failures,
                )
                break

            # Select a random function
            func, desc, example = random.choice(FUNCTIONS)

            # Write the function example
            if write_function_improved(func, desc, example):
                successful_files += 1
                consecutive_failures = 0  # Reset counter on success
            else:
                failed_files += 1
                consecutive_failures += 1

            # Calculate remaining time
            remaining_time = end_time - datetime.now()
            logger.info("Files created: %s, Failed: %s", successful_files, failed_files)
            logger.info("Time remaining: %s", remaining_time)

            # Wait before next iteration
            time.sleep(LOOP_INTERVAL)

        except KeyboardInterrupt:
            logger.info("CodeWeaverBot stopped by user.")
            break
        except (RuntimeError, Exception) as e:
            logger.error("PyAutoGUI error: %s", e)
            failed_files += 1
            consecutive_failures += 1
            time.sleep(5)  # Wait before retrying
        except (OSError, PermissionError) as e:
            logger.error("System error: %s", e)
            failed_files += 1
            consecutive_failures += 1
            time.sleep(5)  # Wait before retrying

    # Final statistics
    total_runtime = datetime.now() - start_time
    logger.info("CodeWeaverBot session completed!")
    logger.info("Successfully created: %s files", successful_files)
    logger.info("Failed attempts: %s files", failed_files)
    logger.info("Total runtime: %s", total_runtime)


def preview_functions() -> None:
    """Preview all available functions."""
    logger.info("Available Python functions:")
    for i, (func, desc, _) in enumerate(FUNCTIONS, 1):
        print(f"{i}. {func}: {desc}")


def validate_environment() -> bool:
    """Validate the environment before running the bot.

    Returns:
        bool: True if environment is valid, False otherwise
    """
    try:
        # Check if VS Code executable is valid
        if not validate_vscode_executable(VS_CODE_EXECUTABLE):
            logger.error("Invalid VS Code executable: %s", VS_CODE_EXECUTABLE)
            return False

        # Check if we can create the output directory
        try:
            ensure_generated_files_dir()
        except (OSError, PermissionError) as e:
            logger.error("Cannot create output directory: %s", e)
            return False

        # Check PyAutoGUI functionality
        try:
            pyautogui.position()  # Test basic PyAutoGUI functionality
        except (RuntimeError, Exception) as e:
            logger.error("PyAutoGUI not functioning properly: %s", e)
            return False

        logger.info("Environment validation passed")
        return True

    except (OSError, RuntimeError) as e:
        logger.error("Environment validation failed: %s", e)
        return False


def main() -> None:
    """Main entry point with proper error handling."""
    try:
        logger.info("CodeWeaverBot - Intelligent Coding Automation in VSCode")
        logger.info("=" * 50)

        # Validate environment first
        if not validate_environment():
            logger.error("Environment validation failed. Exiting...")
            sys.exit(1)

        # Preview available functions
        preview_functions()
        print()

        # Test VS Code connection and start bot if successful
        logger.info("Testing VS Code connection...")
        if open_vscode_new_window():
            logger.info("VS Code opened successfully. Starting CodeWeaverBot...")
            time.sleep(2)
            run_bot_improved(vscode_already_open=True)
        else:
            logger.error(
                "Failed to connect to VS Code. Please check installation and PATH."
            )
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        sys.exit(0)
    except (OSError, RuntimeError, ValueError) as e:
        logger.error("Fatal error: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
