# 開発者向け README

このドキュメントは、PlanetSide 2 日本語化ツールの開発者向け情報を提供します。

## 概要
このツールは、クリーンアーキテクチャとイベント駆動アーキテクチャを採用し、保守性と拡張性を高めています。

## 技術スタック

- **言語:** Python 3.12.8
- **GUI:** PySide6
- **HTTP:** requests
- **ロギング:** logging
- **エラーハンドリング:** ErrorHandler (カスタムモジュール)

## 依存ライブラリ

```
pip install -r requirements.txt
```
で`requirements.txt`に記載されているライブラリをインストールしてください。

## ファイル構成
```
- gui/
  - main.py: GUIアプリケーションのエントリーポイント
  - MainWindow.ui: Qt Designerで作成したUIファイル
  - data/: アプリケーションで使用するデータファイル
    - ja_jp_data.dat
    - ja_jp_data.dir
    - MyFont.ttf
    - ver.txt
  - src/:
    - ConfigManager.py: 設定ファイルの読み書きを管理
    - ErrorHandler.py: エラーハンドリングを集約
    - FileOperations.py: ファイル操作を管理
    - GameLauncher.py: ゲームの起動を管理
    - GuiConst.py: GUIアプリケーションで使用する定数を定義
    - GUI.py: GUI関連の処理を記述
    - IMainManagerAdapter.py: MainManagerとGUIの間のインターフェース
    - ILogic.py: Logicモジュールのインターフェース
    - MainManager.py: メインの処理を記述
    - MockNetworkManager.py: NetworkManagerのモック
    - NetworkManager.py: ネットワーク関連の処理を管理
    - Logic/: ビジネスロジックを記述
      - check_gui_server_status_logic.py
      - check_translation_server_status_logic.py
      - check_update_gui_logic.py
      - check_update_translation_logic.py
      - copy_dat_file_logic.py
      - copy_dir_file_logic.py
      - copy_font_file_logic.py
      - download_font_logic.py
      - download_gui_logic.py
      - download_translation_logic.py
      - game_launch_logic.py
      - get_app_version_logic.py
      - get_launch_mode_logic.py
      - get_local_path_logic.py
      - get_translation_version_logic.py
      - set_gui_server_url_logic.py
      - set_launch_mode_logic.py
      - set_local_path_logic.py
      - set_translation_server_url_logic.py
- tests/: テストコード
  - test_config_manager.py
  - test_error_handler.py
  - test_file_operations.py
  - test_game_launcher.py
  - test_main_manager.py
  - test_network_manager.py
  - test_data/: テスト用データ
    - data/
      - test_config.json
```

## アーキテクチャ

クリーンアーキテクチャとイベント駆動アーキテクチャを採用しています。詳細は`memory-bank/systemPatterns.md`を参照してください。

## 実行方法

```
python gui/main.py
