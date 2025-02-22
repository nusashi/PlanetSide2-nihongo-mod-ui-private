# Progress

## 動作するもの

*   設定ファイル (JSON形式) の読み書き (`ConfigManager`): 確認済み
*   基本的なGUI (`MainWindow`, `SettingsPopup`, `HelpPopup`, `TutorialPopup`): 確認済み
*   `MainManager` と `UIManager` の連携 (カスタムシグナルによるイベント駆動): 確認済み
*   GitHub リポジトリへの疎通確認 (`GitHubResourceManager`): 確認済み
*   最新リリースのタグ名取得 (`GitHubResourceManager`): 確認済み
*   設定ポップアップのローカルパス入力欄に、起動時にconfigのデータが出力される: 確認済み
*   `settings_popup.py`の`textEdited`シグナルを使って、ローカルパスなどの変更が`MainManager`に通知される: 確認済み
*   `main_window.py`の`HelpPopup`と`SettingsPopup`関連の処理が削除され、`UIManager`経由で呼び出される: 確認済み
*   誤って削除した`main_window.py`のコールバック設定が復元された: 確認済み
*   `main_window.py`の`set_icons`メソッドで`icon.ico`を読み込む: 確認済み
*   Nuitkaによるコンパイル手順の確立: 確認済み
*   初回起動時のチュートリアルポップアップ (`TutorialPopup`): 確認済み
*   ゲーム起動 (通常版/Steam版): 実装済み (`MainManager.try_game_launch`)
*   ファイル置換 (日本語化): 実装済み (`MainManager.try_translation`)
*   アップデート機能 (アプリと翻訳データ)
    *   GitHub Releases からのダウンロード: 実装済み (`GitHubResourceManager.download_latest_assets`, `MainManager.download_app_files`, `MainManager.download_translation_files`)
*   Nuitka でのコンパイルと証明書署名: 確認済み (`build.bat` で自動化)
*   `updater.bat`の作成: 完了

## 構築するもの

*   なし

## 要件

*   サーバーダウン時: 適切なエラーメッセージを表示: 実装済み (`MainManager.check_update`でエラーメッセージを設定)
*   設定ファイル破損時: デフォルト設定で起動: 実装済み (`ConfigManager`でデフォルト設定を使用)
*   ファイル操作権限不足時: エラーメッセージを表示し、処理を中断しない: 未実装 (TODO: ファイル操作時に例外処理を追加)
*   ファイル不在時: 適切なエラーメッセージを表示: 実装済み (各メソッド内でファイル/フォルダの存在チェックとエラー処理を実施)

## 現在のステータス

*   Memory Bank の更新: 実施中
*   全コードの読み込み: 完了

## 既知の問題

*   特になし

## 今後の計画

*   なし
