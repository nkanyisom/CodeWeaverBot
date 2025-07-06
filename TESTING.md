# Testing Documentation for CodeWeaverBot

## Overview

CodeWeaverBot includes a comprehensive test suite designed to ensure code quality, security, and cross-platform compatibility. The testing framework covers unit tests, integration tests, security validation, and performance testing.

## Test Structure

### Test Files

- **`test_codeweaver_bot.py`** - Main unit test suite covering:
  - Configuration validation
  - File tracking functionality
  - VS Code integration
  - Content generation
  - Environment validation
  - Integration testing

- **`test_security_performance.py`** - Security and performance tests covering:
  - Security feature validation
  - Performance benchmarks
  - Edge case handling
  - Cross-platform compatibility
  - Error handling robustness

- **`run_tests.py`** - Test runner script with options for:
  - Running all tests
  - Running security tests only
  - Verbose output
  - Command-line interface

## Running Tests

### Local Testing

#### Basic Test Execution
```bash
# Run all tests
python run_tests.py

# Run with verbose output
python run_tests.py --verbose

# Run only security tests
python run_tests.py --security-only
```

#### Using Python's unittest directly
```bash
# Run main test suite
python -m unittest test_codeweaver_bot.py -v

# Run security tests
python -m unittest test_security_performance.py -v

# Run specific test class
python -m unittest test_codeweaver_bot.TestConfig -v
```

#### Using pytest (if installed)
```bash
# Install pytest
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_codeweaver_bot.py -v

# Run tests with specific markers
pytest -m security -v
```

### Platform-Specific Setup

#### 🪟 Windows
```powershell
# PowerShell
python run_tests.py --verbose

# With virtual environment
.\venv\Scripts\activate
python run_tests.py
```

#### 🐧 Linux
```bash
# Install testing dependencies
sudo apt-get install python3-tk python3-dev xvfb

# Set up virtual display for GUI testing
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &

# Run tests
python3 run_tests.py --verbose
```

#### 🍎 macOS
```bash
# Ensure PyObjC is installed for GUI testing
pip install pyobjc-core pyobjc

# Run tests
python3 run_tests.py --verbose
```

## Test Categories

### Unit Tests

**Configuration Tests (`TestConfig`)**
- Version information validation
- Security constants verification
- Timing configuration validation
- Path configuration testing
- Content limits validation

**File Tracker Tests (`TestFileTracker`)**
- Unique filename generation
- Filename sanitization
- Collision prevention
- Input validation
- Security constraints

**VS Code Validation Tests (`TestVSCodeValidation`)**
- Executable path validation
- Security checks for command injection
- Input type validation
- Length limit enforcement

### Security Tests

**Security Features (`TestSecurityFeatures`)**
- Path traversal attack prevention
- Filename length limit enforcement
- Content injection prevention
- Safe character validation
- Configuration immutability

**Performance and Limits (`TestPerformanceAndLimits`)**
- Filename generation performance
- Content truncation performance
- Memory usage limits
- Runtime hours validation boundaries

### Integration Tests

**Environment Validation (`TestEnvironmentValidation`)**
- Complete environment setup validation
- VS Code accessibility testing
- Directory creation and permissions
- PyAutoGUI functionality verification

**Cross-Platform Compatibility (`TestCrossPlatformCompatibility`)**
- Path separator handling
- Path length limits for different platforms
- File extension validation
- Platform-specific configurations

## Test Fixtures and Mocking

### Mock Objects Used

- **PyAutoGUI**: Mocked for GUI automation testing without actual GUI interaction
- **Subprocess**: Mocked for VS Code launching without actually starting VS Code
- **File System**: Temporary directories and files for safe testing
- **Time Functions**: Mocked to speed up time-dependent tests

### Test Data

Tests use controlled test data including:
- Valid and invalid filenames
- Various content lengths
- Different VS Code executable paths
- Malicious input patterns
- Cross-platform path formats

## Continuous Integration

### GitHub Actions Workflow

The project includes a comprehensive CI/CD pipeline (`.github/workflows/tests.yml`) that:

- Tests on multiple platforms (Ubuntu, Windows, macOS)
- Tests Python versions 3.6 through 3.11
- Runs security audits with Bandit and Safety
- Generates coverage reports
- Uploads security reports as artifacts

### Security Scanning

Automated security scanning includes:
- **Bandit**: Static security analysis for Python code
- **Safety**: Dependency vulnerability checking
- **Custom Security Tests**: Application-specific security validations

## Test Coverage

### Current Coverage Areas

✅ **Configuration Management** (100%)
- All config constants and functions
- Environment variable handling
- Validation logic

✅ **File Operations** (95%)
- File tracking and naming
- Directory management
- Path validation

✅ **Security Features** (100%)
- Input sanitization
- Path traversal prevention
- Content length limits

✅ **Error Handling** (90%)
- Exception handling
- Graceful degradation
- Error logging

### Areas for Future Enhancement

- **GUI Automation Testing**: More comprehensive PyAutoGUI interaction testing
- **End-to-End Testing**: Full workflow testing with actual VS Code
- **Performance Benchmarking**: Detailed performance metrics and regression testing
- **User Interface Testing**: Testing of command-line interfaces and user interactions

## Debugging Tests

### Verbose Output

For detailed test debugging:
```bash
python run_tests.py --verbose
```

### Individual Test Debugging

To debug specific tests:
```python
# Add to test method for debugging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use print statements in test methods
def test_specific_function(self):
    print(f"Testing with input: {test_input}")
    result = function_under_test(test_input)
    print(f"Result: {result}")
    self.assertEqual(result, expected)
```

### Test Isolation

Each test is designed to be independent:
- No shared state between tests
- Proper setup and teardown
- Mocked external dependencies
- Temporary files and directories

## Best Practices

### Writing New Tests

1. **Follow naming conventions**: `test_<function_name>_<scenario>`
2. **Use descriptive test names**: Clearly indicate what is being tested
3. **Test both positive and negative cases**: Valid input and error conditions
4. **Mock external dependencies**: Don't rely on external systems
5. **Keep tests focused**: One test should verify one specific behavior
6. **Use appropriate assertions**: Choose the most specific assertion available

### Test Maintenance

1. **Keep tests up to date**: Update tests when functionality changes
2. **Remove obsolete tests**: Delete tests for removed features
3. **Refactor common code**: Use helper methods for repeated setup
4. **Document complex tests**: Add comments for non-obvious test logic
5. **Monitor test performance**: Keep tests fast and efficient

## Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure Python path includes current directory
export PYTHONPATH="${PYTHONPATH}:."
```

**GUI Testing on Headless Systems**
```bash
# Use virtual display on Linux
sudo apt-get install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

**Permission Errors**
```bash
# Ensure test directories are writable
chmod 755 .
mkdir -p generated_files
```

### Test Environment Issues

If tests fail due to environment issues:

1. **Check Python version**: Ensure compatible Python version (3.6+)
2. **Verify dependencies**: Install all required packages from requirements.txt
3. **Check file permissions**: Ensure write access to test directories
4. **Validate display**: For GUI tests, ensure display is available
5. **Review logs**: Check test output for specific error messages

## Reporting Issues

When reporting test failures, include:

1. **Operating system and version**
2. **Python version**
3. **Complete error output**
4. **Steps to reproduce**
5. **Expected vs. actual behavior**
6. **Environment details** (virtual environment, dependencies, etc.)

This comprehensive testing framework ensures CodeWeaverBot maintains high quality, security, and reliability across all supported platforms.
