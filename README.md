# CodeWeaverBot

An intelligent automation bot that demonstrates Python programming concepts by autonomously creating and writing code examples in Visual Studio Code. CodeWeaverBot uses GUI automation to simulate human interaction with VS Code, weaving together educational Python examples over a specified duration.

> **📚 EDUCATIONAL PURPOSE DISCLAIMER**  
> This project is designed **exclusively for educational and learning purposes**. It demonstrates GUI automation techniques, Python programming concepts, and software development best practices. This tool should be used responsibly in appropriate environments and in compliance with your organization's policies. Always ensure you have proper authorization before running automation tools in any workspace.

## 🎯 Project Overview

CodeWeaverBot is designed to:
- **Automatically launch VS Code** with new windows
- **Generate Python code examples** for educational purposes
- **Create organized file structures** with unique naming
- **Demonstrate core Python functions** with practical examples
- **Maintain consistent coding activity** for extended periods

### Key Features

- ✅ **Automated VS Code Integration** - Seamlessly opens and controls VS Code
- ✅ **Smart File Management** - Saves files in organized `generated_files/` directory
- ✅ **Unique File Naming** - Prevents duplicates with incremental numbering
- ✅ **Educational Content** - Covers essential Python functions with examples
- ✅ **Robust Error Handling** - Comprehensive error recovery and structured logging
- ✅ **Security Features** - Input validation, path sanitization, and secure subprocess handling
- ✅ **Safety Controls** - Emergency stop and fail-safe mechanisms
- ✅ **Type Safety** - Full type annotations and runtime validation
- ✅ **Configurable Runtime** - Customizable execution duration with safety limits

## 🛠️ Technical Stack

- **Language**: Python 3.6+
- **GUI Automation**: PyAutoGUI
- **Process Management**: subprocess
- **Platform**: Windows (with Linux/Mac support)

## 📋 Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, Linux (Ubuntu 18.04+, Debian 10+), or macOS (10.14+)
- **Python**: Version 3.6 or higher
- **Visual Studio Code**: Installed and accessible via command line
- **Display**: Active desktop session (GUI automation required - no headless support)

### Platform-Specific Requirements

#### 🪟 Windows
- **VS Code**: Install from [official website](https://code.visualstudio.com/)
- **Python**: Install from [python.org](https://www.python.org/) or Microsoft Store
- **Dependencies**: No additional system packages required

#### 🐧 Linux (Ubuntu/Debian)
- **VS Code**: Install via apt or snap
- **System packages** (required for PyAutoGUI):
```bash
sudo apt update
sudo apt install python3-pip python3-tk python3-dev
sudo apt install scrot python3-xlib  # For screen capture
sudo apt install xvfb  # Optional: for virtual display testing
```
- **VS Code installation**:
```bash
# Method 1: Official repository
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# Method 2: Snap
sudo snap install --classic code
```

#### 🍎 macOS
- **VS Code**: Install from [official website](https://code.visualstudio.com/) or via Homebrew
- **Homebrew installation** (recommended):
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install VS Code and Python
brew install --cask visual-studio-code
brew install python
```
- **Additional dependencies**:
```bash
pip3 install pyobjc-core pyobjc  # For PyAutoGUI macOS support
```

### Software Dependencies
- Visual Studio Code with `code` command accessible from terminal
- Python with pip package manager
- Active desktop environment (X11 on Linux, Quartz on macOS)

## 🚀 Installation & Setup

### 1. Clone or Download
```bash
git clone https://github.com/nkanyisom/CodeWeaverBot.git
cd CodeWeaverBot
```

### 2. Platform-Specific Setup

#### 🪟 Windows Setup
```powershell
# Install dependencies
pip install -r requirements.txt

# Verify VS Code installation
code --version
```

#### 🐧 Linux Setup
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Verify VS Code installation
code --version

# If code command not found, create symlink (Ubuntu/Debian)
sudo ln -s /usr/share/code/bin/code /usr/local/bin/code
```

#### 🍎 macOS Setup
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip3 install -r requirements.txt

# Verify VS Code installation
code --version

# If code command not found, add to PATH
echo 'export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"' >> ~/.zshrc
source ~/.zshrc
```

### 3. VS Code Command Verification

Test VS Code accessibility from command line:

#### All Platforms
```bash
code --version
```

**Expected output**:
```
1.80.0 (or similar version)
b3e4e68a0bc097f0ae7907b217c1119af9e03435
x64
```

### 4. Environment Configuration

#### Method 1: Environment Variables (Recommended)

**🪟 Windows (PowerShell)**
```powershell
$env:VSCODE_EXECUTABLE="code"
$env:TOTAL_RUNTIME_HOURS="1"
$env:LOG_LEVEL="INFO"
```

**🪟 Windows (Command Prompt)**
```cmd
set VSCODE_EXECUTABLE=code
set TOTAL_RUNTIME_HOURS=1
set LOG_LEVEL=INFO
```

**🐧 Linux / 🍎 macOS**
```bash
export VSCODE_EXECUTABLE="code"
export TOTAL_RUNTIME_HOURS="1"
export LOG_LEVEL="INFO"

# Make permanent by adding to ~/.bashrc or ~/.zshrc
echo 'export VSCODE_EXECUTABLE="code"' >> ~/.bashrc
```

**Supported Environment Variables**:
- `VSCODE_EXECUTABLE`: Path to VS Code executable
- `TOTAL_RUNTIME_HOURS`: Runtime duration (1-24 hours)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `PYAUTOGUI_PAUSE`: Delay between GUI actions (0.1-2.0 seconds)

#### Method 2: Direct Configuration
Edit configuration in `config.py` or `app.py`:
```python
TOTAL_RUNTIME_HOURS = 1         # Change runtime duration
PYAUTOGUI_PAUSE = 0.8          # Adjust automation speed
VS_CODE_EXECUTABLE = "code"     # VS Code executable path
```

### 5. Platform-Specific VS Code Paths

If the `code` command is not available, use the full path:

#### 🪟 Windows
```python
VS_CODE_EXECUTABLE = r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe"
# Or Program Files installation:
VS_CODE_EXECUTABLE = r"C:\Program Files\Microsoft VS Code\Code.exe"
```

#### 🐧 Linux
```python
VS_CODE_EXECUTABLE = "/usr/bin/code"  # APT installation
VS_CODE_EXECUTABLE = "/snap/bin/code"  # Snap installation
VS_CODE_EXECUTABLE = "/usr/share/code/bin/code"  # Manual installation
```

#### 🍎 macOS
```python
VS_CODE_EXECUTABLE = "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
# Or if installed via Homebrew:
VS_CODE_EXECUTABLE = "/usr/local/bin/code"
```

**Note**: The latest version includes enhanced security features, comprehensive logging, and improved error handling. All configuration constants are now properly defined with type safety and validation.

## 🎮 How to Run

### Platform-Specific Execution

#### 🪟 Windows
```powershell
# PowerShell
python app.py

# Command Prompt
python app.py

# With virtual environment
.\venv\Scripts\activate
python app.py
```

#### 🐧 Linux
```bash
# Direct execution
python3 app.py

# With virtual environment (recommended)
source venv/bin/activate
python app.py

# Background execution with logging
nohup python3 app.py > output.log 2>&1 &
```

#### 🍎 macOS
```bash
# Direct execution
python3 app.py

# With virtual environment (recommended)
source venv/bin/activate
python app.py

# Ensure accessibility permissions are granted (see troubleshooting)
```

### What Happens When You Run It:
1. **Startup Phase**
   - Displays available Python functions
   - Tests VS Code connection (tries subprocess first, falls back to GUI method)
   - Creates `generated_files/` directory
   - Validates environment and permissions

2. **Automation Phase**
   - Opens new VS Code window using platform-appropriate method
   - Continuously creates Python example files
   - Saves files with unique names (e.g., `len_example_001.py`)
   - Displays progress and remaining time
   - Logs all activities to `codeweaver_bot.log`

3. **Completion Phase**
   - Shows statistics (successful/failed files)
   - Reports total runtime
   - Files saved in `generated_files/` folder

### Emergency Stop Methods

#### All Platforms
- **Mouse Failsafe**: Move mouse to top-left corner of screen
- **Keyboard Interrupt**: Press `Ctrl+C` in terminal

#### Platform-Specific Stop Methods
- **Windows**: `Ctrl+C` or close terminal window
- **Linux**: `Ctrl+C`, `Ctrl+Z` (suspend), or `killall python3`
- **macOS**: `Cmd+C` or `Ctrl+C` in terminal

## 📁 Project Structure

```
CodeWeaverBot/
├── app.py                      # Main automation script (enhanced with security features)
├── config.py                   # Configuration module with security validation
├── README.md                   # This file
├── requirements.txt            # Python dependencies (updated for security)
├── TECHNICAL_SPECIFICATION.md  # Detailed technical docs
├── SECURITY_CHECKLIST.md       # Security review and compliance checklist
├── TESTING.md                  # Comprehensive testing documentation
├── codeweaver_bot.log          # Runtime logs (generated during execution)
├── test_codeweaver_bot.py      # Main unit test suite
├── test_security_performance.py # Security and performance tests
├── run_tests.py                # Test runner script
├── pytest.ini                 # pytest configuration
├── .github/
│   └── workflows/
│       └── tests.yml           # CI/CD pipeline for automated testing
└── generated_files/            # Auto-created directory
    ├── len_example_001.py      # Generated examples (when created)
    ├── str_example_002.py      # Generated examples (when created)
    ├── range_example_003.py    # Generated examples (when created)
    └── ...                     # More examples
```

### Key Files Explained

- **`app.py`**: Main application with enhanced security, logging, and cross-platform support
- **`config.py`**: Centralized configuration with validation and platform-specific settings
- **`requirements.txt`**: Updated with version pinning and development tools
- **`SECURITY_CHECKLIST.md`**: Complete security review and compliance documentation
- **`codeweaver_bot.log`**: Structured logging output for debugging and monitoring
- **`generated_files/`**: Auto-created directory for all generated Python examples

### Testing Files

- **`test_codeweaver_bot.py`**: Comprehensive unit test suite covering all core functionality
- **`test_security_performance.py`**: Security-focused and performance tests
- **`run_tests.py`**: Test runner with command-line options
- **`pytest.ini`**: pytest configuration for advanced testing
- **`TESTING.md`**: Complete testing documentation and guide
- **`.github/workflows/tests.yml`**: CI/CD pipeline for automated testing

## 🐍 Python Functions Covered

CodeWeaverBot demonstrates these essential Python functions:

| Function | Description | Example Use Case |
|----------|-------------|------------------|
| `len()` | Get object length | Lists, strings, dictionaries |
| `range()` | Generate number sequences | Loops and iterations |
| `str()` | Convert to string | Type conversions |
| `type()` | Get object type | Debugging and validation |
| `print()` | Console output | Display results |
| `input()` | User input | Interactive programs |

Each generated file includes:
- Function description and purpose
- Practical code examples
- Expected output comments
- Best practice demonstrations

## 🧪 Testing

CodeWeaverBot includes a comprehensive test suite to ensure code quality, security, and cross-platform compatibility.

### Running Tests

#### Quick Test Execution
```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py --verbose

# Run only security tests
python run_tests.py --security-only
```

#### Platform-Specific Testing

**🪟 Windows**
```powershell
# PowerShell
python run_tests.py --verbose
```

**🐧 Linux**
```bash
# Install testing dependencies
sudo apt-get install python3-tk python3-dev xvfb

# Run tests with virtual display
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
python3 run_tests.py --verbose
```

**🍎 macOS**
```bash
# Ensure PyObjC is installed
pip install pyobjc-core pyobjc

# Run tests
python3 run_tests.py --verbose
```

### Test Coverage

✅ **Unit Tests** (54 tests)
- Configuration validation
- File tracking and security
- VS Code integration
- Content generation
- Environment validation

✅ **Security Tests** (21 tests)
- Path traversal prevention
- Input validation
- Content injection protection
- Performance limits

✅ **Integration Tests**
- Cross-platform compatibility
- Error handling robustness
- Complete workflow validation

For detailed testing information, see [`TESTING.md`](TESTING.md).

## ⚙️ Configuration Options

### Runtime Settings
```python
TOTAL_RUNTIME_HOURS = 1     # Duration (hours) - validated for safety
PYAUTOGUI_PAUSE = 0.8       # Delay between actions (seconds)
VS_CODE_EXECUTABLE = "code" # VS Code executable path - security validated
```

### Directory Settings
```python
PROJECT_DIR = Path(__file__).parent.absolute()  # Using pathlib for security
GENERATED_FILES_DIR = PROJECT_DIR / "generated_files"  # Organized output
```

### Safety and Security Settings
```python
pyautogui.FAILSAFE = True       # Emergency mouse failsafe
MAX_FILENAME_LENGTH = 100       # Prevent long filename attacks
MAX_PATH_LENGTH = 260          # Windows path limit enforcement
MAX_CONSECUTIVE_FAILURES = 5   # Auto-stop on repeated failures
```

### Configuration Module (`config.py`)

All settings are centralized in the `config.py` module for enhanced security and maintainability:

```python
# Example configuration options in config.py
VERSION = "2.0"
TOTAL_RUNTIME_HOURS = 1
PYAUTOGUI_PAUSE = 0.8
VS_CODE_EXECUTABLE = "code"
MAX_CONTENT_LENGTH = 10240  # 10KB limit for generated content
SAFE_FILENAME_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-.")
```

**Benefits of centralized configuration**:
- ✅ **Security Validation**: All settings are validated on startup
- ✅ **Environment Variables**: Support for secure environment-based configuration
- ✅ **Type Safety**: Full type annotations and runtime validation
- ✅ **Cross-Platform**: Platform-specific defaults and path handling

## � Security & Code Quality Improvements

### Security Features
- **Input Validation**: All inputs sanitized and validated for security
- **Path Sanitization**: Prevention of directory traversal attacks
- **Command Injection Protection**: Secure subprocess handling
- **Type Safety**: Full type annotations and runtime validation
- **Secure Logging**: Structured logging without sensitive data exposure
- **Resource Limits**: Memory and file size protections

### Code Quality Standards
- **PEP 8 Compliance**: Follows Python style guidelines
- **Type Annotations**: Complete type hints for better code safety
- **Exception Specificity**: Catches specific exceptions instead of generic ones
- **Lazy Logging**: Efficient logging format strings
- **Configuration Management**: Centralized, validated configuration
- **Documentation**: Comprehensive docstrings and comments

### Security Validation
See `SECURITY_CHECKLIST.md` for complete security review and compliance documentation.

## 🔧 Troubleshooting

### Platform-Specific Issues

#### 🪟 Windows Issues

**VS Code Not Found**
```log
Error: [WinError 2] The system cannot find the file specified
```
- **Solution**:
  ```powershell
  # Check VS Code installation
  code --version
  
  # If not found, find VS Code installation
  dir "C:\Users\$env:USERNAME\AppData\Local\Programs\Microsoft VS Code\Code.exe"
  dir "C:\Program Files\Microsoft VS Code\Code.exe"
  
  # Update configuration with full path
  VS_CODE_EXECUTABLE = r"C:\Users\{username}\AppData\Local\Programs\Microsoft VS Code\Code.exe"
  ```

**Permission Issues**
- Run terminal as Administrator if needed
- Check Windows Defender or antivirus exclusions
- Ensure Python and VS Code are allowed through firewall

**PyAutoGUI Issues**
- Install Visual C++ Redistributable if needed
- Update to latest PyAutoGUI version: `pip install --upgrade pyautogui`

#### 🐧 Linux Issues

**VS Code Command Not Found**
```bash
bash: code: command not found
```
- **Solution**:
  ```bash
  # For APT installation
  sudo ln -s /usr/share/code/bin/code /usr/local/bin/code
  
  # For Snap installation
  export PATH="$PATH:/snap/bin"
  
  # Or use full path in config
  VS_CODE_EXECUTABLE = "/usr/bin/code"  # or /snap/bin/code
  ```

**X11 Display Issues**
- Ensure X11 forwarding is enabled: `export DISPLAY=:0`
- Install X11 development packages: `sudo apt install xorg-dev`
- For headless testing: `sudo apt install xvfb`

**Permission/Security Issues**
- Add user to input group: `sudo usermod -a -G input $USER`
- Install accessibility packages: `sudo apt install at-spi2-core`
- Grant Python access to input devices

**PyAutoGUI Dependencies Missing**
```bash
sudo apt update
sudo apt install python3-tk python3-dev
sudo apt install scrot python3-xlib
pip3 install pillow  # For image processing
```

#### 🍎 macOS Issues

**VS Code Command Not Found**
```bash
zsh: command not found: code
```
- **Solution**:
  ```bash
  # Add to PATH
  echo 'export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"' >> ~/.zshrc
  source ~/.zshrc
  
  # Or create symlink
  sudo ln -s "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" /usr/local/bin/code
  ```

**Accessibility Permissions Required**
- Go to **System Preferences > Security & Privacy > Privacy**
- Select **Accessibility** from left panel
- Add Terminal and Python to allowed applications
- **Important**: May need to restart application after permission grant

**PyAutoGUI macOS Issues**
```bash
# Install required dependencies
pip3 install pyobjc-core pyobjc

# For older macOS versions
pip3 install pyautogui[PIL]
```

**Gatekeeper Issues**
- Allow Python in **System Preferences > Security & Privacy > General**
- If blocked: `sudo spctl --master-disable` (temporarily, then re-enable)

### Common Cross-Platform Issues

#### VS Code Won't Open
- **Problem**: "Failed to open VS Code via subprocess"
- **Diagnostic Steps**:
  ```bash
  # Test VS Code manually
  code --version
  code --new-window
  
  # Check PATH
  echo $PATH  # Linux/macOS
  echo $env:PATH  # Windows PowerShell
  ```
- **Solutions**:
  1. Use full path to VS Code executable
  2. Add VS Code to system PATH
  3. Check VS Code installation integrity
  4. Try fallback method (Windows Run dialog)

#### Multiple VS Code Windows Opening
- **Problem**: Bot opens multiple VS Code instances
- **Solution**: 
  - Fixed in latest version - only one instance should open
  - Close extra windows manually if they appear
  - Check for conflicting VS Code processes: `ps aux | grep code` (Linux/macOS)

#### Files Not Saving Correctly
- **Problem**: Save dialog timing issues
- **Solutions**:
  ```python
  # Increase timing delays in config
  PYAUTOGUI_PAUSE = 1.0  # Slower systems
  SAVE_DIALOG_TIMEOUT = 3.0  # Slower save dialogs
  FILE_CREATION_TIMEOUT = 2.0  # More time for file creation
  ```
- Check file permissions in `generated_files/` directory
- Ensure no other applications interfere with focus

#### Bot Stops Unexpectedly
- **Problem**: Automation interruption
- **Common Causes**:
  - Mouse moved to top-left corner (failsafe triggered)
  - Focus lost from VS Code window
  - System sleep/screensaver activation
  - Insufficient disk space
- **Solutions**:
  - Keep mouse away from screen corners
  - Disable screensaver during execution
  - Monitor system logs: `tail -f codeweaver_bot.log`

### Performance Optimization by Platform

#### 🪟 Windows Optimization
- **Fast Systems**: `PYAUTOGUI_PAUSE = 0.5`
- **Slow Systems**: `PYAUTOGUI_PAUSE = 1.2`
- **Multiple Monitors**: Set VS Code to open on primary display
- **Resource Management**: Close unnecessary applications

#### 🐧 Linux Optimization
- **Lightweight DEs**: Works best with GNOME, KDE, XFCE
- **Wayland Users**: May need to switch to X11 session
- **Resource Usage**: Monitor with `htop` during execution
- **Network Storage**: Avoid running on mounted network drives

#### 🍎 macOS Optimization
- **Performance**: Disable visual effects during execution
- **Battery**: Connect to power source for long runs
- **Focus**: Use dedicated desktop space for automation
- **Permissions**: Keep accessibility permissions current

### Debug Mode

Enable debug logging for troubleshooting:
```python
# In config.py
LOG_LEVEL = "DEBUG"

# Or set environment variable
export LOG_LEVEL=DEBUG  # Linux/macOS
set LOG_LEVEL=DEBUG     # Windows
```

View detailed logs:
```bash
# Real-time log viewing
tail -f codeweaver_bot.log  # Linux/macOS
Get-Content codeweaver_bot.log -Wait  # Windows PowerShell

# View last 50 lines
tail -n 50 codeweaver_bot.log  # Linux/macOS
Get-Content codeweaver_bot.log -Tail 50  # Windows PowerShell
```

**Log File Features**:
- ✅ **Structured Logging**: JSON-like format for easy parsing
- ✅ **Security-Safe**: No sensitive information in logs
- ✅ **Cross-Platform**: Works on all supported operating systems
- ✅ **Rotation Ready**: Can be configured for automatic log rotation
- ✅ **Debug Information**: Detailed execution flow and error context
