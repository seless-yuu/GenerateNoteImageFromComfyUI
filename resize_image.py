import argparse
from PIL import Image

def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='画像をリサイズするツール')
    parser.add_argument('--input', required=True, help='入力画像のパス')
    parser.add_argument('--output', required=True, help='出力画像のパス')
    parser.add_argument('--width', type=int, required=True, help='目標の幅（ピクセル）')
    parser.add_argument('--height', type=int, required=True, help='目標の高さ（ピクセル）')
    parser.add_argument('--quality', type=int, default=80, help='WebP画像の品質（0-100、デフォルト80）')
    return parser.parse_args()

def resize_image(input_path, output_path, target_width, target_height, quality=80):
    """画像をリサイズしてWebP形式で保存"""
    try:
        # 画像を開く
        with Image.open(input_path) as image:
            # 元のサイズとアスペクト比を取得
            original_width, original_height = image.size
            original_aspect = original_width / original_height
            
            # 目標サイズのアスペクト比を計算
            target_aspect = target_width / target_height
            
            # アスペクト比の差を計算
            aspect_difference = abs(original_aspect - target_aspect)
            if aspect_difference > 0.01:  # 1%以上の差がある場合は警告
                print(f"警告: アスペクト比が異なります（元: {original_aspect:.3f}, 目標: {target_aspect:.3f}）")
                print(f"元のサイズ: {original_width}x{original_height}")
                print("アスペクト比を維持したままリサイズします")
            
            # アスペクト比を維持したままリサイズ
            if original_aspect > target_aspect:
                # 幅を基準にリサイズ
                new_width = target_width
                new_height = int(target_width / original_aspect)
            else:
                # 高さを基準にリサイズ
                new_height = target_height
                new_width = int(target_height * original_aspect)
            
            # リサイズ実行（Lanczosフィルタを使用）
            resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # WebP形式で保存
            resized_image.save(
                output_path,
                'WEBP',
                quality=quality,
                lossless=False,
                method=4
            )
            
            print(f"リサイズ: {original_width}x{original_height} → {new_width}x{new_height}")
            print(f"保存しました: {output_path}")
            
    except Exception as e:
        raise Exception(f"画像のリサイズに失敗しました: {e}")

def main():
    try:
        args = parse_arguments()
        resize_image(args.input, args.output, args.width, args.height, args.quality)
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1)

if __name__ == "__main__":
    main() 