import json
import os
from typing import Optional

import json
import os
from typing import Optional

from typing import Optional, Any
from src.ErrorHandler import ErrorHandler


class JsonConfigManager:
    def __init__(self, base_dir: str):
        self.config_file = os.path.join(base_dir, "data", "config.json")
        self.config: dict[str, Any] = {}
        self.error_handler = ErrorHandler()
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.error_handler.handle_error(
                "Config File Not Found",
                f"The config file '{self.config_file}' was not found. Creating a new one with default settings.",
            )
            self.error_handler.log_message(f"Config file not found: {self.config_file}")  # ログ出力を追加
            self.create_default_config()
        except json.JSONDecodeError:
            self.error_handler.handle_error(
                "Config File Corrupted",
                f"The config file '{self.config_file}' is corrupted. Creating a new one with default settings.",
            )
            self.create_default_config()

    def create_default_config(self):
        self.error_handler.log_message("Creating default config...")  # ログ出力を追加
        self.config = {
            "app_version": "0.0.0",
            "translation_version": "0.0.0",
            "launch_mode": "normal",
            "local_path": "",
            "app_server_url": "",
            "translation_server_url": "",
        }
        self.save_config()
        self.error_handler.log_message("Default config created.")  # ログ出力を追加

    def save_config(self):
        self.error_handler.log_message("Saving config...")  # ログ出力を追加
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            self.error_handler.handle_error(
                "Error Saving Config",
                f"An error occurred while saving the config file: {e}",
            )
        self.error_handler.log_message("Config saved.")  # ログ出力を追加

    def get_config(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any):
        self.config[key] = value
