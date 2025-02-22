# Active Context

## 次のステップ

*   特になし (今後の計画は全て白紙化されたため)

## 追加のコンテキスト

*   Nuitka でのコンパイルと証明書署名の手順を確立しました。
*   `build.bat` を作成し、Nuitka でのコンパイル、証明書署名、不要なファイルの削除を自動化しました。
*   証明書署名に必要なパスワードは `.env` ファイルで管理するようにしました。
*   `updater.bat`を作成し、アプリケーションのアップデート時にファイルの置き換えと`PS2JPMod.exe`の起動を行うようにしました。
*   `main_manager.py`の`download_app_files`関数でダウンロードするファイル名を指定しました。
*   `main_manager.py`の`initialize`関数に、起動時に`config.json`の`app_version`が`const.py`のバージョンより古かったら、自動的に`const.py`のバージョンに書き換える処理を追加しました。
*   `build.bat`で`PS2JPMod.exe`を`output`フォルダにコピーする際に、`README.md`もコピーするように修正しました。
*   SHAチェックはオミットしました。
*   `const.py`のバージョンは手動で更新します。
