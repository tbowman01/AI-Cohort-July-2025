"""
Test runner script for AutoDevHub backend tests.

This script provides utilities for running tests with different configurations,
generating coverage reports, and validating test results.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term",
        "--cov-report=xml",
        "--cov-fail-under=80",
        "-v",
    ]

    print("Running tests with coverage...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("STDOUT:")
    print(result.stdout)

    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    return result.returncode == 0


def run_specific_test_file(filename):
    """Run tests from a specific file."""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    cmd = ["python", "-m", "pytest", f"tests/{filename}", "-v"]

    print(f"Running tests from {filename}...")
    result = subprocess.run(cmd)
    return result.returncode == 0


def run_tests_by_marker(marker):
    """Run tests with specific marker."""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    cmd = ["python", "-m", "pytest", "tests/", "-m", marker, "-v"]

    print(f"Running tests with marker '{marker}'...")
    result = subprocess.run(cmd)
    return result.returncode == 0


def run_performance_tests():
    """Run only performance tests."""
    return run_tests_by_marker("performance")


def run_integration_tests():
    """Run only integration tests."""
    return run_tests_by_marker("integration")


def run_unit_tests():
    """Run only unit tests."""
    return run_tests_by_marker("unit")


def run_database_tests():
    """Run only database-related tests."""
    return run_tests_by_marker("database")


def run_ai_service_tests():
    """Run only AI service tests."""
    return run_tests_by_marker("ai_service")


def validate_test_environment():
    """Validate that the test environment is properly set up."""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    print("Validating test environment...")

    # Check if required files exist
    required_files = [
        "main.py",
        "config.py",
        "models.py",
        "database.py",
        "dependencies.py",
        "routers/stories.py",
        "tests/conftest.py",
    ]

    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)

    if missing_files:
        print(f"Missing required files: {missing_files}")
        return False

    # Check if pytest and dependencies are installed
    try:
        subprocess.run(
            ["python", "-m", "pytest", "--version"], capture_output=True, check=True
        )
        print("✓ pytest is available")
    except subprocess.CalledProcessError:
        print("✗ pytest is not available")
        return False

    try:
        subprocess.run(
            ["python", "-c", "import fastapi"], capture_output=True, check=True
        )
        print("✓ FastAPI is available")
    except subprocess.CalledProcessError:
        print("✗ FastAPI is not available")
        return False

    try:
        subprocess.run(
            ["python", "-c", "import sqlalchemy"], capture_output=True, check=True
        )
        print("✓ SQLAlchemy is available")
    except subprocess.CalledProcessError:
        print("✗ SQLAlchemy is not available")
        return False

    print("Test environment validation passed!")
    return True


def generate_test_report():
    """Generate a comprehensive test report."""
    backend_dir = Path(__file__).parent.parent
    os.chdir(backend_dir)

    print("Generating comprehensive test report...")

    cmd = [
        "python",
        "-m",
        "pytest",
        "tests/",
        "--cov=.",
        "--cov-report=html:htmlcov",
        "--cov-report=term-missing",
        "--junit-xml=test-results.xml",
        "--html=test-report.html",
        "--self-contained-html",
        "-v",
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print("\n✓ Test report generated successfully!")
        print("  - Coverage HTML report: htmlcov/index.html")
        print("  - Test HTML report: test-report.html")
        print("  - JUnit XML report: test-results.xml")
    else:
        print("\n✗ Test report generation failed!")

    return result.returncode == 0


def main():
    """Main CLI interface for running tests."""
    parser = argparse.ArgumentParser(description="AutoDevHub Backend Test Runner")
    parser.add_argument(
        "--coverage", action="store_true", help="Run tests with coverage reporting"
    )
    parser.add_argument(
        "--file", type=str, help="Run tests from specific file (e.g., test_main.py)"
    )
    parser.add_argument("--marker", type=str, help="Run tests with specific marker")
    parser.add_argument(
        "--performance", action="store_true", help="Run only performance tests"
    )
    parser.add_argument(
        "--integration", action="store_true", help="Run only integration tests"
    )
    parser.add_argument("--unit", action="store_true", help="Run only unit tests")
    parser.add_argument(
        "--database", action="store_true", help="Run only database tests"
    )
    parser.add_argument(
        "--ai-service", action="store_true", help="Run only AI service tests"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate test environment"
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate comprehensive test report"
    )

    args = parser.parse_args()

    if args.validate:
        success = validate_test_environment()
        sys.exit(0 if success else 1)

    if args.report:
        success = generate_test_report()
        sys.exit(0 if success else 1)

    if args.coverage:
        success = run_tests_with_coverage()
    elif args.file:
        success = run_specific_test_file(args.file)
    elif args.marker:
        success = run_tests_by_marker(args.marker)
    elif args.performance:
        success = run_performance_tests()
    elif args.integration:
        success = run_integration_tests()
    elif args.unit:
        success = run_unit_tests()
    elif args.database:
        success = run_database_tests()
    elif args.ai_service:
        success = run_ai_service_tests()
    else:
        # Default: run all tests
        success = run_tests_with_coverage()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
