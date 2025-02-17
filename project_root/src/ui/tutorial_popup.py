from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QTextEdit,
    QPushButton,
    QScrollArea,
    QLineEdit,
    QHBoxLayout,
    QFileDialog,
)
from PySide6.QtCore import Qt


class TutorialPopup(QWidget):
    def __init__(self, ui_manager):
        super().__init__()
        self.ui_manager = ui_manager
        self.setWindowTitle("ようこそ!")

        # チュートリアルメッセージ
        tutorial_text = """
        PlanetSide 2 日本語化ツールへようこそ！

        このツールを使うと、簡単に PlanetSide 2 を日本語化できます。

        まず、PlanetSide 2 がインストールされているフォルダを指定してください。
        """
        label_tutorial = QLabel(tutorial_text)
        label_tutorial.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        label_tutorial.setWordWrap(True)

        # スクロールエリア
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(label_tutorial)

        # ローカルパス設定
        label_local_path = QLabel("PlanetSide 2 インストールフォルダ:")
        self.lineedit_local_path = QLineEdit()
        button_local_path = QPushButton("参照...")
        button_local_path.clicked.connect(self.browse_local_path)

        hbox_local_path = QHBoxLayout()
        hbox_local_path.addWidget(label_local_path)
        hbox_local_path.addWidget(self.lineedit_local_path)
        hbox_local_path.addWidget(button_local_path)

        # textEditedシグナルに接続
        self.lineedit_local_path.textEdited.connect(self._on_lineedit_local_path_text_edited)

        # レイアウト
        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        layout.addLayout(hbox_local_path)
        self.setLayout(layout)

        # ウィンドウサイズを固定
        self.setFixedSize(400, 175)
        # 最大化ボタンを無効化
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint)

    def browse_local_path(self):
        file_dialog = QFileDialog()
        selected_path = file_dialog.getExistingDirectory(self, "Select Directory")
        if selected_path:
            self.lineedit_local_path.setText(selected_path)
            self.ui_manager.set_property("local_path", selected_path)

    def _on_lineedit_local_path_text_edited(self, text):
        self.ui_manager.set_property("local_path", text)
        self.ui_manager.local_path_changed.emit(text)

    def closeEvent(self, event):
        event.accept()