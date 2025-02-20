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
    """ベースディレクトリとdataディレクトリを初期化し、環境変数に設定する"""

    if "__compiled__" in globals():
        # Nuitkaでコンパイルされた場合
        # sys.argv[0] は実行ファイルの絶対パス (バージョン2.4以降) or 実行ファイル名
        exe_path = Path(sys.argv[0])
        if not exe_path.is_absolute():
            exe_path = Path(os.path.abspath(sys.argv[0]))
        base_dir = exe_path.parent
        data_dir = base_dir / "data"  # onefileの場合はdataを同階層に置くことを想定
        print("Nuitka environment detected.")
    else:
        # 通常のPython環境
        # __file__ はスクリプトファイルの絶対パス
        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir.parent / "data"  # srcディレクトリの親がプロジェクトルート
        print("Normal Python environment detected.")

    os.environ["BASE_DIR"] = str(base_dir)
    os.environ["DATA_DIR"] = str(data_dir)
    print(f"initialize_base_directory: base_dir={base_dir}, data_dir={data_dir}")


setup_module_path()

if __name__ == "__main__":
    initialize_base_directory()

    main_manager = MainManager(os.environ["DATA_DIR"])
    main_manager.initialize()
