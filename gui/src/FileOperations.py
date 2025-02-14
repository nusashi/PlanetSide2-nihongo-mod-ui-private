import os
import shutil
from abc import ABC, abstractmethod
import logging

class FileOperationsInterface(ABC):
    @abstractmethod
    def copy_translation_files(self, local_path):
        """翻訳ファイルをコピーする"""
        pass


class DefaultFileOperations(FileOperationsInterface):
    def __init__(self, config_manager, base_dir):
        self.config_manager = config_manager
        self.base_dir = base_dir

    def copy_translation_files(self, local_path):
        """
        翻訳ファイルとフォントファイルをPlanetSide2のインストールディレクトリにコピーする。

        Args:
            local_path (str): PlanetSide2のインストールディレクトリのパス。

        Raises:
            OSError: ディレクトリの作成に失敗した場合。
            FileNotFoundError: ファイルまたはディレクトリが存在しない場合。
            Exception: ファイルのコピーに失敗した場合。
        """
        jp_data_dat_path = os.path.join(self.base_dir, "data", "ja_jp_data.dat")
        jp_data_dir_path = os.path.join(self.base_dir, "data", "ja_jp_data.dir")
        font_path = os.path.join(self.base_dir, "data", "MyFont.ttf")

        logging.debug(f"copy_translation_files: jp_data_dat_path = {jp_data_dat_path}")
        logging.debug(f"copy_translation_files: jp_data_dir_path = {jp_data_dir_path}")
        logging.debug(f"copy_translation_files: font_path = {font_path}")

        # ファイルとディレクトリの存在を確認
        if not os.path.exists(jp_data_dat_path):
            raise FileNotFoundError(f"Translation file not found: {jp_data_dat_path}")
        if not os.path.exists(jp_data_dir_path):
            raise FileNotFoundError(f"Translation file not found: {jp_data_dir_path}")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file not found: {font_path}")

        try:
            # 必要なディレクトリを作成する
            os.makedirs(os.path.join(local_path, "Locale"), exist_ok=True)
            os.makedirs(
                os.path.join(local_path, "UI", "Resource", "Fonts"), exist_ok=True
            )

            # 翻訳ファイルをコピーする
            logging.debug(f"copy_translation_files: copying {jp_data_dat_path} to {os.path.join(local_path, 'Locale', 'en_us_data.dat')}")
            try:
                shutil.copy2(
                    jp_data_dat_path, os.path.join(local_path, "Locale", "en_us_data.dat")
                )
            except OSError as e:
                logging.error(f"copy_translation_files: OSError: {e}")
                raise Exception(f"Failed to copy file: {e}") from e
            logging.debug(f"copy_translation_files: copying {jp_data_dir_path} to {os.path.join(local_path, 'Locale', 'en_us_data.dir')}")
            try:
                shutil.copy2(
                    jp_data_dir_path, os.path.join(local_path, "Locale", "en_us_data.dir")
                )
            except OSError as e:
                logging.error(f"copy_translation_files: OSError: {e}")
                raise Exception(f"Failed to copy file: {e}") from e

            # フォントファイルをコピーする
            logging.debug(f"copy_translation_files: copying {font_path} to {os.path.join(local_path, 'UI', 'Resource', 'Fonts', 'Geo-Md.ttf')}")
            try:
                shutil.copy2(
                    font_path,
                    os.path.join(local_path, "UI", "Resource", "Fonts", "Geo-Md.ttf"),
                )
            except OSError as e:
                logging.error(f"copy_translation_files: OSError: {e}")
                raise Exception(f"Failed to copy file: {e}") from e
            logging.debug(f"copy_translation_files: copying {font_path} to {os.path.join(local_path, 'UI', 'Resource', 'Fonts', 'Ps2GeoMdRosaVerde.ttf')}")
            try:
                shutil.copy2(
                    font_path,
                    os.path.join(
                        local_path, "UI", "Resource", "Fonts", "Ps2GeoMdRosaVerde.ttf"
                    ),
                )
            except OSError as e:
                logging.error(f"copy_translation_files: OSError: {e}")
                raise Exception(f"Failed to create directories or copy files: {e}") from e

        except Exception as e:
            logging.error(f"copy_translation_files: Exception: {e}")
            raise Exception(f"Failed to copy or find translation files: {e}") from e
