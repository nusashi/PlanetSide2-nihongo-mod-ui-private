from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult
from src.MockNetworkManager import MockNetworkManager


class CheckUpdateTranslationLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("CheckUpdateTranslationLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("CheckUpdateTranslationLogic.__init__: end")

    def execute(self, repo_owner: str, repo_name: str, *args, **kwargs) -> LogicResult:
        """
        翻訳ファイルのアップデートを確認する

        Args:
            repo_owner (str): リポジトリのオーナー
            repo_name (str): リポジトリの名前

        Returns:
            LogicResult: アップデートが必要かどうか
        """
        self.main_manager.get_error_handler().log_message("CheckUpdateTranslationLogic.execute: start")
        try:
            network_manager = self.main_manager.get_network_manager()
            if not isinstance(network_manager, MockNetworkManager):
                self.main_manager.get_error_handler().log_message("CheckUpdateTranslationLogic.execute: Network manager is not an instance of MockNetworkManager.")
                return LogicResult(success=False, error="Network manager is not an instance of MockNetworkManager.")

            latest_release = network_manager.get_latest_release(repo_owner, repo_name)
            self.main_manager.get_error_handler().log_message(f"CheckUpdateTranslationLogic.execute: latest_release={latest_release}")
            if latest_release:
                for asset in latest_release["assets"]:
                    if asset["name"] == "version_info.txt":
                        version_info = network_manager.download_asset_content(repo_owner, repo_name, "version_info.txt")
                        self.main_manager.get_error_handler().log_message(f"CheckUpdateTranslationLogic.execute: version_info={version_info}")
                        if version_info:
                            for line in version_info.splitlines():
                                key, value = line.split("=")
                                if key == "translation_version":
                                    latest_translation_version = value
                                    current_version = self.main_manager.get_config_manager().get_config("translation_version")
                                    self.main_manager.get_error_handler().log_message(f"CheckUpdateTranslationLogic.execute: latest_translation_version={latest_translation_version}, current_version={current_version}")
                                    return LogicResult(success=True, value=(latest_translation_version != current_version))
                            break
            return LogicResult(success=True, value=False)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"CheckUpdateTranslationLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("CheckUpdateTranslationLogic.execute: end")
