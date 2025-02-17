import requests
import os
import re
from urllib.parse import urljoin, urlparse
from typing import Callable, List, Optional, Dict, Union


class GitHubResourceManager:
    """
    複数の GitHub リポジトリのリソースを管理するクラス。
    """

    def __init__(self, token: str = None):
        """
        初期化。

        Args:
            token: GitHub Personal Access Token (オプション)。認証が必要な場合や、APIレート制限を緩和したい場合に指定。
        """
        self.token = token
        self.base_url = "https://github.com"

    def _get_headers(self) -> dict:
        """認証情報を含むヘッダーを取得する。"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        return headers

    def _parse_github_url(self, url: str) -> Optional[Dict[str, str]]:
        """
        GitHub の URL からオーナーとリポジトリ名を抽出する。

        Args:
            url: GitHub の URL。

        Returns:
            辞書形式の情報 (owner, repo)。抽出できない場合は None。
        """
        parsed_url = urlparse(url)
        if parsed_url.netloc != "github.com":
            return None

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            return None

        return {"owner": path_parts[0], "repo": path_parts[1]}

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

    def get_latest_tag(self, owner: str, repo: str) -> Optional[str]:
        """
        指定されたリポジトリの最新リリースのタグ名を取得する。

        Args:
            owner: リポジトリのオーナー。
            repo: リポジトリ名。

        Returns:
            最新リリースのタグ名。取得できない場合は None。
        """
        url = f"{self.base_url}/{owner}/{repo}/releases/latest"
        try:
            response = requests.get(url, headers=self._get_headers(), allow_redirects=False)
            response.raise_for_status()

            if response.status_code == 302:
                redirect_url = response.headers["Location"]
                match = re.search(r"/releases/tag/(.+)$", redirect_url)
                if match:
                    return match.group(1)
        except requests.exceptions.RequestException:
            return None  # エラーの場合は None を返す
        return None

    def download_asset(self, owner: str, repo: str, tag: str, filename: str, destination_dir: str, progress_callback: Optional[Callable[[str, int, int, int], None]] = None) -> str:
        """
        指定されたリリースからファイルをダウンロードする（進捗情報付き）。
        Args:
            owner: リポジトリのオーナー。
            repo: リポジトリ名。
            tag: リリースのタグ名。
            filename: ダウンロードするファイル名。
            destination_dir: 保存先のディレクトリ。
            progress_callback: 進捗状況を通知するコールバック関数 (オプション)。
                引数: ファイル名, 現在のファイル番号, ファイル総数, ダウンロード済みバイト数
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

        downloaded_size = 0  # ダウンロード済みのバイト数

        with open(destination_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if progress_callback:
                        # ファイル名, 現在のファイル番号(常に1), ファイル総数(常に1), ダウンロード済みバイト数 を渡す
                        progress_callback(filename, 1, 1, downloaded_size)
        return destination_path

    def download_latest_assets(self, repositories: List[Dict[str, Union[str, List[str]]]], destination_dir: str, progress_callback: Optional[Callable[[str, int, int, int], None]] = None) -> Dict[str, Union[List[str], str]]:
        """
        複数の GitHub リポジトリの最新リリースの指定されたアセットをダウンロードする。

        Args:
            repositories: リポジトリ情報 (URL とファイル名リスト) のリスト。
                例:
                [
                    {"url": "https://github.com/owner1/repo1", "filenames": ["file1.txt", "file2.zip"]},
                    {"url": "https://github.com/owner2/repo2", "filenames": ["image1.png"]},
                ]
            destination_dir: アセットを保存するディレクトリ。
            progress_callback: 進捗状況を通知するコールバック関数 (省略可能)。
                引数: ファイル名, 現在のファイル番号, ファイル総数, ダウンロード済みバイト数

        Returns:
            ダウンロードに成功した場合は、リポジトリURLをキーとし、ダウンロードしたファイルのパスのリストを値とする辞書。
            失敗した場合は、リポジトリURLをキーとし、エラーメッセージを値とする辞書。
        """
        results = {}
        total_files = sum(len(repo["filenames"]) for repo in repositories)  # 総ファイル数
        downloaded_files_count = 0  # ダウンロード済みのファイル数

        for repo_info in repositories:
            update_url = repo_info["url"]
            filenames = repo_info["filenames"]

            repo_info = self._parse_github_url(update_url)
            if not repo_info:
                results[update_url] = "Invalid GitHub URL."
                continue

            owner = repo_info["owner"]
            repo = repo_info["repo"]

            if not self.check_connection(owner, repo):
                results[update_url] = "Connection check failed."
                continue

            tag = self.get_latest_tag(owner, repo)
            if not tag:
                results[update_url] = "Could not get latest tag."
                continue

            if not filenames:
                results[update_url] = "No files specified for download."
                continue

            downloaded_files = []
            for i, filename in enumerate(filenames):
                try:
                    # 個々のファイルのダウンロード
                    file_path = self.download_asset(owner, repo, tag, filename, destination_dir)
                    downloaded_files.append(file_path)
                    downloaded_files_count += 1

                    if progress_callback:
                        # 全体の進捗を通知: ファイル名, 現在のファイル番号, ファイル総数, ダウンロード済みバイト数(ここでは0)
                        progress_callback(filename, downloaded_files_count, total_files, 0)

                except (requests.exceptions.RequestException, FileNotFoundError) as e:
                    results[update_url] = f"Download failed for {filename}: {e}"
                    downloaded_files = []  # 失敗したら空にする
                    break  # 失敗したら、そのリポジトリのダウンロードは中断

            if downloaded_files:  # 成功していれば結果に追加
                results[update_url] = downloaded_files

        return results
