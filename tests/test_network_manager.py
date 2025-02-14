import unittest
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import MainManager
from gui.src.ConfigManager import JsonConfigManager
from unittest.mock import patch, MagicMock
import requests
import shutil
import json
from PySide6.QtWidgets import QApplication
import logging
import stat
from gui.src.MockNetworkManager import MockNetworkManager  # 追加
from gui.src.IMainManagerAdapter import IMainManagerAdapter


logging.basicConfig(level=logging.DEBUG)

app = None


# IMainManagerAdapterを実装したMockGUIクラスを定義
class MockGUI(IMainManagerAdapter):
    def __init__(self):
        self.set_local_path = MagicMock()
        self.set_launch_mode = MagicMock()
        self.set_server_url = MagicMock()
        self.launch_game = MagicMock()
        self.copy_translation_files = MagicMock()
        self.update_data = MagicMock()
        self.get_config_manager = MagicMock()
        self.get_network_manager = MagicMock()
        self.get_base_dir = MagicMock()
        self.check_gui_server_status = MagicMock()
        self.check_translation_server_status = MagicMock()
        self.get_app_version = MagicMock()
        self.get_translation_version = MagicMock()
        self.show_update_dialog = MagicMock()

    def set_local_path(self, path):
        pass

    def set_launch_mode(self, mode):
        pass

    def set_server_url(self, url):
        pass

    def launch_game(self, mode, path):
        pass

    def copy_translation_files(self, path):
        pass

    def update_data(self):
        pass

    def get_config_manager(self):
        pass

    def get_network_manager(self):
        pass

    def get_base_dir(self):
        pass

    def check_gui_server_status(self):
        pass

    def check_translation_server_status(self):
        pass

    def get_app_version(self):
        pass

    def get_translation_version(self):
        pass

    def show_update_dialog(self, app_update, app_url):
        pass


class TestNetworkManager(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global app
        if not QApplication.instance():
            app = QApplication(sys.argv)

    def setUp(self):
        # BASE_DIR環境変数を設定
        os.environ["BASE_DIR"] = os.path.join(os.path.dirname(__file__), "test_data")
        self.config_file = "test_config.json"
        self.config_manager = JsonConfigManager(self.config_file)
        self.main_manager = MainManager.MainManager(MockGUI())  # MockGUIを使用
        self.main_manager.config_manager = self.config_manager
        self.main_manager.network_manager = (
            MockNetworkManager(self.config_manager)  # MockNetworkManagerを設定
        )
        self.test_file = os.path.join(os.path.dirname(__file__), "test_file.txt")
        # テスト用のディレクトリとファイルを作成
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        os.makedirs(os.path.join(self.test_dir, "data"), exist_ok=True)

        self.test_data_dat_path = os.path.join(self.test_dir, "data", "ja_jp_data.dat")
        self.test_data_dir_path = os.path.join(self.test_dir, "data", "ja_jp_data.dir")
        self.test_font_path = os.path.join(self.test_dir, "data", "MyFont.ttf")

        # MainManagerのbase_dirをテスト用のディレクトリに設定
        self.main_manager.base_dir = self.test_dir
        # ErrorHandlerのshow_guiをFalseに設定
        self.main_manager.error_handler.show_gui = False

    @patch("Logic.check_gui_server_status_logic.CheckGuiServerStatusLogic.execute")
    @patch("Logic.check_translation_server_status_logic.CheckTranslationServerStatusLogic.execute")
    @patch("requests.get")
    def test_check_server_status_server_down(self, mock_get, mock_execute_trans, mock_execute_gui):
        # Test checking server status when the server is down
        mock_get.side_effect = requests.exceptions.RequestException("Server is down")
        mock_execute_gui.return_value = MagicMock(success=False, error_msg="Server is down")
        mock_execute_trans.return_value = MagicMock(success=False, error_msg="Server is down")
        result = self.main_manager.check_server_status()
        self.assertEqual(result, (None, None))
        mock_execute_gui.assert_called_once()
    
    @patch("gui.src.MainWindow.MainWindow")  # MainWindowをモック化
    def test_check_updates_with_mock(self, mock_main_window):
        # MockNetworkManagerを使用するように設定
        mock_network_manager = MockNetworkManager(self.config_manager)
        self.main_manager = MainManager.MainManager(mock_main_window)
        self.main_manager.config_manager = self.config_manager
        self.main_manager.network_manager = mock_network_manager

        # バージョン情報を設定
        self.config_manager.set_config("app_version", "1.0.0")
        self.config_manager.set_config("translation_version", "0.9.0")

        # check_updatesを呼び出し
        translation_update, gui_update = self.main_manager.check_updates()

        # 更新があることを確認
        self.assertTrue(translation_update)
        self.assertTrue(gui_update)

        # バージョン情報を更新
        self.config_manager.set_config("app_version", "1.1.0")
        self.config_manager.set_config("translation_version", "1.0.0")

        # check_updatesを呼び出し
        translation_update, gui_update = self.main_manager.check_updates()

        # 更新がないことを確認
        self.assertFalse(translation_update)
        self.assertFalse(gui_update)
