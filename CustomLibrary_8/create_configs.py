import os
import json
import traceback


def create_default_configs(configs_dir):
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
            "window": {"width": 500, "height": 700, "title": "Calculator"},
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
            "window": {"width": 500, "height": 700, "title": "Calculator"},
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
            "window": {"width": 400, "height": 600, "title": "Calculator"},
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
            "window": {"width": 400, "height": 600, "title": "Calculator"},
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
            "window": {"width": 450, "height": 650, "title": "Calculator"},
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
            "window": {"width": 400, "height": 600, "title": "Calculator"},
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
            "window": {"width": 420, "height": 620, "title": "Calculator"},
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
            "window": {"width": 550, "height": 750, "title": "Calculator"},
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
        
    for filename, config in configs.items():
        filepath = os.path.join(configs_dir, filename)
        if not os.path.exists(filepath):
            try:
                with open(filepath, 'w', encoding='utf-8') as file:
                        json.dump(config, file, indent=2)
            except Exception as e:
                traceback.print_exc()


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    configs_dir = os.path.join(base_dir, "configs")
    os.makedirs(configs_dir, exist_ok=True)

    create_default_configs(configs_dir)
