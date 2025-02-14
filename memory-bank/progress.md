## 動作するもの

*   ゲーム起動 (通常版/Steam版)
*   ファイル置換 (日本語化)
*   ローカルパス設定
*   起動モード設定
*   設定ファイル (JSON形式)
*   エラー処理 (ログ出力、ユーザー通知、GUI表示)
*   GitHub Releasesからのアップデート確認 (アプリバージョン): モック実装完了
*   GUIからの設定編集機能 (翻訳バージョン、アプリケーションバージョンは表示のみで編集不可)
*   各種テスト: 完了
    *   ファイル操作
    *   `NetworkManager`のモック
    *   `MainManager`と各`Logic`モジュールの結合
    *   コマンドライン引数によるビジネスロジック
*   ローカルパス設定 (設定ポップアップから変更可能に)
*   URL変更 (設定ポップアップから変更可能に)
* UIとビジネスロジックの接続（`MainManager`、`UIManager`、`MainWindow`、`Logic`モジュールの連携）
* 起動確認: 完了

## 構築するもの

*   翻訳ファイルとフォントファイルのダウンロード (GitHub Releases から): 実装とテスト
*   アプリの自動アップデート機能

## 要件

*   サーバーダウン時: 適切なエラーメッセージを表示
*   設定ファイル破損時: デフォルト設定で起動
*   ファイル操作権限不足時: エラーメッセージを表示し、処理を中断しない
*   ファイル不在時: 適切なエラーメッセージを表示

## 現在のステータス

*   Memory Bank の更新: 完了
*   クリーンアーキテクチャに基づいたリファクタリング: 完了
*   プロジェクト構成の変更: 完了
*   設定ファイル形式を JSON に変更: 完了
*   エラー処理の改善と集約、ログ機能を実装: 完了
*   ファイルパスを環境変数から取得: 完了
*   GUIとの依存関係を排除: 完了
*   ダークモード対応: オミット
*   README、仕様書、readme_dev.txt の更新: 完了
*   GUI再構築: `preview_gui.py`の修正 (UI調整): 完了
*   GUI再構築: `preview_gui.py`の修正 (イベントハンドラ実装): 完了
*   GUI再構築: `MainWindow.py`への移植: 完了 (イベントハンドラ実装、UIManagerとの接続を含む)
*   `config.json`のキー変更(`server_url`を`app_server_url`と`translation_server_url`に分割): 完了
*   `MainManager`の`update_gui`と`update_translation`メソッド追加: 完了
*   `UIManager`の`set_app_server_url`、`set_translation_server_url`、`set_local_path`メソッド追加: 完了
*   `SettingsPopup`と`UIManager`の接続: 完了
*   `MainWindow`にローカルパス表示機能追加: 完了
*   `MainManager`と`UIManager`のリファクタリング: 完了
*   起動確認とエラー修正: 完了
*   各Logicモジュールへのログ出力追加: 完了
*   `MainManager.py`へのログ出力追加: 未完了
*   `MainManager.py`の構文エラー修正: 完了
*   `ConfigManager.py`、`NetworkManager.py`、`IMainManagerAdapter.py`、`UIManager.py`、`MainWindow.py`、`check_update_gui_logic.py`、`check_update_translation_logic.py`のインポート文修正: 完了
*   `gui/src/Logic/__init__.py`の作成と修正: 完了
*   インポートエラーの修正: 完了
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
*   `MainWindow.py`の`setup_layout`メソッドで`combobox_launch_mode`をレイアウトに追加: 完了
*   `MainWindow`クラスに`update_local_path`メソッドを定義: 完了
*   `MainManager.py`へのログ出力追加: 完了
*   `UIManager.py`へのログ出力追加: 完了
*   Memory Bankの更新: 完了 (今回`activeContext.md`を更新)

## 既知の問題

*   アップデート: アプリの自動アップデート未実装

## 今後の計画

1.  **アップデート:** GitHub Releasesからのアップデート確認機能とアプリの自動アップデート機能を実装
2.  **サーバーの可用性:** GitHub Releasesへの完全移行 (現行サーバーの停止)

## UIに関する要件
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
