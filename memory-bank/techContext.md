# Tech Context

このプロジェクトは、Python で実装されており、以下のライブラリを使用します。

*   **requests:** HTTP リクエストを送信するために使用されます。サーバーとの通信、翻訳データのダウンロード、アップデート確認などに利用されます。
*   **PySide6:** GUI を構築するために使用されます。
*   **logging:** ログ出力をするために使用されます。
*   **ErrorHandler:** エラー処理を集約し、ログ出力とユーザーへの通知を行うモジュールです。

## 開発環境

*   Python 3.12.8
*   PySide6
*   requests
*   logging

## 開発手順

1.  必要なライブラリをインストールします。
    ```
    pip install -r requirements.txt
    ```
2.  `gui/main.py` を実行してアプリケーションを起動します。

## 技術的な制約

*   ファイルパスのハードコーディングの排除
*   エラー処理の改善
*   設定ファイルの管理の改善
*   コードの可読性の向上 (再設計によりほぼ解消)

## 依存関係

*   requests
*   PySide6
*   logging
*   ErrorHandler
