import sys
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QObject, Signal
from ui.main_window import MainWindow
from ui.settings_popup import SettingsPopup
from ui.help_popup import HelpPopup
from const import const


class UIManager(QObject):
    # カスタムシグナル
    local_path_changed = Signal(str)
    app_update_server_url_changed = Signal(str)
    translation_update_server_url_changed = Signal(str)
    launch_mode_changed = Signal(str)
    status_text_changed = Signal(str)
    app_version_label_changed = Signal(str)
    translation_version_label_changed = Signal(str)
    show_update_app_button_changed = Signal(bool)
    show_update_translation_button_changed = Signal(bool)

    def __init__(self, main_manager):
        super().__init__()
        self.app = QApplication(sys.argv)  # QApplicationインスタンスをここで作成
        self.main_manager = main_manager
        self.main_window = MainWindow(self)
        self.settings_popup = SettingsPopup()
        self.help_popup = HelpPopup()
        self.setup_connections()
        self.show_main_window()

    # setup_connections, show_main_window, 各種イベントハンドラ, redraw, update_launch_mode_ui は変更なし(略)
    def run(self):
        sys.exit(self.app.exec())

    def setup_connections(self):
        # MainWindowのコールバック設定
        self.main_window.set_radio_normal_callback(self.on_radio_normal_clicked)
        self.main_window.set_radio_steam_callback(self.on_radio_steam_clicked)
        self.main_window.set_button_game_launch_callback(self.on_game_launch_clicked)
        self.main_window.set_button_replace_translation_callback(self.on_replace_translation_clicked)
        self.main_window.set_button_update_app_callback(self.on_update_app_clicked)
        self.main_window.set_button_update_translation_callback(self.on_update_translation_clicked)
        self.main_window.set_button_check_update_callback(self.on_check_update_clicked)
        self.main_window.set_button_settings_callback(self.on_settings_clicked)
        self.main_window.set_button_help_callback(self.on_help_clicked)
        self.main_window.set_combobox_launch_mode_callback(self.on_launch_mode_changed)
        self.main_window.set_close_event_callback(self.on_main_window_close_event)
        # SettingsPopupのコールバック設定
        self.settings_popup.set_button_local_path_callback(self.on_local_path_browse_clicked)
        # シグナルとスロットの接続
        self.local_path_changed.connect(self.main_window.update_local_path_label)
        self.local_path_changed.connect(self.settings_popup.update_lineedit_local_path_text)
        self.app_update_server_url_changed.connect(self.settings_popup.update_lineedit_app_server_url_text)
        self.translation_update_server_url_changed.connect(self.settings_popup.update_lineedit_translation_server_url_text)
        self.launch_mode_changed.connect(self.update_launch_mode_ui)
        self.status_text_changed.connect(self.main_window.update_status_text)
        self.app_version_label_changed.connect(self.main_window.update_app_version_label)
        self.translation_version_label_changed.connect(self.main_window.update_translation_version_label)
        self.show_update_app_button_changed.connect(self.main_window.button_update_app.setVisible)
        self.show_update_translation_button_changed.connect(self.main_window.button_update_translation.setVisible)

    # MainWindowの表示
    def show_main_window(self):
        self.redraw()  # 初期描画
        self.main_window.show()

    # 各種イベントハンドラ (MainManagerの同名メソッドを呼び出す)
    def on_radio_normal_clicked(self):
        self.main_manager.launch_mode = const.NORMAL_LAUNCH
        self.launch_mode_changed.emit(self.main_manager.launch_mode)

    def on_radio_steam_clicked(self):
        self.main_manager.launch_mode = const.STEAM_LAUNCH
        self.launch_mode_changed.emit(self.main_manager.launch_mode)

    def on_game_launch_clicked(self):
        if self.main_manager.try_game_launch():
            self.status_text_changed.emit("ゲームを起動しました。")
        else:
            self.status_text_changed.emit("ゲームの起動に失敗しました。")

    def on_replace_translation_clicked(self):
        if self.main_manager.try_translation():
            self.status_text_changed.emit("翻訳ファイルを配置しました。")
        else:
            self.status_text_changed.emit("翻訳ファイルの配置に失敗しました。")

    def on_update_app_clicked(self):
        # TODO: ダウンロード処理、進捗表示
        self.main_manager.download_app_file("temp")  # 仮のディレクトリ
        self.status_text_changed.emit("Appのアップデートは未実装")

    def on_update_translation_clicked(self):
        # TODO: ダウンロード処理、進捗表示
        self.main_manager.download_translation_file("data")  # dataディレクトリ
        self.status_text_changed.emit("翻訳のアップデートは未実装")

    def on_check_update_clicked(self):
        self.main_manager.check_update()
        self.redraw()

    def on_settings_clicked(self):
        self.settings_popup.show()

    def on_help_clicked(self):
        self.help_popup.show()

    def on_launch_mode_changed(self, index):
        # コンボボックスが変更されたときの処理 (必要に応じて)
        pass

    def on_local_path_browse_clicked(self):
        # TODO: MainManagerのset_local_pathを呼び出して、local_path_changedシグナルを発行
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(self.settings_popup, "Select Directory")
        if selected_path:
            self.main_manager.local_path = selected_path
            self.local_path_changed.emit(selected_path)

    def on_main_window_close_event(self, event):
        # TODO: 必要なら確認ダイアログを出すなど
        event.accept()
        QApplication.quit()

    # UIの再描画
    def redraw(self):
        # MainManagerから最新の情報を取得してUIを更新
        self.local_path_changed.emit(self.main_manager.local_path)
        self.app_update_server_url_changed.emit(self.main_manager.app_update_server_url)
        self.translation_update_server_url_changed.emit(self.main_manager.translation_update_server_url)
        self.launch_mode_changed.emit(self.main_manager.launch_mode)
        self.status_text_changed.emit(self.main_manager.status_string)
        self.app_version_label_changed.emit(f"アプリバージョン: {self.main_manager.app_version}")
        self.translation_version_label_changed.emit(f"翻訳バージョン: {self.main_manager.translation_version}")

        # アップデートボタンの表示/非表示
        if self.main_manager.next_app_version != self.main_manager.app_version:
            self.show_update_app_button_changed.emit(True)
        else:
            self.show_update_app_button_changed.emit(False)

        if self.main_manager.next_translation_version != self.main_manager.translation_version:
            self.show_update_translation_button_changed.emit(True)
        else:
            self.show_update_translation_button_changed.emit(False)

        # 起動モードのUI更新
        self.update_launch_mode_ui(self.main_manager.launch_mode)

    def update_launch_mode_ui(self, launch_mode):
        if launch_mode == const.NORMAL_LAUNCH:
            self.main_window.radio_normal.setChecked(True)
        elif launch_mode == const.STEAM_LAUNCH:
            self.main_window.radio_steam.setChecked(True)
        # 他のモードがあれば追加
