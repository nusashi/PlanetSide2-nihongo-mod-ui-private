import os
import sys
import time
import subprocess
import shutil
from urllib.parse import urljoin, urlparse
from typing import Callable, List, Optional, Tuple, Dict
import requests
from packaging import version
from const import const
from system.config_manager import JsonConfigManager
from system.github_resource_manager import GitHubResourceManager
from system.github_release_scraper import GitHubReleaseScraper
from ui.ui_manager import UIManager


class MainManager:
    def __init__(self, data_dir):
        print("MainManagerインスタンス作成")
        # インスタンス変数宣言
        self._data_dir = data_dir
        if not self._data_dir:
            self._data_dir = os.path.dirname(os.path.abspath(__file__))
        self._next_app_version = const.DEFAULT_APP_VERSION
        self._next_translation_version = const.DEFAULT_TRANSLATION_VERSION
        self._status_string = ""  # ステータス
        self._config_manager = JsonConfigManager(data_dir)
        self._github_resource_manager = GitHubResourceManager()
        self.scraper = GitHubReleaseScraper()
        self.ui_manager = UIManager()

    def initialize(self):
        print("初期化")

        # UIマネージャにプロパティのコールバックを登録
        properties_to_register = [
            "status_string",
            "app_version",
            "next_app_version",
            "translation_version",
            "next_translation_version",
            "launch_mode",
            "local_path",
            "app_update_server_url",
            "translation_update_server_url",
        ]
        for prop_name in properties_to_register:
            self.ui_manager.set_property_callbacks(
                prop_name,
                lambda prop_name=prop_name: getattr(self, prop_name),  # getter
                lambda value, prop_name=prop_name: setattr(self, prop_name, value),  # setter
            )

        # ローカル関数としてコールバック関数を定義し、UIマネージャにコールバック関数を登録
        def on_game_launch_clicked():
            self.try_game_launch()
            self.ui_manager.redraw()

        self.ui_manager.set_on_game_launch_clicked_callback(on_game_launch_clicked)

        def on_replace_translation_clicked():
            self.try_translation()
            self.ui_manager.redraw()

        self.ui_manager.set_on_replace_translation_clicked_callback(on_replace_translation_clicked)

        def on_update_app_clicked():
            filenames = [
                "PS2JPMod.exe",
                "README.md",
            ]
            downloaded_files = self.download_app_files(self._data_dir, filenames, self.progress_callback)
            self.ui_manager.redraw()
            if downloaded_files and len(downloaded_files) == len(filenames):
                self.status_string = "Appのダウンロードが完了しました。アップデートを開始します。"
                self.ui_manager.update_status_text_ui(self.status_string)
                time.sleep(1)
                subprocess.Popen("data/updater.bat", cwd=os.environ["BASE_DIR"])
                sys.exit(0)

        self.ui_manager.set_on_update_app_clicked_callback(on_update_app_clicked)

        def on_update_translation_clicked():
            # ダウンロードするファイル名のリスト
            filenames = [
                const.JP_DAT_FINE_NAME,
                const.JP_DIR_FILE_NAME,
            ]
            self.download_translation_files(filenames, self.progress_callback)
            self.ui_manager.redraw()

        self.ui_manager.set_on_update_translation_clicked_callback(on_update_translation_clicked)

        def on_check_update_clicked():
            self.check_update()
            self.ui_manager.redraw()

        self.ui_manager.set_on_check_update_clicked_callback(on_check_update_clicked)

        def on_launch_mode_changed(launch_mode: str):
            self.launch_mode = launch_mode
            self.ui_manager.redraw()

        self.ui_manager.set_on_radio_normal_clicked_callback(on_launch_mode_changed)
        self.ui_manager.set_on_radio_steam_clicked_callback(on_launch_mode_changed)

        # 初回起動対応
        is_tutorial = self._config_manager.get_initial_config()

        if version.parse(self.app_version) < version.parse(const.DEFAULT_APP_VERSION):
            self.app_version = const.DEFAULT_APP_VERSION

        self._next_app_version = self.app_version
        self._next_translation_version = self.translation_version
        # アップデート確認
        self.check_update()

        self.ui_manager.show_main_window()
        if is_tutorial:
            # 初回起動時、チュートリアルポップアップを表示
            self.ui_manager.show_tutorial_popup()
        self.ui_manager.run()

    def _check_version_update(self, server_url: str, current_version: str, next_version_attr: str) -> Tuple[Optional[str], Optional[str]]:
        """
        バージョンアップデートを確認する共通関数。
        Args:
            server_url: アップデートサーバーの URL。
            current_version: 現在のバージョン。
            next_version_attr: 次のバージョンを格納する属性名。
        Returns:
            (エラーメッセージ, バージョン) のタプル。
            エラーがない場合はエラーメッセージは None。
            アップデートがない場合は現在のバージョン、ある場合は最新のバージョンを返す。
        """
        repo_info = self.scraper.parse_github_url(server_url)
        if not repo_info:
            return f"無効なアップデートサーバー", current_version
        latest_tag = self.scraper.get_latest_tag(repo_info["owner"], repo_info["repo"])
        if not latest_tag:
            return f"最新タグの取得に失敗", current_version
        try:
            if version.parse(latest_tag) > version.parse(current_version):
                setattr(self, next_version_attr, latest_tag)
                return None, str(version.parse(latest_tag))  # (エラーなし, 最新バージョン)
            else:
                return None, current_version  # (エラーなし, 現在のバージョン)
        except version.InvalidVersion:
            return f"無効なバージョンタグ: {latest_tag}", current_version

    def check_update(self):
        app_version_status = ""
        translation_version_status = ""
        # Appのアップデート確認
        if not self.check_app_update_server_connection():
            print("アップデートサーバーに接続できません")
            app_error, self._next_app_version = "アップデートサーバーに接続できません", self.app_version
        else:
            app_error, self._next_app_version = self._check_version_update(self.app_update_server_url, self.app_version, "next_app_version")

        # 翻訳のアップデート確認
        if not self.check_translation_update_server_connection():
            print("アップデートサーバーに接続できません")
            translation_error, self._next_translation_version = "アップデートサーバーに接続できません", self.translation_version
        else:
            translation_error, self._next_translation_version = self._check_version_update(self.translation_update_server_url, self.translation_version, "next_translation_version")

        # 結果の表示 (UI 更新など)
        if app_error:
            print(app_error)
            app_version_status = f"App:{app_error}"
        else:
            print("次のAppバージョン:", self._next_app_version)

        if translation_error:
            print(translation_error)
            translation_version_status = f"翻訳:{translation_error}"
        else:
            print("次の翻訳バージョン:", self._next_translation_version)

        if app_error is None:
            if version.parse(self._next_app_version) > version.parse(self.app_version):
                app_version_status = f"新しいAppバージョンが利用可能です: {self._next_app_version}"
            else:
                app_version_status = "Appバージョンは最新です"

        if translation_error is None:
            if version.parse(self._next_translation_version) > version.parse(self.translation_version):
                translation_version_status = f"新しい翻訳バージョンが利用可能です: {self._next_translation_version}"
            else:
                app_version_status = "翻訳バージョンは最新です"

        self.status_string = app_version_status + "\n" + translation_version_status

    # ゲーム起動
    def try_game_launch(self) -> bool:
        print("ゲーム起動")
        if self.launch_mode == const.NORMAL_LAUNCH:
            if os.path.exists(self.local_path + "/LaunchPad.exe"):
                subprocess.Popen(self.local_path + "/LaunchPad.exe")
                self.status_string = "ゲームランチャーを起動しました。\n緑のゲージが完全に満タンになったら\n「日本語化」を押してください。"
                return True
            else:
                error_message = "LaunchPad.exe が見つかりません。"
                print(error_message)
                self.status_string = error_message
                return False
        elif self.launch_mode == const.STEAM_LAUNCH:
            os.startfile(const.STEAM_GAME_URI)
            self.status_string = "ゲームランチャーを起動しました。\n緑のゲージが完全に満タンになったら\n「日本語化」を押してください。"
            return True
        else:
            print("不正な起動モードです")
            self.status_string = "不正な起動モードです"
            return False

    # 日本語化
    def try_translation(self) -> bool:
        print("翻訳開始")
        # data フォルダが存在しない場合はエラー
        if not os.path.isdir(self._data_dir):
            print(f"{self._data_dir} フォルダが存在しません")
            self.status_string = f"{self._data_dir} フォルダが存在しません"
            return False

        jp_data_dat_path = os.path.join(self._data_dir, const.JP_DAT_FINE_NAME)
        if not os.path.exists(jp_data_dat_path):
            print(f"{const.JP_DAT_FINE_NAME} が存在しません")
            self.status_string = f"{const.JP_DAT_FINE_NAME} が存在しません"
            return False

        jp_data_dir_path = os.path.join(self._data_dir, const.JP_DIR_FILE_NAME)
        if not os.path.exists(jp_data_dir_path):
            print(f"{const.JP_DIR_FILE_NAME} が存在しません")
            self.status_string = f"{const.JP_DIR_FILE_NAME} が存在しません"
            return False

        font_path = os.path.join(self._data_dir, const.FONT_FILE_NAME)
        if not os.path.exists(font_path):
            print(f"{const.FONT_FILE_NAME} が存在しません")
            self.status_string = f"{const.FONT_FILE_NAME} が存在しません"
            return False

        locale_path = os.path.join(self.local_path, "Locale")
        # Locale フォルダが存在しない場合はエラー
        if not os.path.isdir(locale_path):
            print(f"{locale_path} フォルダが存在しません")
            self.status_string = f"{locale_path} フォルダが存在しません"
            return False

        destination_dat_path = os.path.join(locale_path, const.EN_DAT_FINE_NAME)
        if not os.path.exists(destination_dat_path):
            print(f"{const.EN_DAT_FINE_NAME} が存在しません")
            self.status_string = f"{const.EN_DAT_FINE_NAME} が存在しません"
            return False

        destination_dir_path = os.path.join(locale_path, const.EN_DIR_FILE_NAME)
        if not os.path.exists(destination_dir_path):
            print(f"{const.EN_DIR_FILE_NAME} が存在しません")
            self.status_string = f"{const.EN_DIR_FILE_NAME} が存在しません"
            return False

        ui_resource_fonts_path = os.path.join(self.local_path, "UI", "Resource", "Fonts")
        # Fonts フォルダが存在しない場合はエラー
        if not os.path.isdir(ui_resource_fonts_path):
            print(f"{ui_resource_fonts_path} フォルダが存在しません")
            self.status_string = f"{ui_resource_fonts_path} フォルダが存在しません"
            return False

        # TODO 足りないときはアップデートで対応
        # チェックするフォントのリスト (ファイル名のみ)
        required_fonts = [
            "Geo-Md.ttf",
            "Ps2GeoMdRosaVerde.ttf",
        ]
        existing_font_paths = []  # 存在が確認されたフォントのパスを格納するリスト

        for font_name in required_fonts:
            destination_font_path = os.path.join(ui_resource_fonts_path, font_name)
            if os.path.exists(destination_font_path):
                existing_font_paths.append(destination_font_path)  # 存在したらリストに追加
            else:
                print(f"{font_name} が存在しません")
                self.status_string = f"{font_name} が存在しません"
                return False

        try:
            shutil.copy2(jp_data_dat_path, destination_dat_path)
            shutil.copy2(jp_data_dir_path, destination_dir_path)
            for destination_font_path in existing_font_paths:
                shutil.copy2(font_path, destination_font_path)
            print("翻訳終了")
            self.status_string = "日本語化が完了しました。\n「PLAY」ボタンを押してゲームを実行してください"
            return True
        except Exception as e:
            print(f"翻訳失敗 {str(e)}")
            self.status_string = f"日本語化に失敗しました。: {e}"
            return False

    # AppUpdateServer疎通確認関数
    def check_app_update_server_connection(self) -> bool:
        """
        アプリケーションアップデートサーバーへの疎通確認を行う。
        """
        repo_info = self.scraper.parse_github_url(self.app_update_server_url)
        if not repo_info:
            print("無効なAppアップデートサーバーURL")
            return False
        return self._github_resource_manager.check_connection(repo_info["owner"], repo_info["repo"])

    # TranslationUpdateServer疎通確認関数
    def check_translation_update_server_connection(self) -> bool:
        """
        翻訳アップデートサーバーへの疎通確認を行う。
        """
        repo_info = self.scraper.parse_github_url(self.translation_update_server_url)
        if not repo_info:
            print("無効な翻訳アップデートサーバーURL")
            return False
        return self._github_resource_manager.check_connection(repo_info["owner"], repo_info["repo"])

    # プログレスコールバック関数を定義
    def progress_callback(self, filename: str, file_number: int, total_files: int):
        self.status_string = f"{filename} ({file_number}/{total_files}) ダウンロード完了"
        self.ui_manager.update_status_text_ui(self.status_string)

    # 最新のAppダウンロード
    def download_app_files(self, destination_dir: str, filenames: List[str], progress_callback: Optional[Callable[[str, int, int], None]] = None) -> Optional[List[str]]:
        """
        アプリケーションの最新版（複数ファイル）をダウンロードする。

        Args:
            destination_dir: 保存先のディレクトリ。
            filenames: ダウンロードするファイル名のリスト。
            progress_callback: 進捗コールバック関数。
                引数: ファイル名, 現在のファイル番号, ファイル総数

        Returns:
            ダウンロードしたファイルのパスのリスト。失敗した場合は None。
        """
        repo_info = self.scraper.parse_github_url(self.app_update_server_url)
        if not repo_info:
            print("無効なAppアップデートサーバーURL")
            self.status_string = "無効なAppアップデートサーバーURL"
            return None

        owner = repo_info["owner"]
        repo = repo_info["repo"]
        tag = self.scraper.get_latest_tag(owner, repo)
        if not tag:
            print("Appアップデート用の最新タグを取得できませんでした")
            self.status_string = "Appアップデート用の最新タグを取得できませんでした"
            return None

        downloaded_files = []
        for filename in filenames:
            try:
                # 個々のファイルのダウンロード
                file_path = self._github_resource_manager.download_asset(owner, repo, tag, filename, destination_dir)

                downloaded_files.append(file_path)
                if progress_callback:
                    # ファイル名, 現在のファイル番号(常に1), ファイル総数(filenamesの数)
                    progress_callback(filename, len(downloaded_files), len(filenames))

            except (requests.exceptions.RequestException, FileNotFoundError, ValueError) as e:
                print(f"Download failed for {filename}: {e}")
                self.status_string = f"{filename}のダウンロードに失敗しました: {e}"
                return None  # 失敗したら None を返す

        if downloaded_files:
            return downloaded_files  # ダウンロードしたファイルのパスのリストを返す
        else:
            self.status_string = "Appのダウンロードに失敗しました"
            return None

    # 翻訳ファイルのダウンロード関数
    def download_translation_files(self, filenames: List[str], progress_callback: Optional[Callable[[str, int, int], None]] = None) -> Optional[List[str]]:
        """
        翻訳ファイルとフォントファイルの最新版をダウンロードする。

        Args:
            filenames: ダウンロードするファイル名のリスト。
            progress_callback: 進捗コールバック関数。
                引数: ファイル名, 現在のファイル番号, ファイル総数

        Returns:
            ダウンロードしたファイルのパスのリスト。失敗した場合は None。
        """
        repo_info = self.scraper.parse_github_url(self.translation_update_server_url)
        if not repo_info:
            print("無効な翻訳アップデートサーバーURL")
            self.status_string = "無効な翻訳アップデートサーバーURL"
            return None

        owner = repo_info["owner"]
        repo = repo_info["repo"]
        tag = self.scraper.get_latest_tag(owner, repo)
        if not tag:
            print("翻訳アップデート用の最新タグを取得できませんでした")
            self.status_string = "翻訳アップデート用の最新タグを取得できませんでした"
            return None

        downloaded_files = []
        for filename in filenames:
            try:
                # 個々のファイルのダウンロード
                file_path = self._github_resource_manager.download_asset(owner, repo, tag, filename, self._data_dir)

                downloaded_files.append(file_path)
                if progress_callback:
                    # ファイル名, 現在のファイル番号(常に1), ファイル総数(filenamesの数)
                    progress_callback(filename, len(downloaded_files), len(filenames))

            except (requests.exceptions.RequestException, FileNotFoundError, ValueError) as e:
                print(f"Download failed for {filename}: {e}")
                self.status_string = f"{filename}のダウンロードに失敗しました: {e}"
                return None  # 失敗したら None を返す

        if downloaded_files:
            self.status_string = "翻訳ファイルのダウンロードが完了しました。"
            # バージョンを更新する
            self.translation_version = self._next_translation_version
            return downloaded_files  # ダウンロードしたファイルのパスのリストを返す
        else:
            self.status_string = "翻訳ファイルのダウンロードに失敗しました"
            return None

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
