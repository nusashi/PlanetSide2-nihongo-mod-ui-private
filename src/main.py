import sys
import os
import ctypes
import ctypes.wintypes
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
        try:
            # Windows APIで実行ファイルパスを取得（最も信頼性が高い）
            # まずMAX_PATHでトライ
            buffer_size = ctypes.wintypes.MAX_PATH
            buffer = ctypes.create_unicode_buffer(buffer_size)
            ret = ctypes.windll.kernel32.GetModuleFileNameW(0, buffer, buffer_size)

            # バッファサイズが不足している場合
            if ret == buffer_size:
                # より大きなバッファでリトライ
                buffer_size = 8192  # 8KB
                buffer = ctypes.create_unicode_buffer(buffer_size)
                ret = ctypes.windll.kernel32.GetModuleFileNameW(0, buffer, buffer_size)

            # エラー発生時
            if ret == 0:
                error_code = ctypes.GetLastError()
                print(f"Warning: GetModuleFileNameW failed with error code {error_code}")
                # フォールバック: sys.argv[0]を使用
                exe_path = Path(os.path.abspath(sys.argv[0]))
            else:
                exe_path = Path(buffer.value)

        except Exception as e:
            # 何らかの例外が発生した場合
            print(f"Warning: Exception occurred while getting executable path: {e}")
            # フォールバック: sys.argv[0]を使用
            exe_path = Path(os.path.abspath(sys.argv[0]))

        base_dir = exe_path.parent
        data_dir = base_dir / "data"  # onefileの場合はdataを同階層に置くことを想定
        print(f"Nuitka environment detected. Executable path: {exe_path}")
    else:
        # 通常のPython環境
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
