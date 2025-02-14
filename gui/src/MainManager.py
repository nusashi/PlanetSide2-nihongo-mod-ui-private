import sys
import os
from pathlib import Path

from src.ConfigManager import JsonConfigManager
from src.NetworkManager import RequestsNetworkManager
from src.GameLauncher import DefaultGameLauncher
from src.FileOperations import DefaultFileOperations
from src.ErrorHandler import ErrorHandler
from src.IMainManagerAdapter import IMainManagerAdapter
from src.UIManager import UIManager  # Import UIManager
import re
from typing import Union, Tuple, Optional

from src.Logic.check_update_gui_logic import CheckUpdateGuiLogic
from src.Logic.check_update_translation_logic import CheckUpdateTranslationLogic
from src.Logic.download_translation_logic import DownloadTranslationLogic
from src.Logic.download_gui_logic import DownloadGuiLogic
from src.Logic.copy_dat_file_logic import CopyDatFileLogic
from src.Logic.copy_dir_file_logic import CopyDirFileLogic
from src.Logic.copy_font_file_logic import CopyFontFileLogic
from src.Logic.set_gui_server_url_logic import SetGuiServerUrlLogic
from src.Logic.set_translation_server_url_logic import SetTranslationServerUrlLogic
from src.Logic.check_gui_server_status_logic import CheckGuiServerStatusLogic
from src.Logic.check_translation_server_status_logic import (
    CheckTranslationServerStatusLogic,
)
from src.Logic.get_app_version_logic import GetAppVersionLogic
from src.Logic.get_translation_version_logic import GetTranslationVersionLogic
from src.Logic.get_launch_mode_logic import GetLaunchModeLogic
from src.Logic.get_local_path_logic import GetLocalPathLogic
from src.Logic.set_launch_mode_logic import SetLaunchModeLogic
from src.Logic.download_font_logic import DownloadFontLogic
from src.Logic.game_launch_logic import GameLaunchLogic
from src.Logic.set_local_path_logic import SetLocalPathLogic


class MainManager(IMainManagerAdapter):
    def __init__(self, config_manager, network_manager, base_dir):
        self.next_app_version: Optional[str] = None
        self.next_translation_version: Optional[str] = None
        self.base_dir = base_dir
        if not self.base_dir:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_manager = config_manager
        self.network_manager = network_manager
        self.game_launcher = DefaultGameLauncher()
        self.file_operations = DefaultFileOperations(self.config_manager, self.base_dir)
        self.error_handler = ErrorHandler()
        self.error_handler.log_message("MainManager initialized")
        # Logicモジュールのインスタンスを辞書に格納
        self.Logic = {
            "check_update_gui": CheckUpdateGuiLogic(self),
            "check_update_translation": CheckUpdateTranslationLogic(self),
            "download_translation": DownloadTranslationLogic(self),
            "download_gui": DownloadGuiLogic(self),
            "download_font": DownloadFontLogic(self),
            "game_launch": GameLaunchLogic(self),
            "copy_dat_file": CopyDatFileLogic(self),
            "copy_dir_file": CopyDirFileLogic(self),
            "copy_font_file": CopyFontFileLogic(self),
            "set_gui_server_url": SetGuiServerUrlLogic(self),
            "set_translation_server_url": SetTranslationServerUrlLogic(self),
            "check_gui_server_status": CheckGuiServerStatusLogic(self),
            "check_translation_server_status": CheckTranslationServerStatusLogic(self),
            "get_app_version": GetAppVersionLogic(self),
            "get_translation_version": GetTranslationVersionLogic(self),
            "get_launch_mode": GetLaunchModeLogic(self),
            "get_local_path": GetLocalPathLogic(self),
            "set_local_path": SetLocalPathLogic(self),
            "set_launch_mode": SetLaunchModeLogic(self),
        }

    def run(self):
        self.error_handler.log_message("MainManager.run called")
        # UIManager経由でGUIを初期化・表示
        self.ui_manager = UIManager(self)
        self.ui_manager.run()
        self.error_handler.log_message("MainManager.run finished")

    def check_server_status(self) -> Union[Tuple[bool, int], None]:
        self.error_handler.log_message("MainManager.check_server_status called")
        try:
            gui_status = self.Logic["check_gui_server_status"].execute()
            translation_status = self.Logic["check_translation_server_status"].execute()
            if gui_status.success and gui_status.value:
                self.network_manager.server_status, self.network_manager.server_code = gui_status.value
            elif translation_status.success and translation_status.value:
                self.network_manager.server_status, self.network_manager.server_code = translation_status.value
            return self.network_manager.server_status, self.network_manager.server_code
        except Exception as e:
            self.error_handler.handle_error("Network Error", str(e), stop_execution=True)
            return None
        self.error_handler.log_message("MainManager.check_server_status finished")

    def check_for_updates(self):
        """
        アプリケーションと翻訳のアップデートを確認し、必要に応じて
        `self.next_app_version` と `self.next_translation_version` を設定する。
        """
        self.error_handler.log_message("MainManager.check_for_updates called")
        app_version_result = self.get_app_version()
        translation_version_result = self.get_translation_version()
        if app_version_result.success:
            current_app_version = self.get_config("app_version")
            if current_app_version != app_version_result.value:
                self.next_app_version = app_version_result.value
        if translation_version_result.success:
            current_translation_version = self.get_config("translation_version")
            if current_translation_version != translation_version_result.value:
                self.next_translation_version = translation_version_result.value
        self.error_handler.log_message("MainManager.check_for_updates finished")

    def check_update_gui(self):
        self.error_handler.log_message("MainManager.check_update_gui called")
        result = self.Logic["check_update_gui"].execute(repo_owner="maboroshino", repo_name="PlanetSide2-nihongo-mod")
        return result

    def check_update_translation(self):
        self.error_handler.log_message("MainManager.check_update_translation called")
        result = self.Logic["check_update_translation"].execute(repo_owner="maboroshino", repo_name="PlanetSide2-nihongo-mod")
        return result

    def set_app_server_url(self, url):
        self.error_handler.log_message("MainManager.set_app_server_url called")
        result = self.Logic["set_gui_server_url"].execute(url)
        if result.success:
            self.config_manager.save_config()
        return result

    def set_translation_server_url(self, url):
        self.error_handler.log_message("MainManager.set_translation_server_url called")
        result = self.Logic["set_translation_server_url"].execute(url)
        if result.success:
            self.config_manager.save_config()
        return result

    def set_local_path(self, path):
        self.error_handler.log_message("MainManager.set_local_path called")
        result = self.Logic["set_local_path"].execute(path)
        if result.success:
            self.config_manager.save_config()
        return result

    def update_gui(self):
        """
        GUIのアップデートを確認し、必要であればダウンロード・更新を行う
        """
        self.error_handler.log_message("MainManager.update_gui called")
        try:
            update_required = self.Logic["check_update_gui"].execute(repo_owner="maboroshino", repo_name="PlanetSide2-nihongo-mod")
            if update_required.success and update_required.value:
                pass
                # TODO: 再起動処理
            else:
                self.error_handler.log_message("MainManager.update_gui: No update required")
        except Exception as e:
            self.error_handler.handle_error("Update Error", str(e))

    def update_translation(self):
        """
        翻訳ファイルのアップデートを確認し、必要であればダウンロード・更新を行う
        """
        self.error_handler.log_message("MainManager.update_translation called")
        try:
            update_required = self.Logic["check_update_translation"].execute(repo_owner="maboroshino", repo_name="PlanetSide2-nihongo-mod")
            if update_required.success and update_required.value:
                pass
                # TODO: ファイルコピー処理
            else:
                self.error_handler.log_message("MainManager.update_translation: No update required")
        except Exception as e:
            self.error_handler.handle_error("Update Error", str(e))

    def get_config(self, key):
        self.error_handler.log_message("MainManager.get_config called")
        return self.config_manager.get_config(key)

    def set_launch_mode(self, mode):
        self.error_handler.log_message("MainManager.set_launch_mode called")
        try:
            self.Logic["set_launch_mode"].execute(mode=mode)
            self.config_manager.set_config("launch_mode", mode)
            self.config_manager.save_config()
        except Exception as e:
            self.error_handler.handle_error("Config Error", str(e))

    def launch_game(self, mode, path):
        self.error_handler.log_message("MainManager.launch_game called")
        try:
            result = self.Logic["game_launch"].execute(mode=mode, path=path)
            if result and result.success:
                self.error_handler.log_message("MainManager.launch_game: success")
            else:
                error_message = result.error if result.error else "Unknown error"
                if isinstance(result.error, FileNotFoundError):
                    error_message = "LaunchPad.exeが見つかりません。" "PlanetSide2のローカルパスが正しい位置になっているか確認してください。"
                self.error_handler.handle_error("Launch Error", error_message, self.ui_manager.get_main_window())
        except Exception as e:
            self.error_handler.handle_error(
                "Launch Error",
                str(e),
                self.ui_manager.get_main_window(),
                stop_execution=True,
            )

    def copy_translation_files(self, path):
        self.error_handler.log_message("MainManager.copy_translation_files called")
        try:
            result_dat = self.Logic["copy_dat_file"].execute(path)
            result_dir = self.Logic["copy_dir_file"].execute(path)
            result_font = self.Logic["copy_font_file"].execute(path)
            if result_dat and result_dat.success and result_dir and result_dir.success and result_font and result_font.success:
                pass
            else:
                error_message = ""
                if result_dat and result_dat.error:
                    error_message += f"copy_dat_file error: {result_dat.error}\n"
                if result_dir and result_dir.error:
                    error_message += f"copy_dir_file error: {result_dir.error}\n"
                if result_font and result_font.error:
                    error_message += f"copy_font_file error: {result_font.error}\n"
                self.error_handler.handle_error(
                    "File Operation Error",
                    error_message,
                    self.ui_manager.get_main_window(),
                )
        except Exception as e:
            self.error_handler.handle_error("File Operation Error", str(e), self.ui_manager.get_main_window())

    def update_data(self):
        self.error_handler.log_message("MainManager.update_data called")
        try:
            # Logicモジュールを使ってデータを更新
            self.Logic["download_translation"].execute(
                "maboroshino",
                "PlanetSide2-nihongo-mod",
                "ja_jp_data.dat",
                self.base_dir,
            )
            self.Logic["download_translation"].execute(
                "maboroshino",
                "PlanetSide2-nihongo-mod",
                "ja_jp_data.dir",
                self.base_dir,
            )
            self.Logic["download_font"].execute("maboroshino", "PlanetSide2-nihongo-mod", "MyFont.ttf", self.base_dir)
            # GUIの更新処理
            gui_update_result = self.Logic["check_update_gui"].execute("maboroshino", "PlanetSide2-nihongo-mod")
            if gui_update_result.success and gui_update_result.value:
                self.ui_manager.show_update_dialog(True, "")  # TODO: Fix URL to actual gui update url
        except Exception as e:
            self.error_handler.handle_error("Update Error", str(e))

    def show_update_dialog(self, app_update, app_url):
        self.error_handler.log_message("MainManager.show_update_dialog called")
        # Dummy implementation
        print(f"show_update_dialog: {app_update} {app_url}")

    def get_app_version(self):
        self.error_handler.log_message("MainManager.get_app_version called")
        return self.Logic["get_app_version"].execute()

    def get_translation_version(self):
        self.error_handler.log_message("MainManager.get_translation_version called")
        return self.Logic["get_translation_version"].execute()

    def get_config_manager(self):
        self.error_handler.log_message("MainManager.get_config_manager called")
        return self.config_manager

    def get_network_manager(self):
        self.error_handler.log_message("MainManager.get_network_manager called")
        return self.network_manager

    def get_error_handler(self):
        self.error_handler.log_message("MainManager.get_error_handler called")
        return self.error_handler

    def get_base_dir(self) -> str:
        self.error_handler.log_message("MainManager.get_base_dir called")
        return self.base_dir

    def check_gui_server_status(self) -> Union[Tuple[bool, int], None]:
        self.error_handler.log_message("MainManager.check_gui_server_status called")
        try:
            return self.Logic["check_gui_server_status"].execute()
        except Exception as e:
            self.error_handler.handle_error("Network Error", str(e))
            return None

    def check_translation_server_status(self) -> Union[Tuple[bool, int], None]:
        self.error_handler.log_message("MainManager.check_translation_server_status called")
        try:
            return self.Logic["check_translation_server_status"].execute()
        except Exception as e:
            self.error_handler.handle_error("Network Error", str(e))
            return None
