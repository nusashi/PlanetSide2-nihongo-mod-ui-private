﻿@echo off
chcp 65001 > nul
setlocal

:: output フォルダのパスを設定
set "OUTPUT_DIR=output"

:: output フォルダの中身を全て削除 (フォルダ自体は残す)
rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

:: .env ファイルから環境変数を読み込む
for /f "usebackq delims=" %%i in (".env") do (
  set "%%i"
)

:: 環境変数が設定されていない場合はエラー
if "%PFX_PASSWORD%"=="" (
    echo Error: PFX_PASSWORD environment variable not set.
    exit /b 1
)

:: const.py を実行してバージョン情報を output/version.txt に出力 (output フォルダのパスを渡す)
python src\const\const.py "%OUTPUT_DIR%"

:: output/version.txt からバージョン情報を読み込む
set /p APP_VERSION=<%OUTPUT_DIR%\version.txt

:: バージョン情報を使って ZIP ファイル名を作成
set "ZIP_FILENAME=PS2JPMod_v%APP_VERSION%.zip"

:: Nuitka でコンパイル
@REM python -m nuitka --onefile --onefile-as-archive --windows-console-mode=force --enable-plugin=pyside6 --windows-icon-from-ico=src/resources/ps2jpmod.ico --include-data-files=src/resources/ps2jpmod.ico=resources/ps2jpmod.ico --output-dir=%OUTPUT_DIR% --output-filename=PS2JPMod_unsigned --clean-cache=all --remove-output src/main.py
python -m nuitka --onefile --onefile-as-archive --windows-console-mode=disable --enable-plugin=pyside6 --windows-icon-from-ico=src/resources/ps2jpmod.ico --include-data-files=src/resources/ps2jpmod.ico=resources/ps2jpmod.ico --output-dir=%OUTPUT_DIR% --output-filename=PS2JPMod_unsigned --clean-cache=all --remove-output src/main.py

:: 署名前後のファイルパスを設定
set "INPUT_EXE=%OUTPUT_DIR%\PS2JPMod_unsigned.exe"
set "OUTPUT_EXE=%OUTPUT_DIR%\PS2JPMod.exe"

:: 証明書の署名
"%OSSLSIGNCODE_PATH%" sign -pkcs12 "%PFX_PATH%" -pass "%PFX_PASSWORD%" -in "%INPUT_EXE%" -out "%OUTPUT_EXE%"

:: 署名前のファイルを削除
del "%INPUT_EXE%"
copy はじめにお読みください.txt "%OUTPUT_DIR%"

:: 一時フォルダを作成 (既に存在する場合は中身を削除)
if exist "temp_dir\" (
  rmdir /s /q "temp_dir"
)
mkdir "temp_dir"

:: 必要なファイルを一時フォルダにコピー
mkdir "temp_dir\PS2日本語化Mod"
copy "%OUTPUT_DIR%\PS2JPMod.exe" "temp_dir\PS2日本語化Mod\"
copy "はじめにお読みください.txt" "temp_dir\PS2日本語化Mod\"
mkdir "temp_dir\PS2日本語化Mod\data"
xcopy "data\fonts" "temp_dir\PS2日本語化Mod\data\fonts\" /E /I /H /Y
copy "data\updater.bat" "temp_dir\PS2日本語化Mod\data\"

:: カレントディレクトリを一時フォルダに変更
pushd "temp_dir"

:: 7-Zip で圧縮 (UTF-8 を指定)
"C:\Program Files\7-Zip\7z.exe" a -tzip -mcp=65001 "../%OUTPUT_DIR%\%ZIP_FILENAME%" "PS2日本語化Mod\*" -r

:: カレントディレクトリを元に戻す
popd

:: 一時フォルダを削除
rmdir /s /q "temp_dir"

echo ZIPファイルを作成しました: %OUTPUT_DIR%\%ZIP_FILENAME%

endlocal
pause