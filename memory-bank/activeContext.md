# Active Context

## 最近の変更

*   Qt Designerの使用が禁止されたため、`gui/MainWindow.ui`を直接編集する方針から、`gui/src/MainWindow.py`を直接編集してGUIを構築する方針に変更。
*   `gui/MainWindow.ui`が破損したため、削除。
*   Memory Bankの更新 (前回)
*   GUI確認用の`gui/src/preview_gui.py`を作成
*   設定ポップアップ(`gui/src/settings_popup.py`)を作成
*   ヘルプポップアップ(`gui/src/help_popup.py`)を作成
*   アイコンをQtの標準アイコンに変更
*   `preview_gui.py`から`MainWindow.py`への移植準備
*   UIとビジネスロジックのつなぎこみ計画策定
*   `main.py`から`QApplication`と`MainWindow`のインスタンス化処理を削除
*   `MainManager`から`PySide6`への依存を削除
*   `UIManager`クラスの作成
*   `MainWindow.py`のイベントハンドラ実装と`UIManager`との接続
*   `ErrorHandler`クラスに`log_message`メソッドを追加
*   `MainManager`クラスに`get_error_handler`メソッドを追加
*   `IMainManagerAdapter`インターフェースに`get_error_handler`メソッドを追加
*   `UIManager`クラスに`get_main_window`メソッドを追加
*   各Logicモジュール、`MainManager`、`UIManager`にログ出力を追加
*   `LogicResult`クラスの`success`属性と`error`属性を直接参照するように修正
*   `ConfigManager`で、`config.json`のパスをexe化後も有効なパスに修正
*   不要な`config.json`ファイルを削除
*   `MainManager`のコンストラクタで依存性注入を行うように修正
*   重複したインポート文の削除
*   `UIManager`に`set_app_server_url`と`set_translation_server_url`メソッドを追加
*   `SettingsPopup`の`lineedit_app_server_url`と`lineedit_translation_server_url`の編集完了イベントを`UIManager`の対応するメソッドに接続
*   `UIManager`に`set_local_path`メソッドを追加
*   `SettingsPopup`の`button_local_path`のクリックイベントを`UIManager`の`set_local_path`メソッドに接続
*   `UIManager`に`update_settings_popup`メソッドを追加し、`config.json`からローカルパスを取得して`SettingsPopup`に表示
*   `MainWindow`に`update_local_path`メソッドを追加し、ローカルパス表示用のラベルを追加
*   `UIManager`の`update_ui`メソッドから`MainWindow`と`SettingsPopup`の`update_local_path`を呼び出すように変更
*   `MainManager`に`update_gui`と`update_translation`メソッドを追加し、アップデート後に`UIManager`の`update_ui`を呼び出すように変更
*   `MainManager`の不要なコメントとメソッドを削除
*   `UIManager`内の`Logic`モジュール呼び出しを`MainManager`のメソッド呼び出しに変更
*   `MainManager`に`IMainManagerAdapter`の抽象メソッドを実装
*   `MainManager`の`Logic`辞書の定義を修正
*   起動確認とエラー修正
    *   `NameError: name 'set_local_path_logic' is not defined`
    *   `AttributeError: module 'gui.src.Logic.get_local_path_logic' has no attribute 'SetLocalPathLogic'`
    *   `TypeError: Can't instantiate abstract class MainManager without an implementation for abstract method 'get_base_dir'`
    *   `TypeError: Can't instantiate abstract class MainManager without an implementation for abstract methods 'check_gui_server_status' 'check_translation_server_status'`
    *   `NameError: name 'Union' is not defined`
    *   `QWidget: Must construct a QApplication before a QWidget`
    *   `AttributeError: 'UIManager' object has no attribute 'get_config'`
    *   `AttributeError: 'UIManager' object has no attribute 'check_updates'`
    *   `TypeError: DownloadGuiLogic.execute() missing 2 required positional arguments: 'asset_name' and 'download_path'`
    *   `AttributeError: 'ErrorHandler' object has no attribute 'show_error'`
* UIに関する要件定義 (2025/2/12)
    1.  **フォント:**
        *   GUI本体はデフォルトフォントを使用。
        *   `MyFont.ttf`は、ゲームの日本語化フォント差し替えに使用する元ファイル。
    2.  **アイコン:**
        *   カスタムアイコンは使用しない。Qtの標準アイコンを使用。
    3.  **ダークモード:**
        *   対応しない。
    4.  **アップデート確認ボタン:**
        *   `button_check_update`: 常時表示。GUIサーバーと翻訳サーバーの疎通確認と、バージョン差異の確認を行う。
        *   `button_update_app`: アプリケーションのバージョン差異がある場合に表示。
        *   `button_update_translation`: 翻訳のバージョン差異がある場合に表示。
        *   バージョン差異の確認は、`MainManager`が一時的に保持する次のバージョン情報と、`config.json`に保存されている現在のバージョン情報を比較することで行う。
    5.  **テキストの省略表示:**
        *   対応しない。
* 各Logicモジュールへのログ出力追加: 完了
* `MainManager.py`へのログ出力追加: 未完了
* `MainManager.py`の構文エラー修正: 完了
* `ConfigManager.py`、`NetworkManager.py`、`IMainManagerAdapter.py`、`UIManager.py`、`MainWindow.py`、`check_update_gui_logic.py`、`check_update_translation_logic.py`のインポート文修正: 完了
* `gui/src/Logic/__init__.py`の作成と修正: 完了
* インポートエラーの修正: 完了
*   `main.py`がGUIに依存する問題を修正: 完了
*   `.clinerules`の誤ったルールを修正: 完了
*   循環インポートの問題を修正: 完了
*   `ConfigManager`の`config_file`のパスを修正: 完了
*   `UIManager`に`get_base_dir`メソッドを追加: 完了
*   `UIManager`の`update_ui`メソッドの修正: 完了
*   `MainWindow.py`を`preview_gui.py`のレイアウトに修正: 完了
*   `MainWindow.py`のイベントハンドラを`UIManager`のメソッドに接続: 完了
*   `MainWindow.py`の不要なラベルとメソッドを削除:完了
*   `MainWindow.py`のアイコン設定を修正:完了
* `MainWindow.py`のコメントアウト解除: 完了
* UIが表示されない問題の解決: 完了
* `MainWindow.py`の`setup_layout`メソッドで`combobox_launch_mode`がレイアウトに追加されていない
* `MainWindow`クラスに`update_local_path`メソッドが定義されていない

## 最近の変更

*   `MainWindow.py`の`setup_layout`メソッドで`combobox_launch_mode`をレイアウトに追加
*   `MainWindow`クラスに`update_local_path`メソッドを定義
*   `MainManager.py`へのログ出力追加
*   `UIManager.py`へのログ出力追加
*   Memory Bankの更新 (今回)

## 次のステップ

*   アップデート機能の実装
