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
*   `main_manager.py`の`_check_version_update`の戻り値の型を修正
*   `ui_manager.py`の`redraw`メソッド内の変数順を修正
*   メインウィンドウのレイアウト調整
    *   ステータス表示エリア拡大
    *   バージョン情報表示エリア縮小

## 次のステップ

*   UIの調整 (必要に応じて)
*   各種機能の実装とテスト (ゲーム起動、日本語化、アップデート確認、設定変更など)
*   UIテスト
*   アップデート機能の実装 (アプリと翻訳データ)
