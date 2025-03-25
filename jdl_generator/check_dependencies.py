import os
import subprocess
import sys
import importlib

def check_and_install_dependencies():
    """Check if required packages are installed and install them if needed."""
    requirements_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "requirements.txt"
    )
    
    if not os.path.exists(requirements_path):
        print("Creating requirements.txt file...")
        with open(requirements_path, "w") as f:
            f.write("pandas>=1.3.0\nopenpyxl>=3.0.0\n")
    
    # Read requirements file
    with open(requirements_path, "r") as f:
        requirements = [line.strip() for line in f if line.strip()]
    
    # Check which packages need to be installed
    missing_packages = []
    for requirement in requirements:
        # Skip empty lines and comments
        if not requirement or requirement.startswith('#'):
            continue
        
        # Parse requirement name (without version)
        package_name = requirement.split('>=')[0].split('==')[0].split('<')[0].strip()
        
        try:
            importlib.import_module(package_name)
            print(f"✓ {package_name} is already installed")
        except ImportError:
            missing_packages.append(requirement)
            print(f"✗ {package_name} needs to be installed")
    
    # Install missing packages
    if missing_packages:
        print("\nInstalling missing dependencies...")
        python_executable = sys.executable
        subprocess.check_call([
            python_executable, "-m", "pip", "install", *missing_packages
        ])
        print("All dependencies installed successfully!\n")
    else:
        print("All required dependencies are already installed.\n")

if __name__ == "__main__":
    print("Checking dependencies...")
    check_and_install_dependencies()
