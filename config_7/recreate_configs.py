"""
Script to recreate all configuration files.
This script deletes all existing configuration files and recreates them with the default values.
"""

import os
import shutil
import sys
from config_manager import ConfigManager

def main():
    print(f"Python version: {sys.version}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Get the directory of this script file
    base_dir = os.path.dirname(os.path.abspath(__file__))
    configs_dir = os.path.join(base_dir, "configs")
    
    print(f"Base directory: {base_dir}")
    print(f"Configs directory: {configs_dir}")
    
    # Check if configs directory exists
    if os.path.exists(configs_dir):
        print(f"Deleting existing configs directory: {configs_dir}")
        shutil.rmtree(configs_dir)
        print("Directory deleted")
    
    # Create a new configuration manager, which will create the default configs
    print("Creating new configuration manager")
    config_manager = ConfigManager()
    
    # List all configuration files
    if os.path.exists(configs_dir):
        config_files = [f for f in os.listdir(configs_dir) if f.endswith('.json')]
        print(f"Created {len(config_files)} configuration files: {config_files}")
    else:
        print("ERROR: Configs directory was not created")
    
    print("Configuration files recreation complete")
    
if __name__ == "__main__":
    main() 