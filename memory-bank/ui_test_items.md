# UIテスト項目

## MainWindow

### 起動モード

*   **テスト対象:** `radio_normal`, `radio_steam`
*   **テスト内容:**
    1.  ラジオボタンの初期状態を確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  アプリケーション起動時に、`config.json`に保存されている`launch_mode`に対応するラジオボタンが選択されている。
    2.  次回起動時に、保存された`launch_mode`の値がUIに反映される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `init_ui`, `setup_layout`, `_on_radio_normal_clicked`, `_on_radio_steam_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_radio_normal_clicked`, `on_radio_steam_clicked`, `update_launch_mode_ui`
    *   `project_root/src/system/main_manager.py`: `launch_mode` (プロパティ)
    *   `project_root/src/system/config_manager.py`: `get_config`, `set_config`, `save_config`

### ゲーム起動

*   **テスト対象:** `button_game_launch`
*   **テスト内容:**
    1.  ローカルパスが設定されていない状態で「ゲーム起動」ボタンを押したときに、エラーメッセージが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  ローカルパスが設定されている状態で「ゲーム起動」ボタンを押したときに、選択されている起動モードでゲームが起動するか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    3.  通常起動が選択されている場合
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    4.  Steam起動が選択されている場合
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  エラーメッセージが表示され、ゲームは起動しない。
    2.  選択された起動モードでゲームが起動する。
    3.  `LaunchPad.exe`が通常モードで起動する。
    4.  `LaunchPad.exe`がSteam経由で起動する。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `_on_button_game_launch_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_game_launch_clicked`
    *   `project_root/src/system/main_manager.py`: `try_game_launch`

### ファイル置換

*   **テスト対象:** `button_replace_translation`
*   **テスト内容:**
    1.  ローカルパスが設定されていない状態で「日本語化」ボタンを押したときに、エラーメッセージが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  ローカルパスが設定されている状態で「日本語化」ボタンを押したときに、日本語化ファイルがゲームフォルダにコピーされるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  エラーメッセージが表示され、ファイルはコピーされない。
    2.  `ja_jp_data.dat`、`ja_jp_data.dir`、`MyFont.ttf`がゲームフォルダにコピーされる。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `_on_button_replace_translation_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_replace_translation_clicked`
    *   `project_root/src/system/main_manager.py`: `try_translation`

### バージョン情報/アップデート

*   **テスト対象:** `label_app_version`, `label_translation_version`, `button_update_app`, `button_update_translation`, `button_check_update`
*   **テスト内容:**
    1.  「アップデート確認」ボタンを押したときに、アプリケーションと翻訳ファイルのバージョン情報が取得され、ラベルに表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  アプリケーションのバージョンが古い場合、「更新」ボタンが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    3.  翻訳ファイルのバージョンが古い場合、「更新」ボタンが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    4.  「更新」ボタンを押したときに、アップデート処理が実行されるか確認する。 (TODO: アップデート処理の実装後)
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  ラベルに現在のバージョン情報が表示される。
    2.  アプリケーションのバージョンが古い場合、「更新」ボタンが表示される。
    3.  翻訳ファイルのバージョンが古い場合、「更新」ボタンが表示される。
    4.  アップデート処理が実行される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `init_ui`, `update_app_version_label`, `update_translation_version_label`, `_on_button_update_app_clicked`, `_on_button_update_translation_clicked`, `_on_button_check_update_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_update_app_clicked`, `on_update_translation_clicked`, `on_check_update_clicked`, `show_update_app_button_changed`, `show_update_translation_button_changed`
    *   `project_root/src/system/main_manager.py`: `check_update`, `download_app_file`, `download_translation_file`, `app_version`, `translation_version`, `next_app_version`, `next_translation_version`
    *   `project_root/src/system/github_resource_manager.py`: `check_connection`, `get_latest_tag`, `download_asset`

### ステータス

*   **テスト対象:** `textedit_status`
*   **テスト内容:**
    1.  各種処理の実行中に、ステータスが適切に表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  エラーが発生した場合に、エラーメッセージが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  処理の進捗状況や結果がステータス表示に表示される。
    2.  エラーが発生した場合、エラーメッセージが表示される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `init_ui`, `setup_layout`, `update_status_text`
    *   `project_root/src/ui/ui_manager.py`: `status_text_changed`
    *   `project_root/src/system/main_manager.py`: `status_string`

### 設定

*   **テスト対象:** `button_settings`
*   **テスト内容:**
    1.  「設定」ボタンを押したときに、設定ポップアップが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  設定ポップアップが表示される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `_on_button_settings_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_settings_clicked`
    *   `project_root/src/ui/settings_popup.py`

### ヘルプ

*   **テスト対象:** `button_help`
*   **テスト内容:**
    1.  「ヘルプ」ボタンを押したときに、ヘルプポップアップが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  ヘルプポップアップが表示される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/main_window.py`: `_on_button_help_clicked`
    *   `project_root/src/ui/ui_manager.py`: `on_help_clicked`
    *   `project_root/src/ui/help_popup.py`

## SettingsPopup

### ローカルパス設定

*   **テスト対象:** `label_local_path`, `lineedit_local_path`, `button_local_path`
*   **テスト内容:**
    1.  「参照...」ボタンを押したときに、フォルダ選択ダイアログが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  フォルダ選択ダイアログでフォルダを選択したときに、`lineedit_local_path`にフォルダパスが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    3.  `lineedit_local_path`の内容が変更されたときに、`config.json`の`local_path`の値が更新されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  フォルダ選択ダイアログが表示される。
    2.  選択したフォルダのパスが`lineedit_local_path`に表示される。
    3.  `lineedit_local_path`の内容が`config.json`の`local_path`に保存される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/settings_popup.py`: `init_ui`, `setup_layout`, `_on_button_local_path_clicked`, `update_lineedit_local_path_text`
    *   `project_root/src/ui/ui_manager.py`: `on_local_path_browse_clicked`, `local_path_changed`
    *   `project_root/src/system/main_manager.py`: `local_path`
    *   `project_root/src/system/config_manager.py`: `set_config`, `save_config`

### サーバーURL設定

*   **テスト対象:** `label_app_server_url`, `lineedit_app_server_url`, `label_translation_server_url`, `lineedit_translation_server_url`
*   **テスト内容:**
    1.  `lineedit_app_server_url`と`lineedit_translation_server_url`にURLを入力し、Enterキーを押したときに、`config.json`の`app_server_url`と`translation_server_url`の値が更新されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  入力したURLが`config.json`に保存される。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/settings_popup.py`: `init_ui`, `setup_layout`, `update_lineedit_app_server_url_text`, `update_lineedit_translation_server_url_text`
    *   `project_root/src/ui/ui_manager.py`: `app_update_server_url_changed`, `translation_update_server_url_changed`
    *   `project_root/src/system/main_manager.py`: `app_update_server_url`, `translation_update_server_url`
    *   `project_root/src/system/config_manager.py`: `set_config`, `save_config`

## HelpPopup

### ヘルプテキスト表示

*   **テスト対象:** `label_help`
*   **テスト内容:**
    1.  ヘルプテキストが正しく表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  テキストが折り返されて表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    3.  テキストが左上に配置されているか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  定義されたヘルプテキストが表示される。
    2.  テキストが折り返されて表示される。
    3.  テキストが左上に配置されている。
*   **関連ファイルとメソッド:**
    *   `project_root/src/ui/help_popup.py`: `__init__`