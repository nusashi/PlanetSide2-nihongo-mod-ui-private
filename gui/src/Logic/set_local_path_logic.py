from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult

class SetLocalPathLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("SetLocalPathLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("SetLocalPathLogic.__init__: end")

    def execute(self, path: str, *args, **kwargs) -> LogicResult:
        """
        ローカルパスを設定する

        Args:
            path (str): 設定するローカルパス

        Returns:
            LogicResult: 設定の成否
        """
        self.main_manager.get_error_handler().log_message("SetLocalPathLogic.execute: start")
        try:
            self.main_manager.get_config_manager().set_config("local_path", path)
            self.main_manager.get_config_manager().save_config()
            self.main_manager.get_error_handler().log_message(f"SetLocalPathLogic.execute: Set local_path to {path}")
            return LogicResult(success=True)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"SetLocalPathLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("SetLocalPathLogic.execute: end")
