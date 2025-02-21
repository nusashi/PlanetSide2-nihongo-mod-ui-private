import requests
import os
from urllib.parse import urljoin
from typing import Callable, Optional


class GitHubResourceManager:
    """
    GitHub リポジトリのリソースを管理するクラス (ダウンロードに特化)。
    """

    def __init__(self, token: str = None):
        """
        初期化。

        Args:
            token: GitHub Personal Access Token (オプション)。
        """
        self.token = token
        self.base_url = "https://github.com"

    def _get_headers(self) -> dict:
        """認証情報を含むヘッダーを取得する。"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def check_connection(self, owner: str, repo: str) -> bool:
        """
        指定されたリポジトリへの疎通確認を行う。
        /releases/latest へのリダイレクトを確認

        Args:
            owner: リポジトリのオーナー。
            repo: リポジトリ名。

        Returns:
            疎通が確認できれば True、そうでなければ False。
        """
        url = f"{self.base_url}/{owner}/{repo}/releases/latest"
        try:
            response = requests.get(url, headers=self._get_headers(), allow_redirects=False)
            response.raise_for_status()  # 200番台以外のステータスコードはエラー
            return response.status_code == 302  # 302 (リダイレクト) なら OK
        except requests.exceptions.RequestException:
            return False

    def download_asset(self, owner: str, repo: str, tag: str, filename: str, destination_dir: str) -> str:
        """
        指定されたリリースからファイルをダウンロードする。
        Args:
            owner: リポジトリのオーナー。
            repo: リポジトリ名。
            tag: リリースのタグ名。
            filename: ダウンロードするファイル名。
            destination_dir: 保存先のディレクトリ。

        Returns:
            保存先のファイルパス。
        Raises:
            requests.exceptions.RequestException: リクエストエラーが発生した場合。
            FileNotFoundError: ファイルが見つからない場合。
        """
        download_url = urljoin(
            self.base_url,
            f"/{owner}/{repo}/releases/download/{tag}/{filename}",
        )

        # ファイルをダウンロード (stream=True でストリーミング)
        response = requests.get(download_url, stream=True, headers=self._get_headers())
        response.raise_for_status()

        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(destination_dir, filename)

        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        return destination_path
