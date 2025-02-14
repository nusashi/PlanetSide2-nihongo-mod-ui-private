import unittest
import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from gui.src.MainManager import MainManager
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
        return self.get_config_manager

    def get_network_manager(self):
        return self.get_network_manager

    def get_base_dir(self):
        return self.get_base_dir

    def check_gui_server_status(self):
        return self.check_gui_server_status

    def check_translation_server_status(self):
        return self.check_translation_server_status

    def get_app_version(self):
        return self.get_app_version

    def get_translation_version(self):
        return self.get_translation_version

    def show_update_dialog(self, app_update, app_url):
        pass


class TestMainManager(unittest.TestCase):
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
        self.main_manager = MainManager(MockGUI())  # MockGUIを使用
        self.main_manager.config_manager = self.config_manager
        self.main_manager.network_manager = MockNetworkManager(self.config_manager)  # MockNetworkManagerを設定
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
        print(sys.path)

    def test_init(self):
        # Test that the MainManager is initialized correctly
        self.assertIsNotNone(self.main_manager.config_manager)
        self.assertIsNotNone(self.main_manager.network_manager)
        self.assertIsNotNone(self.main_manager.game_launcher)
        self.assertIsNotNone(self.main_manager.file_operations)
        self.assertIsNotNone(self.main_manager.error_handler)
        self.assertIsInstance(self.main_manager.gui_app, MockGUI)  # gui_appがMockGUIのインスタンスであることを確認

    @patch("gui.src.Logic.set_local_path_logic.SetLocalPathLogic.execute")
    @patch("gui.src.Logic.set_launch_mode_logic.SetLaunchModeLogic.execute")
    @patch("gui.src.Logic.check_gui_server_status_logic.CheckGuiServerStatusLogic.execute")
    @patch("gui.src.Logic.check_translation_server_status_logic.CheckTranslationServerStatusLogic.execute")
    @patch("gui.src.Logic.check_update_gui_logic.CheckUpdateGuiLogic.execute")
    @patch("gui.src.Logic.check_update_translation_logic.CheckUpdateTranslationLogic.execute")
    @patch("gui.src.Logic.copy_dat_file_logic.CopyDatFileLogic.execute")
    @patch("gui.src.Logic.copy_dir_file_logic.CopyDirFileLogic.execute")
    @patch("gui.src.Logic.copy_font_file_logic.CopyFontFileLogic.execute")
    @patch("gui.src.Logic.set_translation_server_url_logic.SetTranslationServerUrlLogic.execute")
    @patch("gui.src.Logic.get_app_version_logic.GetAppVersionLogic.execute")
    @patch("gui.src.Logic.get_translation_version_logic.GetTranslationVersionLogic.execute")
    @patch("gui.src.Logic.game_launch_logic.GameLaunchLogic.execute")
    @patch("gui.src.Logic.download_translation_logic.DownloadTranslationLogic.execute")
    @patch("gui.src.Logic.download_font_logic.DownloadFontLogic.execute")
    def test_logic_integration(
        self,
        mock_download_font,
        mock_download_translation,
        mock_launch_game,
        mock_get_translation_version,
        mock_get_app_version,
        mock_set_translation_server_url,
        mock_copy_font_file,
        mock_copy_dir_file,
        mock_copy_dat_file,
        mock_check_update_translation,
        mock_check_update_gui,
        mock_check_translation_server_status,
        mock_check_gui_server_status,
        mock_set_launch_mode,
        mock_set_local_path,
    ):
        # MainManagerとLogicモジュールの結合テスト
        # MockGUIを使用するように修正
        mock_gui_app = self.main_manager.gui_app

        # 各Logicモジュールのexecuteメソッドの戻り値を設定
        mock_set_local_path.return_value = MagicMock(success=True)
        # 各Logicモジュールのexecuteメソッドの戻り値を設定
        mock_set_local_path.return_value = MagicMock(success=True)
        # 各Logicモジュールのexecuteメソッドの戻り値を設定
        mock_set_local_path.return_value = MagicMock(success=True)
        mock_set_launch_mode.return_value = MagicMock(success=True)
        mock_check_gui_server_status.return_value = MagicMock(success=True, value=(200, None))
        mock_check_translation_server_status.return_value = MagicMock(success=True, value=(200, None))
        mock_check_update_gui.return_value = MagicMock(gui_updatable=False, current_gui_version="1.0.0", latest_gui_version="1.0.0")
        mock_check_update_translation.return_value = MagicMock(translation_updatable=False, current_translation_version="1.0.0", latest_translation_version="1.0.0")
        mock_copy_dat_file.return_value = MagicMock(success=True)
        mock_copy_dir_file.return_value = MagicMock(success=True)
        mock_copy_font_file.return_value = MagicMock(success=True)
        mock_set_translation_server_url.return_value = MagicMock(success=True)
        mock_get_app_version.return_value = MagicMock(success=True, value="1.0.0")
        mock_get_translation_version.return_value = MagicMock(success=True, value="1.0.0")
        mock_launch_game.return_value = MagicMock(success=True)
        mock_download_translation.return_value = MagicMock(success=True)
        mock_download_font.return_value = MagicMock(success=True)

        # 各Logicモジュールのexecuteメソッドが期待通りに呼び出されたことを確認
        self.main_manager.set_local_path("test_path")
        mock_set_local_path.assert_called_once_with("test_path")

        self.main_manager.set_launch_mode(1)
        mock_set_launch_mode.assert_called_once_with(1)

        self.main_manager.check_server_status()
        mock_check_gui_server_status.assert_called_once()
        mock_check_translation_server_status.assert_called_once()

        self.main_manager.check_updates()
        mock_check_update_gui.assert_called_once()
        mock_check_update_translation.assert_called_once()

        self.main_manager.copy_translation_files("test_path")
        mock_copy_dat_file.assert_called_once_with("test_path")
        mock_copy_dir_file.assert_called_once_with("test_path")
        mock_copy_font_file.assert_called_once_with("test_path")

        self.main_manager.set_server_url("test_url")
        mock_set_translation_server_url.assert_called_once_with("test_url")

        self.main_manager.get_latest_release_info("owner", "repo")
        mock_get_app_version.assert_called_once_with("owner", "repo")
        mock_get_translation_version.assert_called_once_with("owner", "repo")

        self.main_manager.launch_game(1, "test_path")
        mock_launch_game.assert_called_once_with(1, "test_path")

        self.main_manager.update_data()
        self.assertEqual(mock_download_translation.call_count, 2)
        mock_download_font.assert_called_once()
        self.assertEqual(mock_check_update_gui.call_count, 2)
        # MockNetworkManagerを使用しているので、show_update_dialogは呼ばれないはず


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test MainManager functionalities.")
    parser.add_argument("--test", type=str, help="Specific test to run (e.g., test_set_local_path)")
    args = parser.parse_args()

    # Run specific test if provided, otherwise run all tests
    if args.test:
        suite = unittest.TestSuite()
        suite.addTest(TestMainManager(args.test))
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        unittest.main()
