import subprocess
import sys

# Function to install a package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
required_packages = [
    "requests",
    "beautifulsoup4",
    "mimetypes",
    "logging"
]

# Iterate over the required packages and install each one
for package in required_packages:
    try:
        install(package)
        print(f"Successfully installed {package}")
    except Exception as e:
        print(f"Failed to install {package}: {e}")
