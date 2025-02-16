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
from ui.settings_popup import SettingsPopup
from ui.help_popup import HelpPopup


class MainWindow(QMainWindow):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager
        print("MainWindow initialized")
        self.setWindowTitle("PS2 日本語化")
        print("MainWindow.setWindowTitle called")
        self.set_icons()
        print("MainWindow.set_icons called")
        self.init_ui()
        print("MainWindow.init_ui called")
        self.setup_layout()
        print("MainWindow.setup_layout called")
        self.setFixedSize(270, 350)
        print("MainWindow.setFixedSize called")
        # 設定ポップアップのインスタンス
        self.settings_popup = SettingsPopup()
        print("MainWindow.settings_popup initialized")
        self.help_popup = HelpPopup()
        print("MainWindow.help_popup initialized")

        self.setup_callbacks()  # コールバック設定

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

        # ローカルパス

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
        self.button_settings.setIcon(self.style().standardIcon(QStyle.SP_FileDialogListView))
        self.button_settings.setIconSize(QSize(24, 24))
        self.button_settings.setFixedSize(30, 30)
        self.button_settings.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        print("MainWindow.button_settings initialized")

        # ヘルプボタン (仮)
        self.button_help = QPushButton()
        self.button_help.setIcon(self.style().standardIcon(QStyle.SP_MessageBoxQuestion))
        self.button_help.setIconSize(QSize(24, 24))
        self.button_help.setFixedSize(30, 30)
        self.button_help.setStyleSheet("QPushButton { background-color: transparent; border: none; }")
        print("MainWindow.button_help initialized")

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
        grid_version.addWidget(self.button_check_update, 2, 0, 2, 2)  # Span two columns
        grid_version.setRowStretch(2, 1)
        # ローカルパス (ラベル)
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

    def setup_callbacks(self):
        # 各種コールバック関数の初期化 (Noneで初期化)
        self.radio_normal_callback = None
        self.radio_steam_callback = None
        self.button_game_launch_callback = None
        self.button_replace_translation_callback = None
        self.button_update_app_callback = None
        self.button_update_translation_callback = None
        self.button_check_update_callback = None
        self.button_settings_callback = None
        self.button_help_callback = None
        self.close_event_callback = None

        # 既存の接続を解除してから新しいコールバック関数を接続
        self.radio_normal.clicked.disconnect()
        self.radio_normal.clicked.connect(self._on_radio_normal_clicked)

        self.radio_steam.clicked.disconnect()
        self.radio_steam.clicked.connect(self._on_radio_steam_clicked)

        self.button_game_launch.clicked.disconnect()
        self.button_game_launch.clicked.connect(self._on_button_game_launch_clicked)

        self.button_replace_translation.clicked.disconnect()
        self.button_replace_translation.clicked.connect(self._on_button_replace_translation_clicked)

        self.button_update_app.clicked.disconnect()
        self.button_update_app.clicked.connect(self._on_button_update_app_clicked)

        self.button_update_translation.clicked.disconnect()
        self.button_update_translation.clicked.connect(self._on_button_update_translation_clicked)

        self.button_check_update.clicked.disconnect()
        self.button_check_update.clicked.connect(self._on_button_check_update_clicked)

        self.button_settings.clicked.disconnect()
        self.button_settings.clicked.connect(self._on_button_settings_clicked)

        self.button_help.clicked.disconnect()
        self.button_help.clicked.connect(self._on_button_help_clicked)


    # コールバック関数登録用のメソッド
    def set_radio_normal_callback(self, callback):
        self.radio_normal_callback = callback

    def set_radio_steam_callback(self, callback):
        self.radio_steam_callback = callback

    def set_button_game_launch_callback(self, callback):
        self.button_game_launch_callback = callback

    def set_button_replace_translation_callback(self, callback):
        self.button_replace_translation_callback = callback

    def set_button_update_app_callback(self, callback):
        self.button_update_app_callback = callback

    def set_button_update_translation_callback(self, callback):
        self.button_update_translation_callback = callback

    def set_button_check_update_callback(self, callback):
        self.button_check_update_callback = callback

    def set_button_settings_callback(self, callback):
        self.button_settings_callback = callback

    def set_button_help_callback(self, callback):
        self.button_help_callback = callback

    def set_close_event_callback(self, callback):
        self.close_event_callback = callback

    # 内部で呼ばれる実際の処理
    def _on_radio_normal_clicked(self):
        if self.radio_normal_callback:
            self.radio_normal_callback()

    def _on_radio_steam_clicked(self):
        if self.radio_steam_callback:
            self.radio_steam_callback()

    def _on_button_game_launch_clicked(self):
        if self.button_game_launch_callback:
            self.button_game_launch_callback()

    def _on_button_replace_translation_clicked(self):
        if self.button_replace_translation_callback:
            self.button_replace_translation_callback()

    def _on_button_update_app_clicked(self):
        if self.button_update_app_callback:
            self.button_update_app_callback()

    def _on_button_update_translation_clicked(self):
        if self.button_update_translation_callback:
            self.button_update_translation_callback()

    def _on_button_check_update_clicked(self):
        if self.button_check_update_callback:
            self.button_check_update_callback()

    def _on_button_settings_clicked(self):
        if self.button_settings_callback:
            self.button_settings_callback()

    def _on_button_help_clicked(self):
        if self.button_help_callback:
            self.button_help_callback()

    def closeEvent(self, event):
        if self.close_event_callback:
            # コールバックが設定されている場合、それを呼び出す
            # (注) コールバック側で閉じたくない場合は event.ignore() を呼び出す
            self.close_event_callback(event)
            if event.isAccepted():  # コールバック側でeventがacceptされていれば閉じる
                print("ユーザーによってアプリケーションは閉じられました")
        else:
            # コールバックが設定されていない場合、デフォルトの閉じ処理
            event.accept()
            print("ユーザーによってアプリケーションは閉じられました")

    # ラベル更新用のメソッド
    def update_app_version_label(self, text):
        self.label_app_version.setText(text)

    def update_translation_version_label(self, text):
        self.label_translation_version.setText(text)

    def update_status_text(self, text):
        self.textedit_status.setText(text)
