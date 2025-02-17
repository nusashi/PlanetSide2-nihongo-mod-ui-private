from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt


class HelpPopup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ヘルプ")

        # ヘルプテキスト (複数行)
        help_text = """
        このツールは、PlanetSide 2 の日本語化を支援します。

        使い方:

        1. **ゲームフォルダ位置指定:** PlanetSide 2 がインストールされているフォルダを指定します。
        2. **起動モード:** 通常起動またはSteam経由起動を選択します。
        3. **ゲーム起動:** 選択したモードでゲームを起動します。
        4. **日本語化:** 日本語化ファイルをゲームフォルダにコピーします。
        5. **アップデート確認:** アプリケーションと翻訳ファイルのアップデートを確認します。
        6. **設定:** インストールフォルダや、サーバーURLなどを設定します。
        7. **ヘルプ:** このヘルプを表示します。

        詳細については、README.mdを参照してください。
        """
        self.label_help = QLabel(help_text)
        self.label_help.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)  # 左上
        self.label_help.setWordWrap(True)  # 折り返しを有効にする

        # レイアウト
        layout = QVBoxLayout()
        layout.addWidget(self.label_help)
        self.setLayout(layout)
