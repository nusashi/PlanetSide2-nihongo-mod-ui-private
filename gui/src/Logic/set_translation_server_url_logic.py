from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult


class SetTranslationServerUrlLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("SetTranslationServerUrlLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("SetTranslationServerUrlLogic.__init__: end")

    def execute(self, url: str, *args, **kwargs) -> LogicResult:
        """
        翻訳ファイル用のサーバーURLを設定する

        Args:
            url (str): 設定するURL

        Returns:
            LogicResult: 設定の成否
        """
        self.main_manager.get_error_handler().log_message("SetTranslationServerUrlLogic.execute: start")
        try:
            self.main_manager.get_config_manager().set_config("translation_server_url", url)
            self.main_manager.get_config_manager().save_config()
            self.main_manager.get_error_handler().log_message(f"SetTranslationServerUrlLogic.execute: Set translation_server_url to {url}")
            return LogicResult(success=True)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"SetTranslationServerUrlLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("SetTranslationServerUrlLogic.execute: end")
