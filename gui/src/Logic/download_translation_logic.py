from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult
from src.MockNetworkManager import MockNetworkManager


class DownloadTranslationLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.__init__: end")

    def execute(self, repo_owner: str, repo_name: str, asset_name: str, download_path: str, *args, **kwargs) -> LogicResult:
        """
        翻訳ファイルをダウンロードする

        Args:
            repo_owner (str): リポジトリのオーナー
            repo_name (str): リポジトリの名前
            asset_name (str): アセットの名前
            download_path (str): ダウンロード先のパス

        Returns:
            LogicResult: ダウンロードの成否
        """
        self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: start")
        try:
            network_manager = self.main_manager.get_network_manager()
            if not isinstance(network_manager, MockNetworkManager):
                self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: Network manager is not an instance of MockNetworkManager.")
                return LogicResult(success=False, error="Network manager is not an instance of MockNetworkManager.")

            latest_release = network_manager.get_latest_release(repo_owner, repo_name)
            self.main_manager.get_error_handler().log_message(f"DownloadTranslationLogic.execute: latest_release={latest_release}")

            if latest_release:
                for asset in latest_release["assets"]:
                    if asset["name"] == asset_name:
                        url = asset["browser_download_url"]
                        success, _ = network_manager.download_file(url, download_path)
                        if success:
                            self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: success")
                            return LogicResult(success=True)
                        else:
                            self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: Failed to download asset.")
                            return LogicResult(success=False, error="Failed to download asset.")
                self.main_manager.get_error_handler().log_message(f"DownloadTranslationLogic.execute: Asset '{asset_name}' not found in the latest release.")
                return LogicResult(success=False, error=f"Asset '{asset_name}' not found in the latest release.")
            else:
                self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: Failed to get the latest release information.")
                return LogicResult(success=False, error="Failed to get the latest release information.")
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"DownloadTranslationLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("DownloadTranslationLogic.execute: end")
