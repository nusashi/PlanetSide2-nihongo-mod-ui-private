# Implementation Plan

## 実装手順

1.  **プロジェクトのセットアップ**:
    *   新しいディレクトリを作成する。
    *   必要なファイルを作成する（`main.py`、`src/`ディレクトリ、`src/__init__.py`、`src/MainManager.py`、`src/UIManager.py`、`src/MainWindow.py`、`src/ConfigManager.py`、`src/ILogic.py`、`src/IMainManagerAdapter.py`、`src/Logic/__init__.py`、`src/Logic/set_local_path_logic.py`、`src/Logic/game_launch_logic.py`、`src/Logic/get_launch_mode_logic.py`、`src/Logic/set_launch_mode_logic.py`）。
    *   `requirements.txt`を作成する（最初は`PySide6`と`logging`を記述）。
2.  **`ConfigManager`の実装**:
    *   設定ファイルの読み書き機能を実装する。
3.  **`MainWindow`のUI構築**:
    *   必要最小限のUI要素（ラベル、ボタン、コンボボックスなど）を配置する。
4.  **`UIManager`の実装**:
    *   `MainWindow`と`MainManager`の接続を実装する。
    *   イベントハンドラを実装する。
5.  **`MainManager`の実装**:
    *   `ConfigManager`、`Logic`モジュール、`UIManager`の初期化と連携を実装する。
    *   `Logic`モジュールの呼び出しを実装する。
    *   エラーハンドリングを実装する。
6.  **`Logic`モジュールの実装**:
    *   各ビジネスロジック（ローカルパスの設定、ゲームの起動、起動モードの取得と設定）を実装する。
7.  **テスト**:
    *   各モジュールの動作確認を行う。

## タスクの優先順位

1.  プロジェクトのセットアップ
2.  `ConfigManager`の実装
3.  `MainWindow`のUI構築
4.  `UIManager`の実装
5.  `MainManager`の実装
6.  `Logic`モジュールの実装
7.  テスト

## スケジュール

*   未定 (各タスクの見積もり時間に基づいて後で決定)