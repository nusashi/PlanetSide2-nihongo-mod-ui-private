import os
import subprocess
from abc import ABC, abstractmethod


class GameLauncherInterface(ABC):
    @abstractmethod
    def launch_game(self, launch_mode, local_path):
        """ゲームを起動する"""
        pass


class DefaultGameLauncher(GameLauncherInterface):
    def launch_game(self, launch_mode, local_path):
        if launch_mode == 1:
            if os.path.exists(local_path + "/LaunchPad.exe"):
                subprocess.Popen(local_path + "/LaunchPad.exe")
            else:
                raise FileNotFoundError("LaunchPad.exe が見つかりません。")
        elif launch_mode == 2:
            os.startfile("steam://run/218230")
        else:
            raise ValueError("起動モードが不正です。")
