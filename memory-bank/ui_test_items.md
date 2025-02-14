# UIテスト項目

## MainWindow

### 起動モード

*   **テスト対象:** `radio_normal`, `radio_steam`, `combobox_launch_mode`
*   **テスト内容:**
    1.  ラジオボタンの初期状態を確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  ラジオボタンを切り替えたときに、`combobox_launch_mode`の選択肢が適切に変化するか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    3.  `combobox_launch_mode`で選択した起動モードが、`config.json`の`launch_mode`に正しく保存されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    4.  アプリケーション起動時に、`config.json`の`launch_mode`の値が`combobox_launch_mode`とラジオボタンに正しく反映されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  アプリケーション起動時に、`config.json`に保存されている`launch_mode`に対応するラジオボタンが選択されている。
    2.  ラジオボタンを切り替えると、`combobox_launch_mode`の選択肢も連動して変化する。
    3.  `combobox_launch_mode`で選択した値が、`config.json`の`launch_mode`に保存される。
    4.  次回起動時に、保存された`launch_mode`の値がUIに反映される。
*   **関連ファイルとメソッド:**
    *   `gui/src/MainWindow.py`: `init_ui`, `setup_layout`, `launch_mode_changed`, `set_launch_mode_on_startup`
    *   `gui/src/UIManager.py`: `set_launch_mode`, `update_ui`
    *   `gui/src/MainManager.py`: `set_launch_mode`
    *   `gui/src/Logic/set_launch_mode_logic.py`: `execute`
    *   `gui/src/Logic/get_launch_mode_logic.py`: `execute`
    *   `gui/src/ConfigManager.py`: `get_config`, `set_config`, `save_config`

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
    *   `gui/src/MainWindow.py`: `launch_game`
    *   `gui/src/UIManager.py`: `launch_game`
    *   `gui/src/MainManager.py`: `launch_game`
    *   `gui/src/Logic/game_launch_logic.py`: `execute`

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
    *   `gui/src/MainWindow.py`: `copy_translation_files`
    *   `gui/src/UIManager.py`: `copy_translation_files`
    *   `gui/src/MainManager.py`: `copy_translation_files`
    *   `gui/src/Logic/copy_dat_file_logic.py`: `execute`
    *   `gui/src/Logic/copy_dir_file_logic.py`: `execute`
    *   `gui/src/Logic/copy_font_file_logic.py`: `execute`

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
    *   `gui/src/MainWindow.py`: `check_updates`, `init_ui`
    *   `gui/src/UIManager.py`: `check_updates`, `update_data`
    *   `gui/src/MainManager.py`: `check_for_updates`, `check_update_gui`, `check_update_translation`, `update_gui`, `update_translation`, `get_app_version`, `get_translation_version`
    *   `gui/src/Logic/check_update_gui_logic.py`: `execute`
    *   `gui/src/Logic/check_update_translation_logic.py`: `execute`
    *   `gui/src/Logic/download_gui_logic.py`: `execute`
    *   `gui/src/Logic/download_translation_logic.py`: `execute`
    *   `gui/src/Logic/get_app_version_logic.py`: `execute`
    *   `gui/src/Logic/get_translation_version_logic.py`: `execute`

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
    *   `gui/src/MainWindow.py`: `init_ui`, `setup_layout`
    *   `gui/src/ErrorHandler.py`: `handle_error`, `log_message`

### 設定

*   **テスト対象:** `button_settings`
*   **テスト内容:**
    1.  「設定」ボタンを押したときに、設定ポップアップが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  設定ポップアップが表示される。
*   **関連ファイルとメソッド:**
    *   `gui/src/MainWindow.py`: `open_settings_popup`
    *   `gui/src/UIManager.py`: `open_settings_popup`
    *   `gui/src/settings_popup.py`

### ヘルプ

*   **テスト対象:** `button_help`
*   **テスト内容:**
    1.  「ヘルプ」ボタンを押したときに、ヘルプポップアップが表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  ヘルプポップアップが表示される。
*   **関連ファイルとメソッド:**
    *   `gui/src/MainWindow.py`: `open_help`
    *   `gui/src/help_popup.py`

### ローカルパス

*   **テスト対象:** `label_local_path`
*   **テスト内容:**
    1.  アプリケーション起動時に、`config.json`に保存されているローカルパスがラベルに表示されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
    2.  設定ポップアップでローカルパスを変更したときに、ラベルの表示が更新されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  `config.json`に保存されているローカルパスがラベルに表示される。
    2.  設定ポップアップでローカルパスを変更すると、ラベルの表示も更新される。
*   **関連ファイルとメソッド:**
    *   `gui/src/MainWindow.py`: `init_ui`, `setup_layout`, `update_local_path`
    *   `gui/src/UIManager.py`: `update_ui`, `set_local_path`
    *   `gui/src/MainManager.py`: `set_local_path`, `get_config`
    *   `gui/src/Logic/get_local_path_logic.py`: `execute`
    *   `gui/src/Logic/set_local_path_logic.py`: `execute`
    *   `gui/src/ConfigManager.py`: `get_config`, `set_config`, `save_config`

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
    *   `gui/src/settings_popup.py`: `init_ui`, `setup_layout`, `open_file_dialog`, `setup_connections`
    *   `gui/src/UIManager.py`: `set_local_path`, `update_settings_popup`
    *   `gui/src/MainManager.py`: `set_local_path`, `get_config`
    *   `gui/src/Logic/set_local_path_logic.py`: `execute`
    *   `gui/src/ConfigManager.py`: `set_config`, `save_config`

### サーバーURL設定

*   **テスト対象:** `label_app_server_url`, `lineedit_app_server_url`, `label_translation_server_url`, `lineedit_translation_server_url`
*   **テスト内容:**
    1.  `lineedit_app_server_url`と`lineedit_translation_server_url`にURLを入力し、Enterキーを押したときに、`config.json`の`app_server_url`と`translation_server_url`の値が更新されるか確認する。
        *   **テスト内容詳細:** (ここに具体的なテスト内容を追記)
        *   **テスト結果:** (ここにテスト結果を追記)
*   **期待される結果:**
    1.  入力したURLが`config.json`に保存される。
*   **関連ファイルとメソッド:**
    *   `gui/src/settings_popup.py`: `init_ui`, `setup_layout`
    *   `gui/src/UIManager.py`: `set_app_server_url`, `set_translation_server_url`, `update_settings_popup`
    *   `gui/src/MainManager.py`: `set_app_server_url`, `set_translation_server_url`, `get_config`
    *   `gui/src/Logic/set_gui_server_url_logic.py`: `execute`
    *   `gui/src/Logic/set_translation_server_url_logic.py`: `execute`
    *   `gui/src/ConfigManager.py`: `set_config`, `save_config`

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
    *   `gui/src/help_popup.py`: `__init__`