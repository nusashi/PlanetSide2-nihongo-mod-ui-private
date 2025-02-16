import json
import os
from typing import Optional, Any
from const import const


class JsonConfigManager:
    def __init__(self, base_dir: str):
        self.initial_config_flag = False
        self.config_file = os.path.join(base_dir, "data", "config.json")
        self.config: dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print("設定ファイルが見つかりません")
            print(f"設定ファイル '{self.config_file}' が見つかりませんでした。デフォルト設定で新規作成します。")
            self.create_default_config()
        except json.JSONDecodeError:
            print("設定ファイルが破損しています")
            print(f"設定ファイル '{self.config_file}' が破損しています。デフォルト設定で新規作成します。")
            self.create_default_config()

    def create_default_config(self):
        print("デフォルト設定を作成中...")
        self.config = {
            const.APP_VERSION: const.DEFAULT_APP_VERSION,
            const.TRANSLATION_VERSION: const.DEFAULT_TRANSLATION_VERSION,
            const.LAUNCH_MODE: const.DEFAULT_LAUNCH_MODE,
            const.LOCAL_PATH: const.DEFAULT_LOCAL_PATH,
            const.APP_UPDATE_SERVER_URL: const.DEFAULT_APP_UPDATE_SERVER_URL,
            const.TRANSLATION_UPDATE_SERVER_URL: const.DEFAULT_TRANSLATION_UPDATE_SERVER_URL,
        }
        self.save_config()
        self.initial_config_flag = True
        print("デフォルト設定を作成しました。")

    def save_config(self):
        print("設定を保存中...")
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print("設定ファイルの保存エラー")
            print(f"設定ファイルの保存中にエラーが発生しました: {e}")
        print("設定を保存しました。")

    def get_config(self, key: str, default: Optional[Any] = None) -> Any:
        return self.config.get(key, default)

    def set_config(self, key: str, value: Any):
        self.config[key] = value

    def get_initial_config(self):
        return self.initial_config_flag
