import json
import os
from tkinter import messagebox
import traceback

import customtkinter as ctk


class ConfigManager:
    def __init__(self, config_file="config.json"):
        # Get the directory of this script file
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.configs_dir = os.path.join(self.base_dir, "configs")
        
        # Ensure the configs directory exists
        os.makedirs(self.configs_dir, exist_ok=True)
        
        # Create default configs if they don't exist
        self._create_default_configs()
        
        # Determine if this is a custom config path (skip last config override)
        self.skip_last_override = ('/' in config_file) or ('\\' in config_file)

        # Check if config_file is a relative path without directory
        if "/" not in config_file and "\\" not in config_file:
            self.config_file = os.path.join(self.configs_dir, config_file)
        else:
            self.config_file = config_file
            
        self.config = None
        self.last_config_path_file = os.path.join(self.configs_dir, "last_config.txt")
        self.default_config = {
            "window": {
                "width": 400,
                "height": 600,
                "title": "Calculator"
            },
            "appearance": {
                "mode": "system",
                "color_theme": "green",
                "background_color": "#2b2b2b",
                "text_color": "#ffffff",
                "button_color": "#1f538d",
                "button_hover_color": "#326ca8"
            },
            "font": {
                "family": "Arial",
                "size": 24,
                "button_size": 20
            },
            "database": {
                "enabled": False,
                "host": "localhost",
                "port": 3306,
                "username": "root",
                "password": "",
                "database_name": "calculator_db"
            },
            "interface_type": {
                "type": "default",
                "variant": "default"
            }
        }
        
        # Try to load the last used configuration (unless custom path)
        if not self.skip_last_override:
            self._load_last_config()

    def _create_default_configs(self):
        """Create default configuration files if they don't exist."""
        # Define all the configuration presets
        configs = {
            "config.json": {
                "window": {"width": 400, "height": 600, "title": "Calculator"},
                "appearance": {
                    "mode": "system", 
                    "color_theme": "green",
                    "background_color": "#2b2b2b",
                    "text_color": "#ffffff",
                    "button_color": "#1f538d",
                    "button_hover_color": "#326ca8"
                },
                "font": {"family": "Arial", "size": 24, "button_size": 20},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "default", "variant": "default"}
            },
            "config_accessibility_high_contrast.json": {
                "window": {"width": 500, "height": 700, "title": "High Contrast Calculator"},
                "appearance": {
                    "mode": "dark", 
                    "color_theme": "dark-blue",
                    "background_color": "#000000",
                    "text_color": "#FFFF00",
                    "button_color": "#000080",
                    "button_hover_color": "#0000CD"
                },
                "font": {"family": "Arial", "size": 28, "button_size": 24},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "accessibility", "variant": "high_contrast"}
            },
            "config_accessibility_light.json": {
                "window": {"width": 500, "height": 700, "title": "Accessible Calculator"},
                "appearance": {
                    "mode": "light", 
                    "color_theme": "blue",
                    "background_color": "#ffffff",
                    "text_color": "#000000",
                    "button_color": "#4682B4",
                    "button_hover_color": "#6495ED"
                },
                "font": {"family": "Arial", "size": 28, "button_size": 24},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "accessibility", "variant": "light"}
            },
            "config_gender_male.json": {
                "window": {"width": 400, "height": 600, "title": "Calculator - Male Style"},
                "appearance": {
                    "mode": "dark", 
                    "color_theme": "blue",
                    "background_color": "#1a1a2e",
                    "text_color": "#ffffff",
                    "button_color": "#0047AB",
                    "button_hover_color": "#00008B"
                },
                "font": {"family": "Arial", "size": 24, "button_size": 20},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "gender", "variant": "male"}
            },
            "config_gender_female.json": {
                "window": {"width": 400, "height": 600, "title": "Calculator - Female Style"},
                "appearance": {
                    "mode": "light", 
                    "color_theme": "blue",
                    "background_color": "#fff0f5",
                    "text_color": "#333333",
                    "button_color": "#FF69B4",
                    "button_hover_color": "#FF1493"
                },
                "font": {"family": "Arial", "size": 24, "button_size": 20},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "gender", "variant": "female"}
            },
            "config_age_children.json": {
                "window": {"width": 450, "height": 650, "title": "Kid's Calculator"},
                "appearance": {
                    "mode": "light", 
                    "color_theme": "green",
                    "background_color": "#e6f7ff",
                    "text_color": "#333333",
                    "button_color": "#32CD32",
                    "button_hover_color": "#00FF00"
                },
                "font": {"family": "Comic Sans MS", "size": 26, "button_size": 22},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "age", "variant": "children"}
            },
            "config_age_youth.json": {
                "window": {"width": 400, "height": 600, "title": "Modern Calculator"},
                "appearance": {
                    "mode": "dark", 
                    "color_theme": "blue",
                    "background_color": "#121212",
                    "text_color": "#ffffff",
                    "button_color": "#1E90FF",
                    "button_hover_color": "#00BFFF"
                },
                "font": {"family": "Arial", "size": 24, "button_size": 20},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "age", "variant": "youth"}
            },
            "config_age_middle.json": {
                "window": {"width": 420, "height": 620, "title": "Professional Calculator"},
                "appearance": {
                    "mode": "system", 
                    "color_theme": "green",
                    "background_color": "#2b2b2b",
                    "text_color": "#ffffff",
                    "button_color": "#006400",
                    "button_hover_color": "#008000"
                },
                "font": {"family": "Arial", "size": 24, "button_size": 20},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "age", "variant": "middle_age"}
            },
            "config_age_elderly.json": {
                "window": {"width": 550, "height": 750, "title": "Large Print Calculator"},
                "appearance": {
                    "mode": "light", 
                    "color_theme": "dark-blue",
                    "background_color": "#f5f5f5",
                    "text_color": "#000000",
                    "button_color": "#4169E1",
                    "button_hover_color": "#6495ED"
                },
                "font": {"family": "Arial", "size": 32, "button_size": 28},
                "database": {
                    "enabled": False,
                    "host": "localhost",
                    "port": 3306,
                    "username": "root",
                    "password": "",
                    "database_name": "calculator_db"
                },
                "interface_type": {"type": "age", "variant": "elderly"}
            }
        }
        
        # Create each configuration file if it doesn't exist
        for filename, config in configs.items():
            filepath = os.path.join(self.configs_dir, filename)
            if not os.path.exists(filepath):
                print(f"Creating default configuration file: {filepath}")
                try:
                    with open(filepath, 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=2)
                except Exception as e:
                    print(f"Error creating configuration file {filename}: {str(e)}")
                    traceback.print_exc()

    def _load_last_config(self):
        """Load the last used configuration file path."""
        try:
            if os.path.exists(self.last_config_path_file):
                with open(self.last_config_path_file, 'r', encoding='utf-8') as file:
                    last_config_path = file.read().strip()
                    print(f"Last config path from file: {last_config_path}")
                    if last_config_path and os.path.exists(last_config_path):
                        self.config_file = last_config_path
                        print(f"Using last config path: {self.config_file}")
                    elif os.path.exists(os.path.join(self.configs_dir, os.path.basename(last_config_path))):
                        # Try to find the file in the configs directory
                        self.config_file = os.path.join(self.configs_dir, os.path.basename(last_config_path))
                        print(f"Using last config from configs dir: {self.config_file}")
                    else:
                        print(f"Last config file not found, using default: {self.config_file}")
            else:
                print(f"Last config file not found at {self.last_config_path_file}, using default")
        except Exception as e:
            print(f"Error loading last config: {str(e)}")
            traceback.print_exc()
            # If there's any error, just use the default config file

    def _save_last_config(self):
        """Save the current configuration file path as the last used one."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.last_config_path_file), exist_ok=True)
            
            with open(self.last_config_path_file, 'w', encoding='utf-8') as file:
                file.write(self.config_file)
            print(f"Saved last config path: {self.config_file}")
        except Exception as e:
            print(f"Error saving last config: {str(e)}")
            traceback.print_exc()
            # If there's any error, just continue without saving

    def load_config(self):
        """
        Load configuration from file.
        If file doesn't exist or is invalid, use default configuration.
        """
        print(f"Loading configuration from: {self.config_file}")
        try:
            if os.path.exists(self.config_file):
                print(f"Config file exists: {self.config_file}")
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    self.config = json.load(file)
                
                # Validate config structure
                if not self._validate_config():
                    print("Config validation failed")
                    messagebox.showerror("Configuration Error", 
                                        "Configuration file is invalid. Using default configuration.")
                    self.config = self.default_config
                    self.config_file = os.path.join(self.configs_dir, "config.json")
                else:
                    print("Config validation passed")
                    # Save this as the last used config
                    self._save_last_config()
                    print(f"Loaded configuration from {self.config_file}")
                    print(f"Config content: {self.config}")
            else:
                print(f"Config file does not exist: {self.config_file}")
                messagebox.showwarning("Configuration Warning", 
                                      f"Configuration file '{self.config_file}' not found. Using default configuration.")
                self.config = self.default_config
                self.config_file = os.path.join(self.configs_dir, "config.json")
                
                # Create default config file
                self.save_config()
                
            return True
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Configuration Error", 
                                f"Error parsing configuration file: {str(e)}. Using default configuration.")
            self.config = self.default_config
            self.config_file = os.path.join(self.configs_dir, "config.json")
            return False
        except Exception as e:
            print(f"Error loading configuration: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Configuration Error", 
                                f"Error loading configuration: {str(e)}. Using default configuration.")
            self.config = self.default_config
            self.config_file = os.path.join(self.configs_dir, "config.json")
            return False

    def save_config(self):
        """Save current configuration to file."""
        print(f"Saving configuration to: {self.config_file}")
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(self.config, file, indent=2)
            
            # Save this as the last used config
            self._save_last_config()
            print(f"Saved configuration to {self.config_file}")
            return True
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
            traceback.print_exc()
            messagebox.showerror("Configuration Error", f"Error saving configuration: {str(e)}")
            return False

    def _validate_config(self):
        """Validate configuration structure."""
        required_sections = ["window", "appearance", "font", "interface_type"]
        for section in required_sections:
            if section not in self.config:
                print(f"Missing required section: {section}")
                return False
                
        # Validate window settings
        if "width" not in self.config["window"] or "height" not in self.config["window"]:
            print("Missing window dimensions")
            return False
            
        # Validate appearance settings
        if "mode" not in self.config["appearance"] or "color_theme" not in self.config["appearance"]:
            print("Missing appearance settings")
            return False
            
        # Validate font settings
        if "family" not in self.config["font"] or "size" not in self.config["font"]:
            print("Missing font settings")
            return False
            
        return True

    def apply_config(self, app):
        """Apply configuration to the application."""
        print("Applying configuration to application")
        if not self.config:
            print("No config loaded, loading now")
            self.load_config()
            
        # Apply window settings
        print(f"Setting window geometry: {self.config['window']['width']}x{self.config['window']['height']}")
        app.geometry(f"{self.config['window']['width']}x{self.config['window']['height']}")
        app.title(self.config['window']['title'])
        
        # Apply appearance settings
        print(f"Setting appearance mode: {self.config['appearance']['mode']}")
        print(f"Setting color theme: {self.config['appearance']['color_theme']}")
        ctk.set_appearance_mode(self.config['appearance']['mode'])
        ctk.set_default_color_theme(self.config['appearance']['color_theme'])
        
        # Set background color for the main window if possible
        try:
            print(f"Setting background color: {self.config['appearance']['background_color']}")
            app.configure(fg_color=self.config['appearance']['background_color'])
        except Exception as e:
            print(f"Error setting background color: {str(e)}")
            
        # Apply interface type settings
        self._apply_interface_type(app)
        
        return True
        
    def _apply_interface_type(self, app):
        """Apply interface type specific settings."""
        interface_type = self.config['interface_type']['type']
        variant = self.config['interface_type']['variant']
        print(f"Applying interface type: {interface_type}, variant: {variant}")
        
        # For accessibility interface type
        if interface_type == "accessibility":
            if variant == "high_contrast":
                print("Applying high contrast settings")
                self.config['appearance']['background_color'] = "#000000"
                self.config['appearance']['text_color'] = "#FFFF00"  # Yellow text for better contrast
                self.config['font']['size'] = 28
                self.config['font']['button_size'] = 24
            elif variant == "light":
                print("Applying light accessibility settings")
                self.config['appearance']['background_color'] = "#ffffff"
                self.config['appearance']['text_color'] = "#000000"
                self.config['font']['size'] = 28
                self.config['font']['button_size'] = 24
                
        # For gender-specific interface
        elif interface_type == "gender":
            if variant == "male":
                print("Applying male style settings")
                self.config['appearance']['color_theme'] = "blue"
                self.config['appearance']['button_color'] = "#0047AB"
            elif variant == "female":
                print("Applying female style settings")
                self.config['appearance']['color_theme'] = "blue"  # Changed from pink to blue
                self.config['appearance']['button_color'] = "#FF69B4"
                
        # For age-specific interface
        elif interface_type == "age":
            if variant == "children":
                print("Applying children style settings")
                self.config['appearance']['color_theme'] = "green"
                self.config['appearance']['button_color'] = "#32CD32"
                self.config['font']['family'] = "Comic Sans MS"
            elif variant == "youth":
                print("Applying youth style settings")
                self.config['appearance']['color_theme'] = "blue"
                self.config['appearance']['button_color'] = "#1E90FF"
            elif variant == "middle_age":
                print("Applying middle age style settings")
                self.config['appearance']['color_theme'] = "green"
                self.config['appearance']['button_color'] = "#006400"
            elif variant == "elderly":
                print("Applying elderly style settings")
                self.config['appearance']['color_theme'] = "dark-blue"
                self.config['font']['size'] = 32
                self.config['font']['button_size'] = 28 