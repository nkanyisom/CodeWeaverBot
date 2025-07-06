"""
Test Runner for CodeWeaverBot
============================

Simple test runner script to execute all test suites.

Usage:
    python run_tests.py
    python run_tests.py --verbose
    python run_tests.py --security-only
    python run_tests.py --help

Author: nkmalunga
Version: 2.0
Date: July 6, 2025
"""

import argparse
import sys
import unittest


def run_all_tests(verbose=False):
    """Run all test suites."""
    test_modules = ["test_codeweaver_bot", "test_security_performance"]

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module_name in test_modules:
        try:
            module = __import__(module_name)
            module_suite = loader.loadTestsFromModule(module)
            suite.addTests(module_suite)
        except ImportError as e:
            print(f"Warning: Could not import {module_name}: {e}")

    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    result = runner.run(suite)

    return result


def run_security_tests_only(verbose=False):
    """Run only security and performance tests."""
    try:
        import test_security_performance

        loader = unittest.TestLoader()
        suite = loader.loadTestsFromModule(test_security_performance)

        verbosity = 2 if verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)

        return result
    except ImportError as e:
        print(f"Error: Could not import security tests: {e}")
        return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run CodeWeaverBot tests")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Run tests with verbose output"
    )
    parser.add_argument(
        "--security-only",
        "-s",
        action="store_true",
        help="Run only security and performance tests",
    )

    args = parser.parse_args()

    print("CodeWeaverBot Test Suite")
    print("=" * 50)

    if args.security_only:
        print("Running security and performance tests only...")
        result = run_security_tests_only(args.verbose)
    else:
        print("Running all tests...")
        result = run_all_tests(args.verbose)

    if result is None:
        print("Failed to run tests due to import errors.")
        sys.exit(1)

    print(f"\n{'='*50}")
    print("Final Results:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed.")
        if result.failures:
            print(f"\nFailures ({len(result.failures)}):")
            for test, _ in result.failures:
                print(f"  - {test}")

        if result.errors:
            print(f"\nErrors ({len(result.errors)}):")
            for test, _ in result.errors:
                print(f"  - {test}")

        sys.exit(1)


if __name__ == "__main__":
    main()
