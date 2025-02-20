import os
import sys
import pathlib
import tempfile
import inspect


def print_labeled_path(label, path_expression, path_value, description):
    """ラベル、パス取得の式、パスの値、説明文を表示する。パスが存在しない場合はその旨を明記。"""
    if path_value and (isinstance(path_value, str) and os.path.exists(path_value) or isinstance(path_value, pathlib.Path) and path_value.exists()):
        print(f"【{label}】 {path_expression}: {path_value} ({description})")
    else:
        print(f"【{label}】 {path_expression}: 見つかりません/適用外 ({description})")


print("=== Python パス情報 ===")

# --- スクリプト自身のパス ---
print("\n--- スクリプト自身のパス ---")

# 1. __file__
#   - 通常のPython環境: スクリプトファイルの絶対パス
#   - Nuitka (onefile以外): スクリプトファイルの絶対パス
#   - Nuitka (onefile): 一時展開されたディレクトリ内のスクリプトのパス
print_labeled_path("スクリプトのパス", "__file__", __file__, "実行中のスクリプトファイルの場所")

# 2. pathlib.Path(__file__).resolve()
path_expression = "pathlib.Path(__file__).resolve()"
description = "スクリプトファイルの絶対パス (シンボリックリンクを解決)"
print_labeled_path("絶対パス (__file__)", path_expression, pathlib.Path(__file__).resolve(), description)

# 3. inspect.getfile(inspect.currentframe())
path_expression = "inspect.getfile(inspect.currentframe())"
description = "現在のコードが書かれているファイルのパス"
print_labeled_path("inspectでのパス", path_expression, inspect.getfile(inspect.currentframe()), description)

# 4. os.path.dirname(os.path.abspath(__file__))
path_expression = "os.path.dirname(os.path.abspath(__file__))"
description = "__file__ の絶対パスの親ディレクトリ"
print_labeled_path("__file__の親ディレクトリ", path_expression, os.path.dirname(os.path.abspath(__file__)), description)

# --- 実行関連のパス ---
print("\n--- 実行関連のパス ---")

# 5. sys.argv[0]
#   - 通常のPython環境: 実行コマンドに依存 (相対パスの場合もある)
#   - Nuitka (onefile以外): 実行ファイルの絶対パス (バージョン2.4以降)
#   - Nuitka (onefile): 実行ファイルの絶対パス (バージョン2.4以降) or 実行ファイル名
print_labeled_path("実行コマンドの最初の引数", "sys.argv[0]", sys.argv[0], "Python実行時に指定したスクリプトや実行ファイルのパス")

# 6. sys.executable
#   - 通常のPython環境: Pythonインタプリタの絶対パス
#   - Nuitka (onefile以外): コンパイルされた実行ファイルの絶対パス
#   - Nuitka (onefile): Pythonインタプリタの絶対パス (通常は一時ディレクトリ内)
print_labeled_path("Pythonインタプリタ/実行ファイルのパス", "sys.executable", sys.executable, "Pythonインタプリタまたはコンパイルされた実行ファイルの場所")

# 7. os.getcwd()
print_labeled_path("カレントディレクトリ", "os.getcwd()", os.getcwd(), "現在の作業ディレクトリ")

# --- モジュール関連のパス ---
print("\n--- モジュール関連のパス ---")
# 8. sys.path
print(f"【モジュール検索パス】 sys.path: {sys.path} (Pythonがモジュールを探す場所のリスト)")

# 9. sys.modules['__main__'].__file__
if hasattr(sys.modules["__main__"], "__file__"):
    description = "最初に実行されたスクリプトファイルのパス"
    print_labeled_path("メインモジュールのパス", "sys.modules['__main__'].__file__", sys.modules["__main__"].__file__, description)
else:
    description = "最初に実行されたスクリプトファイルのパス (存在しない/適用できない場合)"
    print_labeled_path("メインモジュールのパス", "sys.modules['__main__'].__file__", "Not found/Not applicable", description)

# --- 一時ディレクトリ ---
print("\n--- 一時ディレクトリ ---")

# 10. tempfile.gettempdir()
print_labeled_path("一時ディレクトリ", "tempfile.gettempdir()", tempfile.gettempdir(), "システムの一時ディレクトリ")

# --- Nuitka 関連 (Nuitka環境でのみ表示) ---
if getattr(sys, "frozen", False):
    print("\n--- Nuitka 関連のパス (Nuitkaでコンパイルされた場合のみ) ---")

    # 11. sys._MEIPASS (onefileモードでのみ)
    #     Nuitka onefileモードで実行ファイルを一時展開したディレクトリ。
    if hasattr(sys, "_MEIPASS"):
        description = "Nuitka onefileモードで一時展開されたディレクトリ"
        print_labeled_path("一時展開ディレクトリ (onefile)", "sys._MEIPASS", sys._MEIPASS, description)

    # 12. __compiled__.containing_dir
    #    Nuitkaでコンパイルされた実行ファイル/モジュールが含まれるディレクトリ。
    try:
        import __compiled__

        description = "Nuitkaでコンパイルされたファイルが含まれるディレクトリ"
        print_labeled_path("コンパイル済みファイルディレクトリ", "__compiled__.containing_dir", __compiled__.containing_dir, description)

    except ImportError:
        description = "Nuitkaでコンパイルされたファイルが含まれるディレクトリ (見つかりません/適用外)"
        print_labeled_path("コンパイル済みファイルディレクトリ", "__compiled__.containing_dir", "Not found/Not applicable", description)

print("=== Python パス情報 終了 ===")
input("何かキーを押して終了...")