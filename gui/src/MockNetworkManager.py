# gui/src/MockNetworkManager.py


class MockNetworkManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.server_status = 1
        self.server_code = 200

    def check_server_status(self):
        return self.server_status, self.server_code

    def get_latest_release(self, repo_owner, repo_name):
        # モックデータを返す
        return {
            "tag_name": "1.1.0",
            "assets": [
                {"name": "version_info.txt", "browser_download_url": "mock_url"},  # 使用しないが、エラーにならないように追加
            ],
        }

    def download_latest_files(self):
        # モック実装では何もしない
        pass

    def check_app_update(self):
        # モック実装では常に更新なしとする
        return False, None

    def get_version_info(self):
        # モックデータを返す
        return "app_version=1.1.0\ntranslation_version=1.0.0"

    def download_asset_content(self, repo_owner, repo_name, asset_name):
        # モックデータを返す
        return "app_version=1.1.0\ntranslation_version=1.0.0"

    def set_local_path(self, path):
        pass
