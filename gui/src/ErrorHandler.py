import logging
import traceback
from PySide6.QtWidgets import QMessageBox

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)  # ログレベルをINFOに設定
        self.show_gui = True
        self.gui_app = None

    def handle_error(self, error_type, error_message, main_window=None, stop_execution=False):
        """
        エラーを処理する。

        Args:
            error_type (str): エラーの種類。
            error_message (str): エラーメッセージ。
            main_window (QWidget, optional): メインウィンドウのインスタンス。デフォルトはNone。
            stop_execution (bool, optional): 実行を停止するかどうか。デフォルトはFalse。
        """
        # ログ出力
        self.logger.error(f"{error_type}: {error_message}")
        self.logger.error(traceback.format_exc())

        # GUI表示
        if self.show_gui and main_window:
            self.show_error_message(error_type, error_message, main_window)

        if stop_execution:
            # 実行を停止する場合の処理（必要に応じて）
            pass

    def show_error_message(self, error_type, error_message, main_window):
        """エラーメッセージをGUIに表示する"""
        # main_window.error_message_label.setText(f"{error_type}: {error_message}") # 修正前
        main_window.textedit_status.setText(f"{error_type}: {error_message}") # 修正後


    def log_message(self, message):
        """ログメッセージを出力する"""
        self.logger.info(message)
