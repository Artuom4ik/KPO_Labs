#!/usr/bin/env python
"""
Script to build and install the calculator libraries.
"""

import os
import sys
import shutil
import subprocess

def build_static_library():
    """
    Build the static calculator library.
    """
    print("Building static calculator library...")
    os.chdir("calculator_lib")
    
    # Create the build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # Build the library
    subprocess.run([sys.executable, "setup.py", "build"], check=True)
    
    # Copy the library files to the build directory
    src_dir = os.path.join("build", "lib")
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join("build", item)
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
    
    print("Static library built successfully.")
    os.chdir("..")

def build_dynamic_library():
    """
    Build the dynamic developer information library.
    """
    print("Building dynamic developer information library...")
    os.chdir("developer_lib")
    
    # Create the build directory if it doesn't exist
    if not os.path.exists("build"):
        os.makedirs("build")
    
    # Build the library
    subprocess.run([sys.executable, "setup.py", "build"], check=True)
    
    # Copy the library files to the build directory
    src_dir = os.path.join("build", "lib")
    if os.path.exists(src_dir):
        for item in os.listdir(src_dir):
            src_path = os.path.join(src_dir, item)
            dst_path = os.path.join("build", item)
            if os.path.isdir(src_path):
                if os.path.exists(dst_path):
                    shutil.rmtree(dst_path)
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)
    
    print("Dynamic library built successfully.")
    os.chdir("..")

def install_libraries():
    """
    Install the libraries to the site-packages directory.
    """
    print("Installing libraries...")
    
    # Install the calculator library
    os.chdir("calculator_lib")
    subprocess.run([sys.executable, "setup.py", "install"], check=True)
    os.chdir("..")
    
    # Install the developer information library
    os.chdir("developer_lib")
    subprocess.run([sys.executable, "setup.py", "install"], check=True)
    os.chdir("..")
    
    print("Libraries installed successfully.")

def copy_to_desktop():
    """
    Copy the main_refactored.py file to the desktop.
    """
    print("Copying main_refactored.py to the desktop...")
    
    # Get the desktop path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # Copy the main_refactored.py file to the desktop
    shutil.copy2("main_refactored.py", os.path.join(desktop_path, "calculator.py"))
    
    print("main_refactored.py copied to the desktop as calculator.py.")

def main():
    """
    Main function to build and install the libraries.
    """
    print("Starting library build process...")
    
    # Build the static library
    build_static_library()
    
    # Build the dynamic library
    build_dynamic_library()
    
    # Install the libraries
    install_libraries()
    
    # Copy the main_refactored.py file to the desktop
    copy_to_desktop()
    
    print("Library build process completed successfully.")

if __name__ == "__main__":
    main() 