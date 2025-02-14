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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("設定")

        # UI要素を初期化
        self.init_ui()

        # レイアウトを設定
        self.setup_layout()

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

    def setup_connections(self, ui_manager):
        self.button_local_path.clicked.connect(lambda: self.open_file_dialog(ui_manager))

    def open_file_dialog(self, ui_manager):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder_path:
            self.lineedit_local_path.setText(folder_path)
            ui_manager.set_local_path(folder_path)
