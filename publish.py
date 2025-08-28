#!/usr/bin/env python3
"""
Publishing helper script for CosmicExcuse package.
This script helps automate the publishing process to PyPI.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class Color:
    """Terminal colors."""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_step(message):
    """Print a step message."""
    print(f"\n{Color.OKCYAN}📌 {message}{Color.ENDC}")


def print_success(message):
    """Print a success message."""
    print(f"{Color.OKGREEN}✅ {message}{Color.ENDC}")


def print_error(message):
    """Print an error message."""
    print(f"{Color.FAIL}❌ {message}{Color.ENDC}")


def print_warning(message):
    """Print a warning message."""
    print(f"{Color.WARNING}⚠️  {message}{Color.ENDC}")


def run_command(command, check=True):
    """Run a shell command."""
    print(f"  Running: {command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if check and result.returncode != 0:
        print_error(f"Command failed: {command}")
        print(f"Error: {result.stderr}")
        return False

    return True


def check_prerequisites():
    """Check if all prerequisites are met."""
    print_step("Checking prerequisites...")

    # Check Python version
    if sys.version_info < (3, 9):
        print_error("Python 3.9+ is required")
        return False
    print_success(f"Python {sys.version.split()[0]} ✓")

    # Check required tools
    tools = {
        "pip": "pip --version",
        "twine": "twine --version",
        "black": "black --version",
        "flake8": "flake8 --version",
        "pytest": "pytest --version"
    }

    for tool, command in tools.items():
        if not run_command(command, check=False):
            print_warning(f"{tool} not found. Installing...")
            if not run_command(f"pip install {tool}", check=False):
                print_error(f"Failed to install {tool}")
                return False
        else:
            print_success(f"{tool} ✓")

    return True


def clean_build():
    """Clean build directories."""
    print_step("Cleaning build directories...")

    dirs_to_clean = ["build", "dist", "*.egg-info", "__pycache__"]

    for dir_pattern in dirs_to_clean:
        for path in Path(".").glob(dir_pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed {path}")
            else:
                path.unlink()
                print(f"  Removed {path}")

    print_success("Build directories cleaned")
    return True


def run_tests():
    """Run tests."""
    print_step("Running tests...")

    if not run_command("pytest tests/ -v"):
        print_error("Tests failed")
        return False

    print_success("All tests passed")
    return True


def check_code_quality():
    """Check code quality."""
    print_step("Checking code quality...")

    # Black formatting check
    if not run_command("black cosmicexcuse tests --check", check=False):
        print_warning("Code not formatted with black")
        response = input("  Format code now? (y/n): ")
        if response.lower() == 'y':
            run_command("black cosmicexcuse tests")
            print_success("Code formatted")
    else:
        print_success("Black formatting ✓")

    # Flake8 linting
    if not run_command("flake8 cosmicexcuse tests --max-line-length=88", check=False):
        print_warning("Flake8 found issues")
    else:
        print_success("Flake8 linting ✓")

    # MyPy type checking
    if not run_command("mypy cosmicexcuse --ignore-missing-imports", check=False):
        print_warning("MyPy found type issues")
    else:
        print_success("MyPy type checking ✓")

    return True


def update_version():
    """Update version number."""
    print_step("Checking version...")

    version_file = Path("cosmicexcuse/__version__.py")
    current_version = None

    # Read current version
    with open(version_file, 'r') as f:
        for line in f:
            if "__version__" in line:
                current_version = line.split('"')[1]
                break

    print(f"  Current version: {current_version}")

    response = input("  Enter new version (or press Enter to keep current): ")
    if response:
        # Update version file
        content = version_file.read_text()
        content = content.replace(f'"{current_version}"', f'"{response}"')
        version_file.write_text(content)

        # Update setup.py if it exists
        setup_file = Path("setup.py")
        if setup_file.exists():
            setup_content = setup_file.read_text()
            setup_content = setup_content.replace(
                f"version=version['__version__']",
                f"version=version['__version__']"
            )
            setup_file.write_text(setup_content)

        # Update pyproject.toml
        pyproject_file = Path("pyproject.toml")
        if pyproject_file.exists():
            pyproject_content = pyproject_file.read_text()
            pyproject_content = pyproject_content.replace(
                f'version = "{current_version}"',
                f'version = "{response}"'
            )
            pyproject_file.write_text(pyproject_content)

        print_success(f"Version updated to {response}")
        return response

    return current_version


def build_package():
    """Build the package."""
    print_step("Building package...")

    if not run_command("python -m build"):
        print_error("Build failed")
        return False

    print_success("Package built successfully")

    # List built files
    dist_files = list(Path("dist").glob("*"))
    print("  Built files:")
    for file in dist_files:
        print(f"    - {file}")

    return True


def check_package():
    """Check package with twine."""
    print_step("Checking package...")

    if not run_command("twine check dist/*"):
        print_error("Package check failed")
        return False

    print_success("Package check passed")
    return True


def test_installation():
    """Test package installation."""
    print_step("Testing installation...")

    # Create temporary virtual environment
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        venv_path = Path(tmpdir) / "test_venv"

        print("  Creating test virtual environment...")
        if not run_command(f"python -m venv {venv_path}"):
            print_error("Failed to create test environment")
            return False

        # Install package
        pip_path = venv_path / "bin" / "pip" if os.name != 'nt' else venv_path / "Scripts" / "pip.exe"
        wheel_file = list(Path("dist").glob("*.whl"))[0]

        print(f"  Installing {wheel_file}...")
        if not run_command(f"{pip_path} install {wheel_file}"):
            print_error("Installation failed")
            return False

        # Test import
        python_path = venv_path / "bin" / "python" if os.name != 'nt' else venv_path / "Scripts" / "python.exe"
        test_code = "from cosmicexcuse import CosmicExcuse; print(CosmicExcuse().generate().text[:50])"

        if not run_command(f'{python_path} -c "{test_code}"'):
            print_error("Import test failed")
            return False

    print_success("Installation test passed")
    return True


def upload_to_testpypi():
    """Upload to TestPyPI."""
    print_step("Uploading to TestPyPI...")

    print_warning("Make sure you have configured ~/.pypirc with TestPyPI credentials")
    response = input("  Continue with TestPyPI upload? (y/n): ")

    if response.lower() != 'y':
        print("  Skipping TestPyPI upload")
        return True

    if not run_command("twine upload --repository testpypi dist/*"):
        print_error("TestPyPI upload failed")
        return False

    print_success("Package uploaded to TestPyPI")
    print("  Test installation with:")
    print("    pip install --index-url https://test.pypi.org/simple/ cosmicexcuse")

    return True


def upload_to_pypi():
    """Upload to PyPI."""
    print_step("Uploading to PyPI...")

    print_warning("⚠️  This will upload to the REAL PyPI!")
    print_warning("Make sure you have:")
    print("  1. Tested on TestPyPI")
    print("  2. Configured ~/.pypirc with PyPI credentials")
    print("  3. Committed and tagged the release")

    response = input("\n  Continue with PyPI upload? (yes/no): ")

    if response.lower() != 'yes':
        print("  Cancelled PyPI upload")
        return False

    if not run_command("twine upload dist/*"):
        print_error("PyPI upload failed")
        return False

    print_success("🎉 Package uploaded to PyPI!")
    print("  Install with: pip install cosmicexcuse")

    return True


def create_git_tag(version):
    """Create git tag for the release."""
    print_step("Creating git tag...")

    response = input(f"  Create git tag v{version}? (y/n): ")
    if response.lower() == 'y':
        run_command(f"git tag -a v{version} -m 'Release version {version}'")
        print_success(f"Tag v{version} created")
        print("  Push with: git push origin v{version}")

    return True


def main():
    """Main publishing workflow."""
    print(f"\n{Color.HEADER}{Color.BOLD}🚀 CosmicExcuse Publishing Script{Color.ENDC}")
    print("=" * 50)

    steps = [
        ("Prerequisites", check_prerequisites),
        ("Clean build", clean_build),
        ("Run tests", run_tests),
        ("Code quality", check_code_quality),
        ("Update version", update_version),
        ("Build package", build_package),
        ("Check package", check_package),
        ("Test installation", test_installation),
        ("Upload to TestPyPI", upload_to_testpypi),
    ]

    version = None

    for step_name, step_func in steps:
        if step_name == "Update version":
            result = step_func()
            if result:
                version = result
            else:
                print_error(f"Step failed: {step_name}")
                return 1
        else:
            if not step_func():
                print_error(f"Step failed: {step_name}")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    return 1

    print("\n" + "=" * 50)
    print_success("All checks passed!")
    print("\nNext steps:")
    print("1. Upload to PyPI (production)")
    print("2. Create git tag")
    print("3. Create GitHub release")

    response = input("\nContinue with PyPI upload? (y/n): ")
    if response.lower() == 'y':
        if upload_to_pypi():
            create_git_tag(version)

    print(f"\n{Color.OKGREEN}🎉 Publishing complete!{Color.ENDC}")
    print("\nPost-publishing checklist:")
    print("  [ ] Verify package on PyPI")
    print("  [ ] Test installation: pip install cosmicexcuse")
    print("  [ ] Push git tag: git push origin v{version}")
    print("  [ ] Create GitHub release")
    print("  [ ] Update documentation")
    print("  [ ] Announce on social media")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nCancelled by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
