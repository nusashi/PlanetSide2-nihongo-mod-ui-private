from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from src.IMainManagerAdapter import IMainManagerAdapter
from src.MainWindow import MainWindow
from src.settings_popup import SettingsPopup
from typing import Union, Tuple


class UIManager(IMainManagerAdapter):
    def __init__(self, main_manager):
        self.main_manager = main_manager
        self.main_window = None
        self.settings_popup = None
        self.main_manager.get_error_handler().log_message("UIManager initialized")
        print("UIManager initialized")

    def run(self):
        self.main_manager.get_error_handler().log_message("UIManager.run called")
        print("UIManager.run called")
        if not QApplication.instance():
            app = QApplication([])
            print("New QApplication instance created")
        else:
            app = QApplication.instance()
            print("Using existing QApplication instance")
        self.main_window = MainWindow(self)
        print("MainWindow instance created")
        self.main_window.setup_layout()
        print("MainWindow.setup_layout() called")
        self.main_window.show()
        print("MainWindow.show() called")
        self.update_ui()  # UIの初期状態を設定
        print("UIManager.update_ui() called")
        app.exec()
        print("app.exec() called")

    def show_error_dialog(self, title, message):
        self.main_manager.get_error_handler().log_message(
            "UIManager.show_error_dialog called"
        )
        QMessageBox.critical(self.main_window, title, message)

    def show_update_dialog(self, app_update, app_url):
        self.main_manager.get_error_handler().log_message(
            "UIManager.show_update_dialog called"
        )
        # Dummy implementation
        print(f"show_update_dialog: {app_update} {app_url}")

    def launch_game(self, mode, path):
        self.main_manager.get_error_handler().log_message(
            "UIManager.launch_game called"
        )
        self.main_manager.launch_game(mode, path)

    def copy_translation_files(self, path):
        self.main_manager.get_error_handler().log_message(
            "UIManager.copy_translation_files called"
        )
        self.main_manager.copy_translation_files(path)

    def update_data(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.update_data called"
        )
        self.main_manager.update_data()

    def open_settings_popup(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.open_settings_popup called"
        )
        if self.settings_popup is None:
            self.settings_popup = SettingsPopup()
        self.update_settings_popup()  # 設定ポップアップの内容を更新
        self.settings_popup.show()

    def set_app_server_url(self, url):
        self.main_manager.get_error_handler().log_message(
            "UIManager.set_app_server_url called"
        )
        result = self.main_manager.set_app_server_url(url)
        if result.success:
            self.main_manager.get_error_handler().log_message(
                f"App server URL set to {url}"
            )
            self.update_settings_popup()  # 設定ポップアップの内容を更新

    def set_translation_server_url(self, url):
        self.main_manager.get_error_handler().log_message(
            "UIManager.set_translation_server_url called"
        )
        result = self.main_manager.set_translation_server_url(url)
        if result.success:
            self.main_manager.get_error_handler().log_message(
                f"Translation server URL set to {url}"
            )
            self.update_settings_popup()  # 設定ポップアップの内容を更新

    def set_local_path(self, path):
        self.main_manager.get_error_handler().log_message(
            "UIManager.set_local_path called"
        )
        result = self.main_manager.set_local_path(path)
        if result.success:
            self.main_manager.get_error_handler().log_message(
                f"Local path set to {path}"
            )
            self.update_ui()

    def update_settings_popup(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.update_settings_popup called"
        )
        if self.settings_popup:
            app_server_url = self.main_manager.get_config("app_server_url")
            translation_server_url = self.main_manager.get_config(
                "translation_server_url"
            )
            local_path = self.main_manager.get_config("local_path")
            self.settings_popup.lineedit_app_server_url.setText(app_server_url)
            self.settings_popup.lineedit_translation_server_url.setText(
                translation_server_url
            )
            self.settings_popup.lineedit_local_path.setText(local_path)

    def update_ui(self):
        """
        MainManagerから取得した情報や、config.jsonの内容を基に、
        MainWindowのUI要素を更新する
        """
        self.main_manager.get_error_handler().log_message("UIManager.update_ui called")
        print("UIManager.update_ui called")
        if self.main_window:
            # ローカルパスの表示を更新
            # local_path = self.main_manager.get_config("local_path")
            # self.main_window.update_local_path(local_path)

            # 起動モードを読み込んで設定
            mode = self.main_manager.get_config("launch_mode")
            self.main_window.set_launch_mode_on_startup(mode)

            # 設定ポップアップが開いている場合は、そちらも更新
            if self.settings_popup:
                self.update_settings_popup()
            print("UIManager.update_ui: self.main_window is not None")
        print("UIManager.update_ui finished")

    def get_main_window(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.get_main_window called"
        )
        return self.main_window

    def get_config_manager(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.get_config_manager called"
        )
        return self.main_manager.get_config_manager()

    def get_network_manager(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.get_network_manager called"
        )
        return self.main_manager.get_network_manager()

    def get_error_handler(self):
        self.main_manager.get_error_handler().log_message(
            "UIManager.get_error_handler called"
        )
        return self.main_manager.get_error_handler()

    def check_updates(self):
        self.main_manager.check_for_updates()

    def get_base_dir(self) -> str:
        return self.main_manager.get_base_dir()

    def check_gui_server_status(self) -> Union[Tuple[bool, int], None]:
        self.main_manager.get_error_handler().log_message(
            "UIManager.check_gui_server_status called"
        )
        try:
            return self.main_manager.check_gui_server_status()
        except Exception as e:
            self.main_manager.get_error_handler().handle_error("Network Error", str(e))
            return None

    def check_translation_server_status(self) -> Union[Tuple[bool, int], None]:
        self.main_manager.get_error_handler().log_message(
            "UIManager.check_translation_server_status called"
        )
        try:
            return self.main_manager.check_translation_server_status()
        except Exception as e:
            self.main_manager.get_error_handler().handle_error("Network Error", str(e))
            return None

    def set_launch_mode(self, mode: int):
        self.main_manager.get_error_handler().log_message(
            "UIManager.set_launch_mode called"
        )
        print(f"UIManager.set_launch_mode: mode={mode}")
        result = self.main_manager.set_launch_mode(mode)
        if result.success:
            self.main_manager.get_error_handler().log_message(
                f"Launch mode set to {mode}"
            )
            # self.update_ui()  # UIの更新は行わない
            if mode == 0:
                self.main_window.radio_normal.setChecked(True)
            elif mode == 1:
                self.main_window.radio_steam.setChecked(True)
