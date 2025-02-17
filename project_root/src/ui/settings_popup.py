from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QFileDialog,
)
from PySide6.QtCore import Qt


class SettingsPopup(QWidget):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager
        self.setWindowTitle("設定")
        # UI要素を初期化
        self.init_ui()
        # レイアウトを設定
        self.setup_layout()
        self.setup_callbacks()  # コールバック初期化

        # ウィンドウサイズを固定
        self.setFixedSize(400, 300)
        # 最大化ボタンを無効化
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

    def init_ui(self):
        # ゲームフォルダ位置指定
        self.label_local_path = QLabel("ローカルパス:")
        self.lineedit_local_path = QLineEdit()
        self.button_local_path = QPushButton("参照...")

        # サーバーURL設定
        self.label_app_server_url = QLabel("アプリサーバーURL:")
        self.lineedit_app_server_url = QLineEdit()
        self.label_translation_server_url = QLabel("翻訳サーバーURL:")
        self.lineedit_translation_server_url = QLineEdit()

        # 作者クレジット
        self.label_author = QLabel("Authors: A, B, C")  # Replace with actual author names
        # ライセンス表示 (仮)
        self.label_license = QLabel("License: MIT License")  # Replace with actual license

    def setup_layout(self):
        # ゲームフォルダ位置指定
        groupbox_local_path = QGroupBox("ゲームフォルダ位置指定")
        hbox_local_path = QHBoxLayout()
        hbox_local_path.addWidget(self.label_local_path)
        hbox_local_path.addWidget(self.lineedit_local_path)
        hbox_local_path.addWidget(self.button_local_path)
        groupbox_local_path.setLayout(hbox_local_path)

        # サーバーURL設定
        groupbox_server_url = QGroupBox("サーバーURL")
        vbox_server_url = QVBoxLayout()
        vbox_server_url.addWidget(self.label_app_server_url)
        vbox_server_url.addWidget(self.lineedit_app_server_url)
        vbox_server_url.addWidget(self.label_translation_server_url)
        vbox_server_url.addWidget(self.lineedit_translation_server_url)
        groupbox_server_url.setLayout(vbox_server_url)

        # 作者クレジット
        hbox_author = QHBoxLayout()
        hbox_author.addWidget(self.label_author)
        hbox_author.setAlignment(Qt.AlignmentFlag.AlignRight)  # Right-align

        # ライセンス表示 (仮)
        hbox_license = QHBoxLayout()
        hbox_license.addWidget(self.label_license)
        hbox_license.setAlignment(Qt.AlignmentFlag.AlignRight)

        # メインレイアウト
        main_layout = QVBoxLayout()
        main_layout.addWidget(groupbox_local_path)
        main_layout.addWidget(groupbox_server_url)
        main_layout.addLayout(hbox_author)
        main_layout.addLayout(hbox_license)
        self.setLayout(main_layout)

    def setup_callbacks(self):
        # コールバック関数の初期化
        self.button_local_path_callback = None

        # 既存の接続を解除
        self.button_local_path.clicked.disconnect()
        # 新しいコールバック関数を接続
        self.button_local_path.clicked.connect(self._on_button_local_path_clicked)

        # textEditedシグナルに接続
        self.lineedit_local_path.textEdited.connect(self._on_lineedit_local_path_text_edited)
        self.lineedit_app_server_url.textEdited.connect(self._on_lineedit_app_server_url_text_edited)
        self.lineedit_translation_server_url.textEdited.connect(self._on_lineedit_translation_server_url_text_edited)

    def set_button_local_path_callback(self, callback):
        self.button_local_path_callback = callback

    def _on_button_local_path_clicked(self):
        if self.button_local_path_callback:
            self.button_local_path_callback()

    def _on_lineedit_local_path_text_edited(self, text):
        self.ui_manager.set_property("local_path", text)
        self.ui_manager.local_path_changed.emit(text)

    def _on_lineedit_app_server_url_text_edited(self, text):
        self.ui_manager.set_property("app_update_server_url", text)
        self.ui_manager.app_update_server_url_changed.emit(text)

    def _on_lineedit_translation_server_url_text_edited(self, text):
        self.ui_manager.set_property("translation_update_server_url", text)
        self.ui_manager.translation_update_server_url_changed.emit(text)

    # 各ラベルとラインエディットのテキストを更新するメソッド
    def update_label_local_path_text(self, text):
        self.label_local_path.setText(text)

    def update_lineedit_local_path_text(self, text):
        self.lineedit_local_path.setText(text)

    def update_label_app_server_url_text(self, text):
        self.label_app_server_url.setText(text)

    def update_lineedit_app_server_url_text(self, text):
        self.lineedit_app_server_url.setText(text)

    def update_label_translation_server_url_text(self, text):
        self.label_translation_server_url.setText(text)

    def update_lineedit_translation_server_url_text(self, text):
        self.lineedit_translation_server_url.setText(text)

    def update_label_author_text(self, text):
        self.label_author.setText(text)

    def update_label_license_text(self, text):
        self.label_license.setText(text)
