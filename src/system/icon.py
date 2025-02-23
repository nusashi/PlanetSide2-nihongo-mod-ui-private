from PIL import Image
import sys


def convert_webp_to_ico(webp_path, ico_path):
    try:
        # WebPファイルを読み込む
        with Image.open(webp_path) as img:
            # ICOファイルに保存するサイズを指定（例: 16x16, 32x32, 64x64）
            sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            # ICOファイルに保存
            img.save(ico_path, format="ICO", sizes=sizes)
        print(f"Successfully converted {webp_path} to {ico_path}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <input_webp> <output_ico>")
    else:
        webp_path = sys.argv[1]
        ico_path = sys.argv[2]
        convert_webp_to_ico(webp_path, ico_path)
