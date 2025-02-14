from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult
import os
import shutil


class CopyDatFileLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager

    def execute(self, local_path: str, *args, **kwargs) -> LogicResult:
        """
        ja_jp_data.datファイルをPlanetSide2のインストールディレクトリにコピーする。

        Args:
            local_path (str): PlanetSide2のインストールディレクトリのパス。

        Returns:
            LogicResult: コピーの成否
        """
        self.main_manager.get_error_handler().log_message(f"CopyDatFileLogic.execute: start. local_path={local_path}")
        try:
            base_dir = self.main_manager.get_base_dir()
            jp_data_dat_path = os.path.join(base_dir, "data", "ja_jp_data.dat")

            if not os.path.exists(jp_data_dat_path):
                raise FileNotFoundError(f"Translation file not found: {jp_data_dat_path}")

            os.makedirs(os.path.join(local_path, "Locale"), exist_ok=True)
            shutil.copy2(jp_data_dat_path, os.path.join(local_path, "Locale", "en_us_data.dat"))
            self.main_manager.get_error_handler().log_message("CopyDatFileLogic.execute: success")
            return LogicResult(success=True)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"CopyDatFileLogic.execute: error: {str(e)}")
            return LogicResult(success=False, error=str(e))
