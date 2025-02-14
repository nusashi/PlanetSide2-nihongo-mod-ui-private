from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult
from src.NetworkManager import RequestsNetworkManager

class CheckTranslationServerStatusLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.__init__: end")

    def execute(self, *args, **kwargs) -> LogicResult:
        """
        翻訳ファイル用のサーバーの状態を確認する

        Returns:
            LogicResult: サーバーの状態とステータスコード。サーバーURLが設定されていない場合はNoneを返す。
        """
        self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.execute: start")
        try:
            url = self.main_manager.get_config_manager().get_config("translation_server_url")
            self.main_manager.get_error_handler().log_message(f"CheckTranslationServerStatusLogic.execute: url={url}")
            if url:
                network_manager = self.main_manager.get_network_manager()
                if isinstance(network_manager, RequestsNetworkManager):
                    result = network_manager.check_server_status(url)
                    if result:
                        status, code = result
                        self.main_manager.get_error_handler().log_message(f"CheckTranslationServerStatusLogic.execute: status={status}, code={code}")
                        return LogicResult(success=True, value=(status, code))
                    else:
                        self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.execute: Server check failed.")
                        return LogicResult(success=False, error="Server check failed.")
                else:
                    self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.execute: Network manager is not an instance of RequestsNetworkManager.")
                    return LogicResult(success=False, error="Network manager is not an instance of RequestsNetworkManager.")
            else:
                self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.execute: No server URL configured.")
                return LogicResult(success=False, error="No server URL configured.")
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"CheckTranslationServerStatusLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("CheckTranslationServerStatusLogic.execute: end")
