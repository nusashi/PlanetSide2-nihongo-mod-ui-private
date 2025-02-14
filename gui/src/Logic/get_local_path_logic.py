from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult

class GetLocalPathLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("GetLocalPathLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("GetLocalPathLogic.__init__: end")

    def execute(self, *args, **kwargs) -> LogicResult:
        """
        現在のローカルパスを取得する
        """
        self.main_manager.get_error_handler().log_message("GetLocalPathLogic.execute: start")
        try:
            path = self.main_manager.get_config_manager().get_config("local_path")
            self.main_manager.get_error_handler().log_message(f"GetLocalPathLogic.execute: path={path}")
            return LogicResult(success=True, value=path)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"GetLocalPathLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("GetLocalPathLogic.execute: end")
