# 定数宣言
WINDOW_TITLE = "PS2JPMod"
EN_DAT_FINE_NAME = "en_us_data.dat"
EN_DIR_FILE_NAME = "en_us_data.dir"
JP_DAT_FINE_NAME = "ja_jp_data.dat"
JP_DIR_FILE_NAME = "ja_jp_data.dir"
FONT_FILE_NAME = "MyFont.ttf"

# config_key
APP_VERSION = "app_version"
TRANSLATION_VERSION = "translation_version"
LAUNCH_MODE = "launch_mode"
LOCAL_PATH = "local_path"
APP_UPDATE_SERVER_URL = "app_server_url"
TRANSLATION_UPDATE_SERVER_URL = "translation_server_url"

# LaunchMode
NORMAL_LAUNCH = 0
STEAM_LAUNCH = 1

# config_default
# TODO DEFAULT_APP_VERSION は 更新の際にバージョンを上げる
DEFAULT_APP_VERSION = "0.0.1"
DEFAULT_TRANSLATION_VERSION = "0.0.1"
DEFAULT_LAUNCH_MODE = STEAM_LAUNCH
DEFAULT_LOCAL_PATH = ""
DEFAULT_APP_UPDATE_SERVER_URL = "https://github.com/nusashi/PlanetSide2-nihongo-mod-ui/releases/latest"
DEFAULT_TRANSLATION_UPDATE_SERVER_URL = "https://github.com/nusashi/PlanetSide2-nihongo-mod-api/releases/latest"


# ラジオボタンレイアウト
LAUNCH_BUTTON_TEXT = "1:ゲーム起動"
TRANSLATION_BUTTON_TEXT = "2:日本語化"
STEAM_GAME_URI = "steam://rungameid/218230"

# バージョンレイアウト
UPDATE_BUTTON_TEXT = "更新"
UPDATE_CONFIRM_BUTTON_TEXT = "アップデート確認"

import os
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]  # 最初の引数を output フォルダのパスとする
    else:
        output_dir = "./output"  # 引数がない場合のデフォルト値

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "version.txt"), "w") as f:
        f.write(DEFAULT_APP_VERSION)
