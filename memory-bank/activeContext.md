# Active Context

## 最近の変更

*   プロジェクトのディレクトリ構造を大幅に変更 (`project_root` を導入)
*   `Logic` モジュールを廃止し、`MainManager` にビジネスロジックを集約
*   `MainManager` と `UIManager` の間の通信にカスタムシグナルを使用するように変更
*   `preview_gui.py` を削除し、`MainWindow.py` に直接UIを実装
*   Memory Bank の更新 (今回)

## 次のステップ

*   Memory Bank の更新 (今回)
    *   `progress.md`, `ui_test_items.md`, `.clinerules` の更新
*   UIの調整 (必要に応じて)
*   各種機能の実装とテスト (ゲーム起動、日本語化、アップデート確認、設定変更など)
*   UIテスト
*   アップデート機能の実装 (アプリと翻訳データ)
