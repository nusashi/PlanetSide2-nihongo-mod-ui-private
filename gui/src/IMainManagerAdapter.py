from abc import ABC, abstractmethod
from src.ConfigManager import JsonConfigManager
from src.ErrorHandler import ErrorHandler
from src.NetworkManager import RequestsNetworkManager
from typing import Union, Tuple


class IMainManagerAdapter(ABC):
    @abstractmethod
    def get_config_manager(self) -> JsonConfigManager:
        pass

    @abstractmethod
    def get_network_manager(self) -> RequestsNetworkManager:
        pass

    @abstractmethod
    def get_error_handler(self) -> ErrorHandler:
        pass

    @abstractmethod
    def check_gui_server_status(self) -> Union[Tuple[bool, int], None]:
        pass

    @abstractmethod
    def check_translation_server_status(self) -> Union[Tuple[bool, int], None]:
        pass

    @abstractmethod
    def get_base_dir(self) -> str:
        pass
