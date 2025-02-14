import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction, QIcon
from settings_popup import SettingsPopup
from help_popup import HelpPopup

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QRadioButton, QLineEdit, QProgressBar, QFrame, QGroupBox, QTextEdit, QMenuBar, QMenu, QSizePolicy, QGridLayout, QStyle


class PreviewWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI Preview")

        # 各セクションのUI要素を定義
        self.init_ui()

        # レイアウトを設定
        self.setup_layout()

        self.resize(400, 450)  #  高さを調整

        # 設定ポップアップのインスタンス
        self.settings_popup = SettingsPopup()

    def init_ui(self):
        # 起動モード
        self.radio_normal = QRadioButton("通常起動")
        self.radio_steam = QRadioButton("Steam起動")

        # ゲーム起動/ファイル置き換えボタン
        self.button_game_launch = QPushButton("1:ゲーム起動")
        height = self.button_game_launch.sizeHint().height()
        self.button_game_launch.setFixedHeight(height * 2)
        self.button_replace_translation = QPushButton("2:日本語化")
        height = self.button_replace_translation.sizeHint().height()
        self.button_replace_translation.setFixedHeight(height * 2)

        # バージョン情報/アップデート
        self.label_app_version = QLabel("アプリバージョン: x.x.x")
        self.button_update_app = QPushButton("更新")
        size_hint = self.button_update_app.sizeHint()
        self.button_update_app.setFixedSize(size_hint)
        self.button_update_app.setVisible(False)  # Initially hidden
        self.label_translation_version = QLabel("翻訳バージョン: x.x.x")
        self.button_update_translation = QPushButton("更新")
        size_hint = self.button_update_translation.sizeHint()
        self.button_update_translation.setFixedSize(size_hint)
        self.button_update_translation.setVisible(False)  # Initially hidden

        self.button_check_update = QPushButton("アップデート確認")

        # ステータス
        self.textedit_status = QTextEdit()
        self.textedit_status.setReadOnly(True)
        self.textedit_status.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        font_metrics = self.textedit_status.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.textedit_status.setFixedHeight(line_height * 3)

        # 設定ボタン
        self.button_settings = QPushButton()
        self.button_settings.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.button_settings.setIconSize(QSize(24, 24))
        self.button_settings.setFixedSize(30, 30)
        self.button_settings.clicked.connect(self.open_settings)
        self.button_settings.setStyleSheet("QPushButton { background-color: transparent; border: none; }")

        # ヘルプボタン (仮)
        self.button_help = QPushButton()
        self.button_help.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.button_help.setIconSize(QSize(24, 24))
        self.button_help.setFixedSize(30, 30)
        self.button_help.clicked.connect(self.open_help)
        self.button_help.setStyleSheet("QPushButton { background-color: transparent; border: none; }")

    def setup_layout(self):
        # 起動モード
        groupbox_launch_mode = QGroupBox("起動モード")
        hbox_launch_mode = QHBoxLayout()
        hbox_launch_mode.addWidget(self.radio_normal)
        hbox_launch_mode.addWidget(self.radio_steam)
        groupbox_launch_mode.setLayout(hbox_launch_mode)
        groupbox_launch_mode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        # ゲーム起動/ファイル置き換えボタン
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.button_game_launch)
        hbox_buttons.addWidget(self.button_replace_translation)

        # バージョン情報/アップデート
        groupbox_version = QGroupBox("バージョン情報")
        grid_version = QGridLayout()
        grid_version.addWidget(self.label_app_version, 0, 0)
        grid_version.addWidget(self.button_update_app, 0, 1)
        grid_version.addWidget(self.label_translation_version, 1, 0)
        grid_version.addWidget(self.button_update_translation, 1, 1)
        grid_version.addWidget(self.button_check_update, 2, 0, 1, 2)  # Span two columns
        groupbox_version.setLayout(grid_version)

        # ステータス
        groupbox_status = QGroupBox("ステータス")
        vbox_status = QVBoxLayout()
        vbox_status.addWidget(self.textedit_status)
        groupbox_status.setLayout(vbox_status)

        # メインレイアウト
        main_layout = QVBoxLayout()

        # 設定ボタンとヘルプボタンを起動モードの右側に追加
        hbox_settings = QHBoxLayout()
        hbox_settings.addWidget(groupbox_launch_mode)
        hbox_settings.addStretch()  # 右寄せにする
        hbox_settings.addWidget(self.button_help)
        hbox_settings.addWidget(self.button_settings)
        main_layout.addLayout(hbox_settings)

        main_layout.addLayout(hbox_buttons)
        main_layout.addWidget(groupbox_status)  # Moved up
        main_layout.addWidget(groupbox_version)
        self.setLayout(main_layout)
        self.setFixedSize(self.sizeHint())  # ウィンドウサイズを固定

        # ヘルプポップアップのインスタンス
        self.help_popup = HelpPopup()

    def open_settings(self):
        if self.settings_popup.isVisible():
            self.settings_popup.hide()
        else:
            self.settings_popup.show()

    def open_help(self):
        self.help_popup.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreviewWindow()
    window.show()
    sys.exit(app.exec())
