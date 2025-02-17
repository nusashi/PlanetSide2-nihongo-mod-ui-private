# Active Context

## 最近の変更

*   プロジェクトのディレクトリ構造を大幅に変更 (`project_root` を導入)
*   `Logic` モジュールを廃止し、`MainManager` にビジネスロジックを集約
*   `MainManager` と `UIManager` の間の通信にカスタムシグナルを使用するように変更
*   `preview_gui.py` を削除し、`MainWindow.py` に直接UIを実装
*   Memory Bank の更新
*   メインウィンドウからローカルパスのラベルを削除
*   設定ポップアップのローカルパス入力欄に、起動時にconfigのデータが出力されない問題を修正
*   `settings_popup.py`の`textEdited`シグナルを使って、ローカルパスなどの変更を`MainManager`に通知するように修正
*   `main_window.py`の`HelpPopup`と`SettingsPopup`関連の処理を削除し、`UIManager`経由で呼び出すように修正
*   誤って削除した`main_window.py`のコールバック設定を復元
*   全コードの読み込み完了

## 次のステップ

*   `systemPatterns.md` の更新 (Mermaid 記法の図を追加)
*   `progress.md` の更新 (コード読み込みの結果を反映)
*   他のメモリーバンクのファイルも必要に応じて更新
*   UIの調整 (必要に応じて)
*   各種機能の実装とテスト (ゲーム起動、日本語化、アップデート確認、設定変更など)
*   UIテスト
*   アップデート機能の実装 (アプリと翻訳データ)
