import sys
import os
from pathlib import Path


def setup_module_path():
    """モジュール検索パスを設定する"""
    # スクリプトのディレクトリパスを取得(exe化後も有効)
    script_dir = Path(__file__).resolve().parent

    # プロジェクトルートディレクトリを特定
    project_root_path = script_dir.parent

    # sys.pathへの追加は最後に行う
    sys.path.append(str(project_root_path))
    sys.path.append(str(script_dir))  # srcディレクトリも追加


def initialize_base_directory():
    """ベースディレクトリを初期化し、環境変数BASE_DIRに設定する"""
    print("Before initialize_base_directory")
    if getattr(sys, "frozen", False):
        # exe化された環境の場合
        base_dir = getattr(sys, "_MEIPASS", None)
        if not base_dir:
            # _MEIPASS が取得できない場合は、exeファイルのあるディレクトリを使う
            base_dir = os.path.dirname(sys.executable)
    else:
        # 通常のPython環境の場合
        base_dir = os.path.dirname(os.path.abspath(__file__))

    os.environ["BASE_DIR"] = base_dir
    print(f"After initialize_base_directory: base_dir={base_dir}")


setup_module_path()

from src.MainManager import MainManager
from src.UIManager import UIManager
from src.NetworkManager import RequestsNetworkManager
from src.ConfigManager import JsonConfigManager
from src.MockNetworkManager import MockNetworkManager

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

if __name__ == "__main__":
    initialize_base_directory()
    config_manager = JsonConfigManager(os.environ["BASE_DIR"])
    network_manager = MockNetworkManager(config_manager)
    main_manager = MainManager(config_manager, network_manager, os.environ["BASE_DIR"])  # base_dirを渡す
    print(f"After MainManager instantiation: config_manager={config_manager}, network_manager={network_manager}, base_dir={os.environ['BASE_DIR']}")
    main_manager.run()
    print("After main_manager.run()")
