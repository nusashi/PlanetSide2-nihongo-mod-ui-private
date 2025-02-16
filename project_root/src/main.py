import sys
import os
from pathlib import Path

from system.main_manager import MainManager

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
    print(f"initialize_base_directory: base_dir={base_dir}")


setup_module_path()

if __name__ == "__main__":
    initialize_base_directory()

    main_manager = MainManager()