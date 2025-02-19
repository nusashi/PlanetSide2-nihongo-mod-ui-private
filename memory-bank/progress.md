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

## 構築するもの

*   アップデート機能 (アプリと翻訳データ)
    *   ダウンロードしたファイルの適用: 未実装 (TODO: `download_app_files`でダウンロードしたファイルを適用する処理が必要)
*   各種機能のテスト: 未実施 (TODO)
*   必要なファイルやフォルダが無い場合の対応:
    *   ja_jp_data.datが無い場合：疎通確認後に初回ダウンロード (TODO: `MainManager.try_translation`で、ファイルが存在しない場合にダウンロードする処理が必要)
    *   ja_jp_data.dirが無い場合：疎通確認後に初回ダウンロード (TODO: `MainManager.try_translation`で、ファイルが存在しない場合にダウンロードする処理が必要)
    *   MyFont.ttfが無い場合：疎通確認後に初回ダウンロード (TODO: `MainManager.try_translation`で、ファイルが存在しない場合にダウンロードする処理が必要)
    *   updater.exeが無い場合：疎通確認後に初回ダウンロード (TODO: まだ`update.exe`は作成すらしてないので)

## 要件

*   サーバーダウン時: 適切なエラーメッセージを表示: 実装済み (`MainManager.check_update`でエラーメッセージを設定)
*   設定ファイル破損時: デフォルト設定で起動: 実装済み (`ConfigManager`でデフォルト設定を使用)
*   ファイル操作権限不足時: エラーメッセージを表示し、処理を中断しない: 未実装 (TODO: ファイル操作時に例外処理を追加)
*   ファイル不在時: 適切なエラーメッセージを表示: 実装済み (各メソッド内でファイル/フォルダの存在チェックとエラー処理を実施)

## 現在のステータス

*   Memory Bank の更新: 実施中
*   全コードの読み込み: 完了

## 既知の問題

*   特になし (これから実装していく中で問題が見つかる可能性あり)

## 今後の計画

1.  UIの調整 (必要に応じて)
2.  各種機能の実装とテスト (ゲーム起動、日本語化、アップデート確認、設定変更など)
3.  UIテスト
4.  アップデート機能の実装 (アプリと翻訳データ)
5.  ダウンロードしたファイルの適用
6.  ファイル操作権限不足時の例外処理
7.  翻訳ファイルやフォントファイルが無い場合の初回ダウンロード処理
