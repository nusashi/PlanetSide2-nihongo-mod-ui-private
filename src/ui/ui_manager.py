import sys
from typing import Tuple, List, Callable
from packaging import version  # バージョン比較に使用
from typing import Callable
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import QObject, Signal, QThread
from ui.main_window import MainWindow
from ui.settings_popup import SettingsPopup
from ui.help_popup import HelpPopup
from ui.tutorial_popup import TutorialPopup
from const import const


class DownloadWorker(QThread):
    """
    ダウンロード処理を別スレッドで実行するクラス。
    進捗通知、完了通知、エラー通知を行う。
    """

    progress_signal = Signal(int, int, str)  # 進捗: 現在のファイル番号, 総数, ファイル名
    finished_signal = Signal(tuple)  # 完了: (ダウンロードしたファイルのリスト, 完了時コールバック関数)
    error_signal = Signal(str)  # エラーメッセージ

    def __init__(self, download_func, filenames, finished_callback):
        """
        初期化メソッド。
        :param download_func: MainManagerから提供されるダウンロード関数
        :param filenames: ダウンロードするファイル名のリスト
        :param finished_callback: 完了時コールバック関数
        """
        super().__init__()
        self.download_func = download_func
        self.filenames = filenames
        self.finished_callback = finished_callback
        self._cancelled = False

    def run(self):
        """
        スレッド内でダウンロード処理を実行。
        進捗をシグナルで通知し、完了またはエラーを通知。
        """
        try:
            downloaded_files = self.download_func(self.filenames, self._progress_callback)
            if not self._cancelled:
                self.finished_signal.emit((downloaded_files, self.finished_callback))
        except Exception as e:
            self.error_signal.emit(str(e))

    def _progress_callback(self, filename, current, total):
        """
        進捗通知用のコールバック関数。
        キャンセルフラグが立っている場合は例外を発生させる。
        """
        if self._cancelled:
            raise InterruptedError("ダウンロードがキャンセルされました")
        self.progress_signal.emit(current, total, filename)


    def cancel(self):
        """ダウンロード処理をキャンセルする。"""
        self._cancelled = True


class UIManager(QObject):
    # プロパティのコールバックを初期化
    _property_callbacks = {}
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

    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)  # QApplicationインスタンスをここで作成
        self.main_window = MainWindow(self)
        self.settings_popup = SettingsPopup(self)
        self.help_popup = HelpPopup()
        self.tutorial_popup = TutorialPopup(self)
        self.setup_connections()

    # 新しいプロパティセッターの追加
    def set_property_callbacks(self, property_name: str, getter: Callable[[], any], setter: Callable[[any], None]):
        self._property_callbacks[property_name] = {"getter": getter, "setter": setter}

    def get_property(self, property_name: str) -> any:
        if property_name not in self._property_callbacks:
            raise ValueError(f"プロパティ '{property_name}'には取得関数(getter)が設定されていません。")
        return self._property_callbacks[property_name]["getter"]()

    def set_property(self, property_name: str, value: any):
        if property_name not in self._property_callbacks:
            raise ValueError(f"プロパティ '{property_name}'には設定関数(setter)が設定されていません。")
        self._property_callbacks[property_name]["setter"](value)

    def set_on_radio_normal_clicked_callback(self, callback: Callable[[str], None]):
        self._on_radio_normal_clicked_callback = callback

    def set_on_radio_steam_clicked_callback(self, callback: Callable[[str], None]):
        self._on_radio_steam_clicked_callback = callback

    def set_on_game_launch_clicked_callback(self, callback: Callable[[], None]):
        self._on_game_launch_clicked_callback = callback

    def set_on_replace_translation_clicked_callback(self, callback: Callable[[], None]):
        self._on_replace_translation_clicked_callback = callback

    def set_download_app_files_callback(self, download_app_files_callback):
        self._download_app_files_callback = download_app_files_callback

    def set_download_translation_files_callback(self, download_translation_files_callback):
        self._download_translation_files_callback = download_translation_files_callback

    def set_on_update_app_clicked_callback(self, callback_data: Tuple[List, Callable[[], None]]):
        self._on_update_app_clicked_callback_data = callback_data

    def set_on_update_translation_clicked_callback(self, callback_data: Tuple[List, Callable[[], None]]):
        self._on_update_translation_clicked_callback_data = callback_data

    def set_on_check_update_clicked_callback(self, callback: Callable[[], None]):
        self._on_check_update_clicked_callback = callback

    def run(self):
        sys.exit(self.app.exec())

    def start_download(self, download_func, filenames, finished_callback):
        """
        ダウンロード処理を開始。
        DownloadWorkerを作成し、シグナルとスロットを接続。
        """
        self.download_worker = DownloadWorker(download_func, filenames, finished_callback)
        self.download_worker.progress_signal.connect(self.update_progress)
        self.download_worker.finished_signal.connect(self.on_download_finished)
        self.download_worker.error_signal.connect(self.on_download_error)
        self.download_worker.start()

    def cancel_download(self):
        """ダウンロードをキャンセル。"""
        if hasattr(self, "download_worker"):
            self.download_worker.cancel()

    def update_progress(self, current, total, filename):
        """進捗情報をGUIに反映。"""
        self.status_text_changed.emit(f"ダウンロード中: {filename} ({current}/{total})")

    def on_download_finished(self, data):
        """ダウンロード完了時の処理。"""
        downloaded_files, finished_callback = data
        self.status_text_changed.emit("ダウンロード完了")
        if finished_callback:
            finished_callback()

    def on_download_error(self, error_message):
        """エラー発生時の処理。"""
        self.status_text_changed.emit(f"エラー: {error_message}")

    def setup_connections(self):
        # MainWindowのコールバック設定
        self.main_window.set_radio_normal_callback(self._on_radio_normal_clicked)
        self.main_window.set_radio_steam_callback(self._on_radio_steam_clicked)
        self.main_window.set_button_game_launch_callback(self._on_game_launch_clicked)
        self.main_window.set_button_replace_translation_callback(self._on_replace_translation_clicked)
        self.main_window.set_button_update_app_callback(self._on_update_app_clicked)
        self.main_window.set_button_update_translation_callback(self._on_update_translation_clicked)
        self.main_window.set_button_check_update_callback(self._on_check_update_clicked)
        self.main_window.set_button_settings_callback(self._on_settings_clicked)
        self.main_window.set_button_help_callback(self._on_help_clicked)
        self.main_window.set_close_event_callback(self._on_main_window_close_event)

        # SettingsPopupのコールバック設定
        self.settings_popup.set_button_local_path_callback(self._on_local_path_browse_clicked)

        # シグナルとスロットの接続
        self.local_path_changed.connect(self.settings_popup.update_lineedit_local_path_text)
        self.app_update_server_url_changed.connect(self.settings_popup.update_lineedit_app_server_url_text)
        self.translation_update_server_url_changed.connect(self.settings_popup.update_lineedit_translation_server_url_text)
        self.launch_mode_changed.connect(self.update_launch_mode_ui)
        self.status_text_changed.connect(self.main_window.update_status_text)
        self.app_version_label_changed.connect(self.main_window.update_app_version_label)
        self.translation_version_label_changed.connect(self.main_window.update_translation_version_label)
        self.show_update_app_button_changed.connect(self.main_window.button_update_app.setVisible)
        self.show_update_translation_button_changed.connect(self.main_window.button_update_translation.setVisible)

    def show_tutorial_popup(self):
        self.tutorial_popup.show()

    # MainWindowの表示
    def show_main_window(self):
        self.redraw()  # 初期描画
        self.main_window.show()

    # 各種イベントハンドラ
    def _on_radio_normal_clicked(self):
        if self._on_radio_normal_clicked_callback:
            self._on_radio_normal_clicked_callback(const.NORMAL_LAUNCH)

    def _on_radio_steam_clicked(self):
        if self._on_radio_steam_clicked_callback:
            self._on_radio_steam_clicked_callback(const.STEAM_LAUNCH)

    def _on_game_launch_clicked(self):
        if self._on_game_launch_clicked_callback:
            self._on_game_launch_clicked_callback()

    def _on_replace_translation_clicked(self):
        if self._on_replace_translation_clicked_callback:
            self._on_replace_translation_clicked_callback()

    def _on_update_app_clicked(self):
        if self._on_update_app_clicked_callback_data:
            filenames = self._on_update_app_clicked_callback_data[0]
            finished_callback = self._on_update_app_clicked_callback_data[1]
            self.start_download(self._download_app_files_callback, filenames, finished_callback)

    def _on_update_translation_clicked(self):
        if self._on_update_translation_clicked_callback_data:
            filenames = self._on_update_translation_clicked_callback_data[0]
            finished_callback = self._on_update_translation_clicked_callback_data[1]
            self.start_download(self._download_translation_files_callback, filenames, finished_callback)

    def _on_check_update_clicked(self):
        if self._on_check_update_clicked_callback:
            self._on_check_update_clicked_callback()

    def _on_settings_clicked(self):
        self.settings_popup.update_lineedit_local_path_text(self.get_property("local_path"))
        self.settings_popup.update_lineedit_app_server_url_text(self.get_property("app_update_server_url"))
        self.settings_popup.update_lineedit_translation_server_url_text(self.get_property("translation_update_server_url"))
        self.settings_popup.show()

    def _on_help_clicked(self):
        self.help_popup.show()

    def _on_local_path_browse_clicked(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(self.settings_popup, "Select Directory")
        if selected_path:
            self.set_property("local_path", selected_path)
            self.local_path_changed.emit(selected_path)

    def _on_main_window_close_event(self, event):
        event.accept()
        QApplication.quit()

    # UIの再描画
    def redraw(self):
        launch_mode = self.get_property("launch_mode")
        status_string = self.get_property("status_string")
        app_version = self.get_property("app_version")
        next_app_version = self.get_property("next_app_version")
        translation_version = self.get_property("translation_version")
        next_translation_version = self.get_property("next_translation_version")
        is_updatable_app = version.parse(next_app_version) > version.parse(app_version)
        is_updatable_translation = version.parse(next_translation_version) > version.parse(translation_version)

        # 起動モードのUI更新
        self.update_launch_mode_ui(launch_mode)

        # ステータスラベルの更新
        self.status_text_changed.emit(status_string)

        # バージョン表示の更新
        self.app_version_label_changed.emit(f"アプリバージョン: {app_version}")
        self.translation_version_label_changed.emit(f"翻訳バージョン: {translation_version}")

        # アップデートボタンの表示/非表示
        self.show_update_app_button_changed.emit(is_updatable_app)
        self.show_update_translation_button_changed.emit(is_updatable_translation)

    def update_launch_mode_ui(self, launch_mode):
        if launch_mode == const.NORMAL_LAUNCH:
            self.main_window.radio_normal.setChecked(True)
        elif launch_mode == const.STEAM_LAUNCH:
            self.main_window.radio_steam.setChecked(True)
        # 他のモードがあれば追加

    def update_status_text_ui(self, status_text):
        self.status_text_changed.emit(status_text)
        QApplication.processEvents()
