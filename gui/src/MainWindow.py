from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QMessageBox,
    QCheckBox,
    QComboBox,
    QSystemTrayIcon,
    QMenu,
    QGroupBox,
    QGridLayout,
    QTextEdit,
    QRadioButton,
    QSizePolicy,
    QStyle,
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QFontMetrics
from src.settings_popup import SettingsPopup
from src.help_popup import HelpPopup


class MainWindow(QMainWindow):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager
        print("MainWindow initialized")
        self.setWindowTitle("PS2 日本語化")
        print("MainWindow.setWindowTitle called")
        # self.set_icons()
        print("MainWindow.set_icons called")
        self.init_ui()
        print("MainWindow.init_ui called")
        # self.setup_layout() # コメントアウト
        # print("MainWindow.setup_layout called")
        self.setFixedSize(270, 350)
        print("MainWindow.setFixedSize called")

        # 設定ポップアップのインスタンス
        self.settings_popup = SettingsPopup()
        print("MainWindow.settings_popup initialized")
        self.help_popup = HelpPopup()
        print("MainWindow.help_popup initialized")

    def set_icons(self):
        print("MainWindow.set_icons called")
        # Use standard icons
        self.app_icon = self.style().standardIcon(QStyle.SP_VistaShield)
        if not self.app_icon.isNull():
            self.setWindowIcon(self.app_icon)
            print("MainWindow.setWindowIcon called")

        if QSystemTrayIcon.isSystemTrayAvailable():
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(self.app_icon)
            tray_menu = QMenu(self)
            tray_menu.addAction("表示", self.show)
            tray_menu.addAction("終了", QApplication.quit)
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.show()
            print("MainWindow.tray_icon setup done")
        else:
            print("System tray is not available.")
        print("MainWindow.set_icons finished")

    def init_ui(self):
        print("MainWindow.init_ui called")
        # 起動モード
        self.radio_normal = QRadioButton("通常起動")
        print("MainWindow.radio_normal initialized")
        self.radio_steam = QRadioButton("Steam起動")
        print("MainWindow.radio_steam initialized")

        # ゲーム起動/ファイル置き換えボタン
        self.button_game_launch = QPushButton("1:ゲーム起動")
        height = self.button_game_launch.sizeHint().height()
        self.button_game_launch.setFixedHeight(height * 2)
        print("MainWindow.button_game_launch initialized")
        self.button_replace_translation = QPushButton("2:日本語化")
        height = self.button_replace_translation.sizeHint().height()
        self.button_replace_translation.setFixedHeight(height * 2)
        print("MainWindow.button_replace_translation initialized")

        # バージョン情報/アップデート
        self.label_app_version = QLabel("アプリバージョン: x.x.x")
        print("MainWindow.label_app_version initialized")
        self.button_update_app = QPushButton("更新")
        size_hint = self.button_update_app.sizeHint()
        self.button_update_app.setFixedSize(size_hint)
        self.button_update_app.setVisible(False)  # Initially hidden
        print("MainWindow.button_update_app initialized")
        self.label_translation_version = QLabel("翻訳バージョン: x.x.x")
        print("MainWindow.label_translation_version initialized")
        self.button_update_translation = QPushButton("更新")
        size_hint = self.button_update_translation.sizeHint()
        self.button_update_translation.setFixedSize(size_hint)
        self.button_update_translation.setVisible(False)  # Initially hidden
        print("MainWindow.button_update_translation initialized")

        self.button_check_update = QPushButton("アップデート確認")
        print("MainWindow.button_check_update initialized")

        # ステータス
        self.textedit_status = QTextEdit()
        self.textedit_status.setReadOnly(True)
        self.textedit_status.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        font_metrics = self.textedit_status.fontMetrics()
        line_height = font_metrics.lineSpacing()
        self.textedit_status.setFixedHeight(line_height * 3)
        print("MainWindow.textedit_status initialized")

        # 設定ボタン
        self.button_settings = QPushButton()
        self.button_settings.setIcon(
            self.style().standardIcon(QStyle.SP_FileDialogListView)
        )
        self.button_settings.setIconSize(QSize(24, 24))
        self.button_settings.setFixedSize(30, 30)
        self.button_settings.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }"
        )
        self.button_settings.clicked.connect(self.ui_manager.open_settings_popup)
        print("MainWindow.button_settings initialized")

        # ヘルプボタン (仮)
        self.button_help = QPushButton()
        self.button_help.setIcon(
            self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        )
        self.button_help.setIconSize(QSize(24, 24))
        self.button_help.setFixedSize(30, 30)
        self.button_help.setStyleSheet(
            "QPushButton { background-color: transparent; border: none; }"
        )
        self.button_help.clicked.connect(self.open_help)
        print("MainWindow.button_help initialized")

        # コンボボックスの選択肢が変更されたときに呼ばれる
        self.combobox_launch_mode = QComboBox()
        self.combobox_launch_mode.currentIndexChanged.connect(self.launch_mode_changed)
        print("MainWindow.combobox_launch_mode initialized")
        print("MainWindow.init_ui finished")

    def setup_layout(self):
        print("MainWindow.setup_layout called")
        # 起動モード
        groupbox_launch_mode = QGroupBox("起動モード")
        hbox_launch_mode = QHBoxLayout()
        hbox_launch_mode.addWidget(self.radio_normal)
        hbox_launch_mode.addWidget(self.radio_steam)
        groupbox_launch_mode.setLayout(hbox_launch_mode)
        groupbox_launch_mode.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        print("MainWindow.groupbox_launch_mode setup done")

        # ゲーム起動/ファイル置き換えボタン
        hbox_buttons = QHBoxLayout()
        hbox_buttons.addWidget(self.button_game_launch)
        hbox_buttons.addWidget(self.button_replace_translation)
        print("MainWindow.hbox_buttons setup done")

        # バージョン情報/アップデート
        groupbox_version = QGroupBox("バージョン情報")
        grid_version = QGridLayout()
        grid_version.addWidget(self.label_app_version, 0, 0)
        grid_version.addWidget(self.button_update_app, 0, 1)
        grid_version.addWidget(self.label_translation_version, 1, 0)
        grid_version.addWidget(self.button_update_translation, 1, 1)
        grid_version.addWidget(self.button_check_update, 2, 0, 1, 2)  # Span two columns
        groupbox_version.setLayout(grid_version)
        print("MainWindow.groupbox_version setup done")

        # ステータス
        groupbox_status = QGroupBox("ステータス")
        vbox_status = QVBoxLayout()
        vbox_status.addWidget(self.textedit_status)
        groupbox_status.setLayout(vbox_status)
        print("MainWindow.groupbox_status setup done")

        # メインレイアウト
        main_layout = QVBoxLayout()

        # 設定ボタンとヘルプボタンを起動モードの右側に追加
        hbox_settings = QHBoxLayout()
        hbox_settings.addWidget(groupbox_launch_mode)
        hbox_settings.addStretch()  # 右寄せにする
        hbox_settings.addWidget(self.button_help)
        hbox_settings.addWidget(self.button_settings)
        main_layout.addLayout(hbox_settings)
        print("MainWindow.hbox_settings setup done")

        main_layout.addLayout(hbox_buttons)
        main_layout.addWidget(groupbox_status)  # Moved up
        main_layout.addWidget(groupbox_version)

        # centralwidget を作成して main_layout を設定
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)  # centralwidget をセット

        print("MainWindow.setup_layout finished")

    def check_updates(self):
        print("MainWindow.check_updates called")
        # Check for updates and show/hide buttons accordingly
        self.ui_manager.check_updates()
        self.button_update_app.setVisible(True)
        self.button_update_translation.setVisible(True)
        print("MainWindow.check_updates finished")

    def launch_game(self):
        print("MainWindow.launch_game called")
        # Get the selected launch mode and local path
        mode = self.combobox_launch_mode.currentText()
        local_path = self.ui_manager.main_manager.get_config("local_path")

        # Check if local_path is set
        if not local_path:
            QMessageBox.critical(
                self,
                "エラー",
                "ローカルパスが設定されていません。\n設定画面から設定してください。",
            )
            return

        # Call the launch_game method in UIManager
        self.ui_manager.launch_game(mode, local_path)
        print("MainWindow.launch_game finished")

    def copy_translation_files(self):
        print("MainWindow.copy_translation_files called")
        local_path = self.ui_manager.main_manager.get_config("local_path")

        # Check if local_path is set
        if not local_path:
            QMessageBox.critical(
                self,
                "エラー",
                "ローカルパスが設定されていません。\n設定画面から設定してください。",
            )
            return
        self.ui_manager.copy_translation_files(local_path)
        QMessageBox.information(self, "情報", "翻訳ファイルをコピーしました。")
        print("MainWindow.copy_translation_files finished")

    def open_settings_popup(self):
        print("MainWindow.open_settings_popup called")
        self.ui_manager.open_settings_popup()
        print("MainWindow.open_settings_popup finished")

    def closeEvent(self, event):
        print("MainWindow.closeEvent called")
        # Ask for confirmation before closing
        reply = QMessageBox.question(
            self,
            "確認",
            "アプリケーションを終了しますか？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        print("MainWindow.closeEvent finished")

    def open_help(self):
        print("MainWindow.open_help called")
        self.help_popup.show()
        print("MainWindow.open_help finished")

    def setup_connections(self):
        print("MainWindow.setup_connections called")
        self.radio_normal.clicked.connect(
            lambda: self.ui_manager.set_launch_mode(0)
        )
        self.radio_steam.clicked.connect(
            lambda: self.ui_manager.set_launch_mode(1)
        )
        self.button_check_update.clicked.connect(self.ui_manager.check_updates)
        self.button_update_app.clicked.connect(self.ui_manager.update_data)
        self.button_update_translation.clicked.connect(self.ui_manager.update_data)
        self.button_launch_game.clicked.connect(self.launch_game)
        self.button_replace_translation.clicked.connect(self.copy_translation_files)
        self.button_settings.clicked.connect(self.ui_manager.open_settings_popup)
        self.button_help.clicked.connect(self.open_help)
        print("MainWindow.setup_connections finished")

    def launch_mode_changed(self):
        print("MainWindow.launch_mode_changed called")
        """
        起動モードが変更されたときに呼ばれる
        """
        mode = self.combobox_launch_mode.currentIndex()
        print(f"MainWindow.launch_mode_changed: mode={mode}")
        self.ui_manager.set_launch_mode(mode)
        print("MainWindow.launch_mode_changed finished")

    def set_launch_mode_on_startup(self, mode: int):
        print("MainWindow.set_launch_mode_on_startup called")
        """
        起動時に起動モードを設定する
        """
        if mode == 0:
            self.radio_normal.setChecked(True)
            print("MainWindow.radio_normal checked")
        elif mode == 1:
            self.radio_steam.setChecked(True)
            print("MainWindow.radio_steam checked")
