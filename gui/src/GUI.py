from PySide6.QtWidgets import QApplication
from gui.src.MainWindow import MainWindow
import sys


class GuiApp:
    def __init__(self, main_manager):
        self.app = QApplication(sys.argv)
        self.main_manager = main_manager
        self.main_window = MainWindow(self.main_manager)

    def run(self):
        self.main_manager.gui_app = self  # MainManagerにGuiAppのインスタンスを設定
        self.main_window.show()
        sys.exit(self.app.exec())
