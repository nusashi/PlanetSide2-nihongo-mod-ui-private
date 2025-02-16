from src.const import const
from src.system.config_manager import JsonConfigManager


class MainManager:
    def __init__(self):
        print("MainManagerインスタンス作成")
        # インスタンス変数宣言
        self._next_app_version = const.DEFAULT_APP_VERSION
        self._next_translation_version = const.DEFAULT_TRANSLATION_VERSION
        self._status_string = "" # ステータス
        self._config_manager = JsonConfigManager()
        # 初回起動対応
        if self._config_manager.get_initial_config():
            # TODO 初回起動時、チュートリアルポップアップを表示
            pass

        # アップデート確認
        self.check_update()

        # TODO 起動モード読み込み
        # TODO 起動モード設定
        # TODO 通常起動関数
        # TODO Steam起動関数
        # TODO ローカルパス確認関数
        # TODO ローカルパス設定関数
        # TODO AppUpdateServer疎通確認関数
        # TODO TranslationUpdateServer疎通確認関数
        # TODO dat&dir 置き換え関数
        # TODO font 置き換え関数
        # TODO 日本語化関数
        # TODO
        # TODO
        # TODO
        self.initialize()

    def initialize(self):
        print("初期化")

    def check_update(self):
        # TODO アップデート確認関数
        pass

    @property
    def status_string(self):
        return self._status_string

    @status_string.setter
    def status_string(self, new_value):
        self._status_string = new_value

    @property
    def app_version(self):
        return self._config_manager.get_config(const.APP_VERSION)

    @app_version.setter
    def app_version(self, new_value):
        self._config_manager.set_config(const.APP_VERSION, new_value)
        self._config_manager.save_config()

    @property
    def next_app_version(self):
        return self._next_app_version

    @next_app_version.setter
    def next_app_version(self, new_value):
        self._next_app_version = new_value

    @property
    def translation_version(self):
        return self._config_manager.get_config(const.TRANSLATION_VERSION)

    @translation_version.setter
    def translation_version(self, new_value):
        self._config_manager.set_config(const.TRANSLATION_VERSION, new_value)
        self._config_manager.save_config()

    @property
    def next_translation_version(self):
        return self._next_translation_version

    @next_translation_version.setter
    def next_translation_version(self, new_value):
        self._next_translation_version = new_value

    @property
    def launch_mode(self):
        return self._config_manager.get_config(const.LAUNCH_MODE)

    @launch_mode.setter
    def launch_mode(self, new_value):
        self._config_manager.set_config(const.LAUNCH_MODE, new_value)
        self._config_manager.save_config()

    @property
    def local_path(self):
        return self._config_manager.get_config(const.LOCAL_PATH)

    @local_path.setter
    def local_path(self, new_value):
        self._config_manager.set_config(const.LOCAL_PATH, new_value)
        self._config_manager.save_config()

    @property
    def app_update_server_url(self):
        return self._config_manager.get_config(const.APP_UPDATE_SERVER_URL)

    @app_update_server_url.setter
    def app_update_server_url(self, new_value):
        self._config_manager.set_config(const.APP_UPDATE_SERVER_URL, new_value)
        self._config_manager.save_config()

    @property
    def translation_update_server_url(self):
        return self._config_manager.get_config(const.TRANSLATION_UPDATE_SERVER_URL)

    @translation_update_server_url.setter
    def translation_update_server_url(self, new_value):
        self._config_manager.set_config(const.TRANSLATION_UPDATE_SERVER_URL, new_value)
        self._config_manager.save_config()
