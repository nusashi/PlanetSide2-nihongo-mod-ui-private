from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult


class SetLaunchModeLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("SetLaunchModeLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("SetLaunchModeLogic.__init__: end")

    def execute(self, mode: int, *args, **kwargs) -> LogicResult:
        """
        起動モードを設定する

        Args:
            mode (int): 設定する起動モード

        Returns:
            LogicResult: 設定の成否
        """
        self.main_manager.get_error_handler().log_message("SetLaunchModeLogic.execute: start")
        try:
            self.main_manager.get_config_manager().set_config("launch_mode", mode)
            self.main_manager.get_config_manager().save_config()
            self.main_manager.get_error_handler().log_message(f"SetLaunchModeLogic.execute: Set launch_mode to {mode}")
            return LogicResult(success=True)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"SetLaunchModeLogic.execute: error={str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("SetLaunchModeLogic.execute: end")
