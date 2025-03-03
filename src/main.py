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

    # デバッグ情報の出力開始
    print("\n[PATH] ----- パス検出診断情報 -----")
    print(f"[PATH] Python情報: {sys.version}")
    print(f"[PATH] コマンドライン引数: {sys.argv}")
    print(f"[PATH] 現在の作業ディレクトリ: {os.getcwd()}")

    # 一時フォルダパスかどうかを判定する関数
    def is_temp_path(path_str):
        if not path_str or not isinstance(path_str, str):
            return False
        temp_indicators = ["temp", "tmp", "onefile_", "appdata\\local\\temp"]
        path_lower = path_str.lower()
        return any(indicator in path_lower for indicator in temp_indicators)

    if "__compiled__" in globals():
        print("[PATH] Nuitka環境を検出しました")

        # 利用可能なパス情報を収集・出力
        paths = {}

        # 1. sys.argv[0]の情報
        if sys.argv:
            paths["argv"] = sys.argv[0]
            print(f"[PATH] sys.argv[0]: {paths['argv']}")
            print(f"[PATH]   - 絶対パス？: {os.path.isabs(paths['argv'])}")
            print(f"[PATH]   - 存在する？: {os.path.exists(paths['argv'])}")
            print(f"[PATH]   - 一時フォルダ？: {is_temp_path(paths['argv'])}")

            # 相対パスなら絶対パスに変換
            if not os.path.isabs(paths["argv"]):
                paths["argv_abs"] = os.path.abspath(paths["argv"])
                print(f"[PATH] sys.argv[0]（絶対パス変換後）: {paths['argv_abs']}")
                print(f"[PATH]   - 存在する？: {os.path.exists(paths['argv_abs'])}")
                print(f"[PATH]   - 一時フォルダ？: {is_temp_path(paths['argv_abs'])}")

        # 2. GetModuleFileNameWの情報
        try:
            import ctypes

            buffer = ctypes.create_unicode_buffer(1024)
            result = ctypes.windll.kernel32.GetModuleFileNameW(0, buffer, 1024)
            if result > 0:
                paths["module"] = buffer.value
                print(f"[PATH] GetModuleFileNameW: {paths['module']}")
                print(f"[PATH]   - 存在する？: {os.path.exists(paths['module'])}")
                print(f"[PATH]   - 一時フォルダ？: {is_temp_path(paths['module'])}")
        except Exception as e:
            print(f"[PATH] GetModuleFileNameW呼び出し失敗: {e}")

        # 3. sys.executableの情報
        if sys.executable:
            paths["executable"] = sys.executable
            print(f"[PATH] sys.executable: {paths['executable']}")
            print(f"[PATH]   - 存在する？: {os.path.exists(paths['executable'])}")
            print(f"[PATH]   - 一時フォルダ？: {is_temp_path(paths['executable'])}")

        # 最適なパスを選択するロジック
        print("[PATH] 最適なパスを判定しています...")

        # 優先順位1: sys.argv[0]が絶対パスで、存在し、一時フォルダではない
        if "argv" in paths and os.path.isabs(paths["argv"]) and os.path.exists(paths["argv"]) and not is_temp_path(paths["argv"]):
            exe_path = Path(paths["argv"])
            print(f"[PATH] 判定結果: sys.argv[0]を使用（絶対パス・実在・非一時フォルダ）")

        # 優先順位2: 絶対パス変換したsys.argv[0]が存在し、一時フォルダではない
        elif "argv_abs" in paths and os.path.exists(paths["argv_abs"]) and not is_temp_path(paths["argv_abs"]):
            exe_path = Path(paths["argv_abs"])
            print(f"[PATH] 判定結果: 絶対パス変換したsys.argv[0]を使用（実在・非一時フォルダ）")

        # 以下、他の選択肢
        elif "module" in paths and not is_temp_path(paths["module"]):
            exe_path = Path(paths["module"])
            print(f"[PATH] 判定結果: GetModuleFileNameWを使用（非一時フォルダ）")
        elif "executable" in paths and not is_temp_path(paths["executable"]):
            exe_path = Path(paths["executable"])
            print(f"[PATH] 判定結果: sys.executableを使用（非一時フォルダ）")
        elif "argv" in paths:
            exe_path = Path(paths["argv"])
            print(f"[PATH] 判定結果（フォールバック）: sys.argv[0]を使用")
        elif "module" in paths:
            exe_path = Path(paths["module"])
            print(f"[PATH] 判定結果（フォールバック）: GetModuleFileNameWを使用")
        elif "executable" in paths:
            exe_path = Path(paths["executable"])
            print(f"[PATH] 判定結果（フォールバック）: sys.executableを使用")
        else:
            print("[PATH] エラー: 実行ファイルパスを特定できません！")
            exe_path = Path(os.getcwd()) / "dummy.exe"
            print(f"[PATH] 緊急フォールバック: カレントディレクトリを使用")

        base_dir = exe_path.parent
        data_dir = base_dir / "data"

        print(f"[PATH] 最終結果:")
        print(f"[PATH]   - exe_path: {exe_path}")
        print(f"[PATH]   - base_dir: {base_dir}")
        print(f"[PATH]   - data_dir: {data_dir}")
        print(f"[PATH]   - data_dirは存在する？: {data_dir.exists()}")

    else:
        # 通常のPython環境
        print("[PATH] 通常のPython環境を検出しました")
        print(f"[PATH] __file__: {__file__}")

        base_dir = Path(__file__).resolve().parent
        data_dir = base_dir.parent / "data"

        print(f"[PATH] base_dir: {base_dir}")
        print(f"[PATH] data_dir: {data_dir}")
        print(f"[PATH] data_dirは存在する？: {data_dir.exists()}")

    # 環境変数の設定
    os.environ["BASE_DIR"] = str(base_dir)
    os.environ["DATA_DIR"] = str(data_dir)
    print(f"[PATH] 環境変数を設定しました: BASE_DIR={os.environ['BASE_DIR']}, DATA_DIR={os.environ['DATA_DIR']}")
    print("[PATH] ----- パス検出終了 -----\n")

    return base_dir, data_dir


setup_module_path()

if __name__ == "__main__":
    initialize_base_directory()

    main_manager = MainManager(os.environ["DATA_DIR"])
    main_manager.initialize()
