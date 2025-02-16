import sys
import os
from pathlib import Path

from system.main_manager import MainManager
from ui.ui_manager import UIManager


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
    """ベースディレクトリとdataディレクトリを初期化し、環境変数に設定する"""
    if getattr(sys, "frozen", False):
        # exe化された環境の場合
        base_dir = getattr(sys, "_MEIPASS", None)
        if not base_dir:
            # _MEIPASS が取得できない場合は、exeファイルのあるディレクトリを使う
            base_dir = Path(sys.executable).resolve().parent
        data_dir = Path(sys.executable).resolve().parent / "data"
    else:
        # 通常のPython環境の場合
        base_dir = Path(__file__).resolve().parent
        data_dir = Path(__file__).resolve().parent.parent / "data"  # srcディレクトリの親がプロジェクトルート

    os.environ["BASE_DIR"] = str(base_dir)
    os.environ["DATA_DIR"] = str(data_dir)

    print(f"initialize_base_directory: base_dir={base_dir}, data_dir={data_dir}")


setup_module_path()

if __name__ == "__main__":
    initialize_base_directory()

    main_manager = MainManager(os.environ["DATA_DIR"])
    ui_manager = UIManager(main_manager)
    ui_manager.run()
