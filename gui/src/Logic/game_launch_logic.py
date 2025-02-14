import os
import subprocess
from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult


class GameLaunchLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager
        self.main_manager.get_error_handler().log_message("GameLaunchLogic.__init__: start")
        self.main_manager.get_error_handler().log_message("GameLaunchLogic.__init__: end")

    def execute(self, launch_mode: int, local_path: str, *args, **kwargs) -> LogicResult:
        """
        ゲームを起動する。

        Args:
            launch_mode (int): 起動モード (1: 通常起動, 2: Steam経由)
            local_path (str): PlanetSide2のインストールパス

        Returns:
            LogicResult: 起動の成否
        """
        self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: start. launch_mode={launch_mode}, local_path={local_path}")
        try:
            if launch_mode == 1:
                if os.path.exists(local_path + "/LaunchPad.exe"):
                    self.main_manager.get_error_handler().log_message("GameLaunchLogic.execute: Launching via LaunchPad.exe")
                    subprocess.Popen(local_path + "/LaunchPad.exe")
                else:
                    error_message = "LaunchPad.exe が見つかりません。"
                    self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: error: {error_message}")
                    raise FileNotFoundError(error_message)
            elif launch_mode == 2:
                self.main_manager.get_error_handler().log_message("GameLaunchLogic.execute: Launching via Steam")
                os.startfile("steam://run/218230")
            else:
                error_message = "起動モードが不正です。"
                self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: error: {error_message}")
                raise ValueError(error_message)
            self.main_manager.get_error_handler().log_message("GameLaunchLogic.execute: success")
            return LogicResult(success=True)
        except FileNotFoundError as e:
            self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: error: {str(e)}")
            return LogicResult(success=False, error=str(e))
        except ValueError as e:
            self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: error: {str(e)}")
            return LogicResult(success=False, error=str(e))
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"GameLaunchLogic.execute: error: {str(e)}")
            return LogicResult(success=False, error=str(e))
        finally:
            self.main_manager.get_error_handler().log_message("GameLaunchLogic.execute: end")
