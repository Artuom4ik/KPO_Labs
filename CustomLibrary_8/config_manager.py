import json
import os
from tkinter import messagebox
import traceback

import customtkinter as ctk


class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.configs_dir = os.path.join(self.base_dir, "configs")
        
        os.makedirs(self.configs_dir, exist_ok=True)
        
        self.skip_last_override = ('/' in config_file) or ('\\' in config_file)

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
        
        if not self.skip_last_override:
            self._load_last_config()

    def _load_last_config(self):
        """Load the last used configuration file path."""
        try:
            if os.path.exists(self.last_config_path_file):
                with open(self.last_config_path_file, 'r', encoding='utf-8') as file:
                    last_config_path = file.read().strip()
                    if last_config_path and os.path.exists(last_config_path):
                        self.config_file = last_config_path
                    elif os.path.exists(os.path.join(self.configs_dir, os.path.basename(last_config_path))):
                        self.config_file = os.path.join(self.configs_dir, os.path.basename(last_config_path))

        except Exception as e:
            traceback.print_exc()

    def _save_last_config(self):
        """Save the current configuration file path as the last used one."""
        try:
            os.makedirs(os.path.dirname(self.last_config_path_file), exist_ok=True)
            
            with open(self.last_config_path_file, 'w', encoding='utf-8') as file:
                file.write(self.config_file)
        except Exception as e:
            traceback.print_exc()

    def load_config(self):
        """
        Load configuration from file.
        If file doesn't exist or is invalid, use default configuration.
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as file:
                    self.config = json.load(file)
                
                if not self._validate_config():
                    messagebox.showerror("Configuration Error", 
                                        "Configuration file is invalid. Using default configuration.")
                    self.config = self.default_config
                    self.config_file = os.path.join(self.configs_dir, "config.json")
                else:
                    self._save_last_config()
            else:
                messagebox.showwarning("Configuration Warning", 
                                      f"Configuration file '{self.config_file}' not found. Using default configuration.")
                self.config = self.default_config
                self.config_file = os.path.join(self.configs_dir, "config.json")
                
                self.save_config()
                
            return True
        except json.JSONDecodeError as e:
            traceback.print_exc()
            messagebox.showerror("Configuration Error", 
                                f"Error parsing configuration file: {str(e)}. Using default configuration.")
            self.config = self.default_config
            self.config_file = os.path.join(self.configs_dir, "config.json")
            return False
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Configuration Error", 
                                f"Error loading configuration: {str(e)}. Using default configuration.")
            self.config = self.default_config
            self.config_file = os.path.join(self.configs_dir, "config.json")
            return False

    def save_config(self):
        """Save current configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as file:
                json.dump(self.config, file, indent=2)
            
            self._save_last_config()
            return True
        except Exception as e:
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
                
        if "width" not in self.config["window"] or "height" not in self.config["window"]:
            print("Missing window dimensions")
            return False
            
        if "mode" not in self.config["appearance"] or "color_theme" not in self.config["appearance"]:
            print("Missing appearance settings")
            return False
            
        if "family" not in self.config["font"] or "size" not in self.config["font"]:
            print("Missing font settings")
            return False
            
        return True

    def apply_config(self, app):
        """Apply configuration to the application."""
        if not self.config:
            self.load_config()
            
        app.geometry(f"{self.config['window']['width']}x{self.config['window']['height']}")
        app.title(self.config['window']['title'])
        
        ctk.set_appearance_mode(self.config['appearance']['mode'])
        ctk.set_default_color_theme(self.config['appearance']['color_theme'])
        
        try:
            app.configure(fg_color=self.config['appearance']['background_color'])
        except Exception as e:
            print(f"Error setting background color: {str(e)}")
            
        self._apply_interface_type(app)
        
        return True
        
    def _apply_interface_type(self, app):
        """Apply interface type specific settings."""
        interface_type = self.config['interface_type']['type']
        variant = self.config['interface_type']['variant']
        
        if interface_type == "accessibility":
            if variant == "high_contrast":
                self.config['appearance']['background_color'] = "#000000"
                self.config['appearance']['text_color'] = "#FFFF00"
                self.config['font']['size'] = 28
                self.config['font']['button_size'] = 24
            elif variant == "light":
                self.config['appearance']['background_color'] = "#ffffff"
                self.config['appearance']['text_color'] = "#000000"
                self.config['font']['size'] = 28
                self.config['font']['button_size'] = 24
                
        elif interface_type == "gender":
            if variant == "male":
                self.config['appearance']['color_theme'] = "blue"
                self.config['appearance']['button_color'] = "#0047AB"
            elif variant == "female":
                self.config['appearance']['color_theme'] = "blue"
                self.config['appearance']['button_color'] = "#FF69B4"
                
        elif interface_type == "age":
            if variant == "children":
                self.config['appearance']['color_theme'] = "green"
                self.config['appearance']['button_color'] = "#32CD32"
                self.config['font']['family'] = "Comic Sans MS"
            elif variant == "youth":
                self.config['appearance']['color_theme'] = "blue"
                self.config['appearance']['button_color'] = "#1E90FF"
            elif variant == "middle_age":
                self.config['appearance']['color_theme'] = "green"
                self.config['appearance']['button_color'] = "#006400"
            elif variant == "elderly":
                self.config['appearance']['color_theme'] = "dark-blue"
                self.config['font']['size'] = 32
                self.config['font']['button_size'] = 28
