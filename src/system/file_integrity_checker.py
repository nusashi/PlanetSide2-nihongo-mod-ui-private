import hashlib


class FileIntegrityChecker:
    """ファイルの整合性 (ハッシュ値) をチェックするクラス"""

    def calculate_sha256(self, filepath: str) -> str:
        """ファイルの SHA-256 ハッシュ値を計算する"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def verify_file(self, filepath: str, expected_sha256: str) -> bool:
        """ファイルの SHA-256 ハッシュ値を計算し、期待されるハッシュ値と比較する"""
        calculated_sha256 = self.calculate_sha256(filepath)
        return calculated_sha256 == expected_sha256
