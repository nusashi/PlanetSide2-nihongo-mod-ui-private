import requests
from src.ConfigManager import JsonConfigManager
from typing import Union, Tuple


class RequestsNetworkManager:
    def __init__(self):
        self.server_status = False
        self.server_code = 0
        self.config_manager = JsonConfigManager()

    def check_server_status(self, url: str) -> Union[Tuple[bool, int], None]:
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Raises HTTPError for bad requests (4xx or 5xx)
            self.server_status = True
            self.server_code = response.status_code
            return True, response.status_code
        except requests.exceptions.RequestException as e:
            self.server_status = False
            self.server_code = 0
            return None

    def download_file(self, url: str, file_path: str) -> Tuple[bool, str]:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True, ""  # Return True and an empty string for success
        except requests.exceptions.RequestException as e:
            return False, str(e)  # Return False and the error message for failure
