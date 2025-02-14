from src.IMainManagerAdapter import IMainManagerAdapter
from src.ILogic import ILogic, LogicResult
import os
import shutil


class CopyFontFileLogic(ILogic):
    def __init__(self, main_manager: IMainManagerAdapter):
        """
        コンストラクタ

        Args:
            main_manager: IMainManagerAdapterのインターフェース
        """
        self.main_manager = main_manager

    def execute(self, local_path: str, *args, **kwargs) -> LogicResult:
        """
        MyFont.ttfファイルをPlanetSide2のインストールディレクトリにコピーする。

        Args:
            local_path (str): PlanetSide2のインストールディレクトリのパス。

        Returns:
            LogicResult: コピーの成否
        """
        self.main_manager.get_error_handler().log_message(f"CopyFontFileLogic.execute: start. local_path={local_path}")
        try:
            base_dir = self.main_manager.get_base_dir()
            font_path = os.path.join(base_dir, "data", "MyFont.ttf")

            if not os.path.exists(font_path):
                raise FileNotFoundError(f"Font file not found: {font_path}")

            os.makedirs(os.path.join(local_path, "UI", "Resource", "Fonts"), exist_ok=True)
            shutil.copy2(
                font_path,
                os.path.join(local_path, "UI", "Resource", "Fonts", "Geo-Md.ttf"),
            )
            shutil.copy2(
                font_path,
                os.path.join(local_path, "UI", "Resource", "Fonts", "Ps2GeoMdRosaVerde.ttf"),
            )
            self.main_manager.get_error_handler().log_message("CopyFontFileLogic.execute: success")
            return LogicResult(success=True)
        except Exception as e:
            self.main_manager.get_error_handler().log_message(f"CopyFontFileLogic.execute: error: {str(e)}")
            return LogicResult(success=False, error=str(e))
