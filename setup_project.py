"""
Run this script to perform initial setup and validation of the project.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True


def check_virtual_env():
    """Check if running in a virtual environment."""
    print("\nChecking virtual environment...")
    in_venv = hasattr(sys, 'real_prefix') or (
        hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
    )
    if not in_venv:
        print("⚠ Not running in a virtual environment!")
        print("Recommendation: Create and activate a virtual environment")
        print("  python -m venv venv")
        print("  .\\venv\\Scripts\\Activate.ps1")
        return False
    print("✓ Virtual environment detected")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\nInstalling dependencies...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def run_tests():
    """Run the test suite."""
    print("\nRunning tests...")
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "-v"], 
                              capture_output=False)
        if result.returncode == 0:
            print("✓ All tests passed")
            return True
        else:
            print("⚠ Some tests failed")
            return False
    except FileNotFoundError:
        print("⚠ pytest not found, skipping tests")
        return True


def create_example_config():
    """Create an example configuration file."""
    print("\nCreating example configuration...")
    config_path = Path("example_config.yaml")
    if not config_path.exists():
        from src.config_loader import ConfigLoader
        ConfigLoader.create_default_config(str(config_path))
        print(f"✓ Example config created: {config_path}")
    else:
        print("✓ Example config already exists")
    return True


def print_next_steps():
    """Print next steps for the user."""
    print("\n" + "="*60)
    print("Setup Complete! Next Steps:")
    print("="*60)
    print("\n1. Try a dry run:")
    print("   python -m src.cli organize --dry-run")
    print("\n2. Organize your Downloads folder:")
    print("   python -m src.cli organize")
    print("\n3. Check for duplicates:")
    print("   python -m src.cli clean-duplicates --report-only")
    print("\n4. View documentation:")
    print("   docs/QUICKSTART.md")
    print("   docs/INSTRUKCJA_PL.md (Polish)")
    print("\n5. Customize configuration:")
    print("   Edit example_config.yaml")
    print("   python -m src.cli organize -c example_config.yaml")
    print("\n" + "="*60)


def main():
    """Main setup function."""
    print("="*60)
    print("Auto Download Organizer - Setup Script")
    print("="*60)
    
    steps = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_env),
        ("Dependencies", install_dependencies),
        ("Tests", run_tests),
        ("Example Config", create_example_config),
    ]
    
    results = []
    for name, func in steps:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*60)
    print("Setup Summary:")
    print("="*60)
    for name, result in results:
        status = "✓" if result else "❌"
        print(f"{status} {name}")
    
    if all(result for _, result in results):
        print("\n✓ Setup completed successfully!")
        print_next_steps()
    else:
        print("\n⚠ Setup completed with warnings")
        print("Please review the messages above")


if __name__ == "__main__":
    main()
