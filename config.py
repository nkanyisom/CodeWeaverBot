"""
Configuration module for CodeWeaverBot
======================================

This module contains all configuration constants and settings for CodeWeaverBot.
Centralizing configuration improves maintainability and security.

Author: nkmalunga
Version: 2.0 (Optimized)
Date: July 6, 2025
"""

import os
from pathlib import Path
from typing import Set

# --- Version Information ---
VERSION = "2.0"
APP_NAME = "CodeWeaverBot"
AUTHOR = "nkmalunga"

# --- Security and Validation Constants ---
MAX_FILENAME_LENGTH = 100
MAX_PATH_LENGTH = 260  # Windows path limit
ALLOWED_FILE_EXTENSIONS: Set[str] = {".py"}
SAFE_FILENAME_CHARS = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-."
)

# --- Timing Constants (in seconds) ---
DEFAULT_PAUSE_TIME = 0.8
VSCODE_LAUNCH_TIMEOUT = 4
FILE_CREATION_TIMEOUT = 1.5
SAVE_DIALOG_TIMEOUT = 2.5
LOOP_INTERVAL = 8
RETRY_DELAY = 5

# --- Runtime Configuration ---
DEFAULT_RUNTIME_HOURS = 1
MAX_RUNTIME_HOURS = 24  # Safety limit
MAX_RETRY_ATTEMPTS = 3
MAX_CONSECUTIVE_FAILURES = 5

# --- File and Directory Settings ---
PROJECT_DIR = Path(__file__).parent.absolute()
GENERATED_FILES_DIR = PROJECT_DIR / "generated_files"
LOG_FILE = PROJECT_DIR / "codeweaver_bot.log"

# --- VS Code Configuration ---
VS_CODE_EXECUTABLE = os.getenv("VSCODE_EXECUTABLE", "code")
VSCODE_ARGS = ["--new-window"]

# --- Content Limits ---
MAX_CONTENT_LENGTH = 10000  # 10KB limit for generated content
MAX_DESCRIPTION_LENGTH = 500
MAX_EXAMPLE_LENGTH = 5000

# --- Logging Configuration ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# --- PyAutoGUI Configuration ---
PYAUTOGUI_PAUSE = DEFAULT_PAUSE_TIME
PYAUTOGUI_FAILSAFE = True
PYAUTOGUI_INTERVAL = 0.03  # Typing interval


# --- Environment Validation ---
def validate_config() -> bool:
    """Validate configuration settings.

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if DEFAULT_RUNTIME_HOURS <= 0 or DEFAULT_RUNTIME_HOURS > MAX_RUNTIME_HOURS:
        return False

    if MAX_FILENAME_LENGTH <= 0 or MAX_PATH_LENGTH <= 0:
        return False

    if not ALLOWED_FILE_EXTENSIONS:
        return False

    return True


# --- Security Functions ---
def get_safe_runtime_hours(requested_hours: float) -> float:
    """Get a safe runtime hours value within limits.

    Args:
        requested_hours: Requested runtime in hours

    Returns:
        float: Safe runtime hours within configured limits
    """
    return max(0.1, min(requested_hours, MAX_RUNTIME_HOURS))


def is_safe_filename(filename: str) -> bool:
    """Check if filename is safe for use.

    Args:
        filename: Filename to validate

    Returns:
        bool: True if filename is safe, False otherwise
    """
    if len(filename) > MAX_FILENAME_LENGTH:
        return False

    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        return False

    # Check file extension
    if not any(filename.endswith(ext) for ext in ALLOWED_FILE_EXTENSIONS):
        return False

    # Check for dangerous characters
    if not all(c in SAFE_FILENAME_CHARS for c in filename):
        return False

    return True


def get_safe_content_length(content: str) -> str:
    """Ensure content is within safe length limits.

    Args:
        content: Content to validate and potentially truncate

    Returns:
        str: Safe content within length limits
    """
    if len(content) <= MAX_CONTENT_LENGTH:
        return content

    return content[:MAX_CONTENT_LENGTH] + "\n# ... (content truncated for safety)"
