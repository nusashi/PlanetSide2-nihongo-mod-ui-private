import requests
from bs4 import BeautifulSoup
import re
import hashlib
from urllib.parse import urlparse
from typing import Optional, Dict


class GitHubReleaseScraper:
    """GitHub Releases ページから情報を取得するクラス"""

    def __init__(self):
        self.base_url = "https://github.com"

    def parse_github_url(self, url: str) -> Optional[Dict[str, str]]:
        """GitHub の URL からオーナーとリポジトリ名を抽出する"""
        parsed_url = urlparse(url)
        if parsed_url.netloc != "github.com":
            return None
        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) < 2:
            return None
        return {"owner": path_parts[0], "repo": path_parts[1]}

    def get_latest_release_page_html(self, owner: str, repo: str) -> Optional[str]:
        """最新リリースのページの HTML を取得する"""
        url = f"{self.base_url}/{owner}/{repo}/releases/latest"
        try:
            response = requests.get(url, allow_redirects=True)  # リダイレクトを許可
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException:
            return None

    def get_latest_tag(self, owner: str, repo: str) -> Optional[str]:
        """最新リリースのタグ名を取得する"""
        html = self.get_latest_release_page_html(owner, repo)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")
        match = re.search(r"/releases/tag/(.+)$", soup.find("a", href=re.compile(r"/releases/tag/"))["href"])
        if match:
            return match.group(1)

        return None
