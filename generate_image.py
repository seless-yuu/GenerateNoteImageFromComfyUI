import argparse
import os
import json
import requests
import time
import random
from pathlib import Path
from PIL import Image
from io import BytesIO

def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='プロンプトから画像を生成するツール')
    parser.add_argument('--prompt-file', required=True, help='生成プロンプトが保存されたJSONファイルパス')
    parser.add_argument('--fixed-prompt', required=True, help='固定プロンプト（{content}が生成プロンプトに置換されます）')
    parser.add_argument('--workflow', required=True, help='ComfyUIのワークフローJSONファイルパス')
    parser.add_argument('--output', required=True, help='出力画像のパス（.webp）')
    parser.add_argument('--comfyui-url', default='http://127.0.0.1:8188', help='ComfyUI APIのURL')
    parser.add_argument('--clear-cache', action='store_true', help='実行後にComfyUIのキャッシュをクリアする')
    parser.add_argument('--seed', type=int, help='画像生成用のシード値（指定しない場合はランダム）')
    parser.add_argument('--webp-quality', type=int, default=80, help='WebP画像の品質（0-100、デフォルト80）')
    return parser.parse_args()

def read_workflow(file_path):
    """ComfyUIのワークフローJSONファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"ワークフローファイルの読み込みに失敗しました: {e}")

def read_prompt(file_path):
    """保存されたプロンプトを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['generated_prompt']
    except Exception as e:
        raise Exception(f"プロンプトファイルの読み込みに失敗しました: {e}")

def create_final_prompt(fixed_prompt, generated_prompt):
    """固定プロンプトと生成プロンプトを結合"""
    return fixed_prompt.replace('{content}', generated_prompt)

def find_text_input_node(workflow_data):
    """テキスト入力ノードを探す"""
    for node_id, node in workflow_data.items():
        # CLIPTextEncodeノードを探す
        if 'class_type' in node and node['class_type'] == 'CLIPTextEncode':
            if 'inputs' in node and 'text' in node['inputs'] and isinstance(node['inputs']['text'], str):
                return node_id, 'text'
                
        # Primitiveノードを探す
        elif 'class_type' in node and ('Primitive' in node['class_type'] or 'Input' in node['class_type']):
            if 'inputs' in node and 'string' in node['inputs']:
                return node_id, 'string'
            
    return None, None

def clear_comfyui_cache(comfyui_url):
    """ComfyUIのキャッシュをクリアする"""
    try:
        # モデルとVAEをアンロード
        print("ComfyUIのキャッシュをクリアしています...")
        
        # システム情報を取得
        system_stats_url = f"{comfyui_url}/system_stats"
        response = requests.get(system_stats_url)
        if response.status_code == 200:
            print(f"クリア前のVRAM使用量: {response.json().get('cuda', {}).get('vram_usage_total', 'N/A')}")
        
        # インターロップAPIを使用してキャッシュをクリア
        execution_url = f"{comfyui_url}/execute"
        clear_payload = {
            "clear_cache": "all"
        }
        response = requests.post(execution_url, json=clear_payload)
        
        # リクエストが成功したか確認
        if response.status_code == 200:
            print("ComfyUIのキャッシュをクリアしました")
        else:
            print(f"キャッシュクリアに失敗しました: {response.status_code} - {response.text}")
            
        # キューをクリア
        queue_url = f"{comfyui_url}/queue"
        response = requests.post(queue_url, json={"clear": True})
        if response.status_code == 200:
            print("ComfyUIのキューをクリアしました")
            
        # 履歴をクリア
        history_url = f"{comfyui_url}/history"
        response = requests.post(history_url, json={"clear": True})
        if response.status_code == 200:
            print("ComfyUIの履歴をクリアしました")
        
        # キャッシュクリア後のVRAM使用状況を確認
        time.sleep(2)  # キャッシュクリアの処理が完了するまで少し待機
        response = requests.get(system_stats_url)
        if response.status_code == 200:
            print(f"クリア後のVRAM使用量: {response.json().get('cuda', {}).get('vram_usage_total', 'N/A')}")
        
        return True
    except Exception as e:
        print(f"ComfyUIのキャッシュクリアに失敗しました: {e}")
        return False

def generate_image_with_comfyui(workflow_data, final_prompt, comfyui_url, seed=None):
    """ComfyUI APIを使用して画像を生成"""
    try:
        # シード値の設定
        if seed is None:
            seed = random.randint(0, 0xFFFFFFFF)  # 32ビットの正の整数
        print(f"使用するシード値: {seed}")
        
        # KSamplerノードのシード値を設定
        for node_id, node in workflow_data.items():
            if 'class_type' in node and node['class_type'] == 'KSampler':
                node['inputs']['seed'] = seed
                break
        
        # テキスト入力ノードを探してプロンプトを設定
        node_id, input_key = find_text_input_node(workflow_data)
        
        if node_id is None:
            print("警告: テキスト入力ノードが見つかりませんでした。CLIPTextEncodeノードの最初のノードにプロンプトを設定します。")
            # テキスト入力が見つからない場合は、最初のCLIPTextEncodeノードを探す
            for node_id, node in workflow_data.items():
                if 'class_type' in node and node['class_type'] == 'CLIPTextEncode':
                    if 'inputs' in node:
                        node['inputs']['text'] = final_prompt
                        break
        else:
            print(f"テキスト入力ノードが見つかりました: node_id={node_id}, input_key={input_key}")
            workflow_data[node_id]['inputs'][input_key] = final_prompt
        
        # ワークフロー実行APIリクエスト
        prompt_url = f"{comfyui_url}/prompt"
        response = requests.post(prompt_url, json={"prompt": workflow_data})
        response.raise_for_status()
        
        prompt_id = response.json()['prompt_id']
        print(f"プロンプトID: {prompt_id}")
        
        # 画像生成の完了を待機
        max_attempts = 30
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            time.sleep(2)  # 少し待機
            
            history_url = f"{comfyui_url}/history"
            history_response = requests.get(history_url)
            
            if history_response.status_code != 200:
                print(f"履歴取得エラー: {history_response.status_code}")
                continue
                
            history = history_response.json()
            
            if prompt_id in history:
                if 'outputs' in history[prompt_id]:
                    outputs = history[prompt_id]['outputs']
                    for node_id, node_output in outputs.items():
                        if 'images' in node_output and node_output['images']:
                            image_data = node_output['images'][0]
                            image_name = image_data['filename']
                            return image_name
            
            print(f"画像生成中... (試行 {attempts}/{max_attempts})")
        
        raise Exception("タイムアウト: 画像生成が完了しませんでした")
    except Exception as e:
        raise Exception(f"画像生成に失敗しました: {e}")

def save_image(image_name, output_path, comfyui_url, webp_quality=80):
    """ComfyUIから画像を取得してwebp形式で保存（非可逆圧縮）"""
    try:
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 画像をダウンロード
        image_url = f"{comfyui_url}/view?filename={image_name}"
        response = requests.get(image_url)
        response.raise_for_status()
        
        # PILで画像を開く
        image = Image.open(BytesIO(response.content))
        
        # WebP形式で保存（非可逆圧縮）
        # quality: 0-100の範囲で指定（低いほど圧縮率が高く、画質は低下）
        # lossless: Falseで非可逆圧縮を指定
        # method: 0-6の範囲で圧縮方法を指定（6が最も圧縮率が高いが、処理時間も長い）
        image.save(
            output_path,
            'WEBP',
            quality=webp_quality,
            lossless=False,
            method=4
        )
        
        # 圧縮率の情報を表示
        original_size = len(response.content)
        compressed_size = os.path.getsize(output_path)
        compression_ratio = (1 - compressed_size / original_size) * 100
        print(f"圧縮率: {compression_ratio:.1f}%（{original_size:,} → {compressed_size:,} bytes）")
        
        return output_path
    except Exception as e:
        raise Exception(f"画像の保存に失敗しました: {e}")

def main():
    try:
        # 引数のパース
        args = parse_arguments()
        
        # プロンプトの読み込み
        generated_prompt = read_prompt(args.prompt_file)
        print(f"読み込んだプロンプト: {generated_prompt}")
        
        # 最終プロンプト作成
        final_prompt = create_final_prompt(args.fixed_prompt, generated_prompt)
        print(f"最終プロンプト: {final_prompt}")
        
        # ワークフローの読み込み
        workflow_data = read_workflow(args.workflow)
        
        # キャッシュクリアが指定されている場合は実行
        if args.clear_cache:
            clear_comfyui_cache(args.comfyui_url)
        
        # 画像生成
        image_name = generate_image_with_comfyui(workflow_data, final_prompt, args.comfyui_url, args.seed)
        
        # 画像の保存
        output_path = save_image(image_name, args.output, args.comfyui_url, args.webp_quality)
        print(f"画像を保存しました: {output_path}")
        
        # 生成後のキャッシュクリア
        if args.clear_cache:
            clear_comfyui_cache(args.comfyui_url)
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1)

if __name__ == "__main__":
    main() 