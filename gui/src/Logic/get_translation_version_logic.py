from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult


class GetTranslationVersionLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("GetTranslationVersionLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("GetTranslationVersionLogic.__init__: end")

    def execute(self, *args, **kwargs) -> LogicResult:
        """
        現在の翻訳ファイルバージョンを取得する
        """
        self.main_manager.get_error_handler().log_message("GetTranslationVersionLogic.execute: start")
        try:
            version = self.main_manager.get_config_manager().get_config("translation_version")
            self.main_manager.get_error_handler().log_message(f"GetTranslationVersionLogic.execute: version={version}")
            return LogicResult(success=True, value=version)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"GetTranslationVersionLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("GetTranslationVersionLogic.execute: end")
