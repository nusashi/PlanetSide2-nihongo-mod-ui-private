# Tech Context

このプロジェクトは、Python で実装されており、以下のライブラリを使用します。

*   **requests:** HTTP リクエストを送信するために使用。GitHub API との通信に利用。
*   **PySide6:** GUI を構築するために使用。
*   **packaging:** バージョン比較に使用。
*   **urllib.parse:** URLを解析するために使用。
*   **Nuitka:** Python コードをコンパイルして実行ファイルを生成するために使用。
*   **osslsigncode:** 実行ファイルに証明書を署名するために使用。

## 開発環境

*   Python
*   PySide6
*   requests
*   packaging
*   urllib.parse
*   Nuitka
*   osslsigncode

## 開発手順

1.  必要なライブラリをインストールします。
    ```
    pip install -r project_root/requirements.txt
    ```
2.  `project_root/build.bat` を実行して、アプリケーションをコンパイルし、証明書で署名します。
3.  `project_root/output` フォルダに生成された `PS2JPMod.exe` を実行して、アプリケーションを起動します。

## 依存関係

*   requests
*   PySide6
*   packaging
*   urllib.parse
*   Nuitka
*   osslsigncode
