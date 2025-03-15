import argparse
import os
import json
import requests
import time
from pathlib import Path

def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='記事文章から画像を生成するツール')
    parser.add_argument('--article', required=True, help='Markdown形式の記事ファイルパス')
    parser.add_argument('--prompt', required=True, help='固定プロンプト（{content}が生成プロンプトに置換されます）')
    parser.add_argument('--workflow', required=True, help='ComfyUIのワークフローJSONファイルパス')
    parser.add_argument('--comfyui-url', default='http://127.0.0.1:8188', help='ComfyUI APIのURL')
    return parser.parse_args()

def read_article(file_path):
    """Markdown記事ファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"記事ファイルの読み込みに失敗しました: {e}")

def read_workflow(file_path):
    """ComfyUIのワークフローJSONファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        raise Exception(f"ワークフローファイルの読み込みに失敗しました: {e}")

def generate_prompt_from_article(article_text):
    """ollamaを使用して記事から画像生成プロンプトを生成"""
    try:
        import ollama
        
        system_prompt = """
        あなたは記事から画像生成AIのためのプロンプトを作成するエキスパートです。
        記事内容を分析し、最適な画像を生成するための英語プロンプトを作成してください。
        プロンプトは具体的な被写体、シーン、雰囲気、色調などの要素を含めてください。
        ただしプロンプトのみを出力し、説明や追加テキストは含めないでください。
        """
        
        response = ollama.chat(
            model='gemma3:12b',
            messages=[
                {
                    'role': 'system',
                    'content': system_prompt
                },
                {
                    'role': 'user',
                    'content': f"以下の記事内容から画像生成AIのプロンプトを英語で作成してください:\n\n{article_text}"
                }
            ]
        )
        
        return response['message']['content'].strip()
    except Exception as e:
        raise Exception(f"プロンプト生成に失敗しました: {e}")

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

def generate_image_with_comfyui(workflow_data, final_prompt, comfyui_url):
    """ComfyUI APIを使用して画像を生成"""
    try:
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

def save_image(image_name, article_path, comfyui_url):
    """ComfyUIから画像を取得してwebp形式で保存"""
    try:
        # 記事ファイルのディレクトリを取得
        article_dir = os.path.dirname(article_path)
        article_filename = Path(article_path).stem
        output_path = os.path.join(article_dir, f"{article_filename}.webp")
        
        # 画像をダウンロード
        image_url = f"{comfyui_url}/view?filename={image_name}"
        response = requests.get(image_url)
        response.raise_for_status()
        
        # webp形式で保存
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        return output_path
    except Exception as e:
        raise Exception(f"画像の保存に失敗しました: {e}")

def main():
    try:
        # 引数のパース
        args = parse_arguments()
        
        # 記事の読み込み
        article_text = read_article(args.article)
        
        # ワークフローの読み込み
        workflow_data = read_workflow(args.workflow)
        
        # プロンプト生成
        generated_prompt = generate_prompt_from_article(article_text)
        print(f"生成されたプロンプト: {generated_prompt}")
        
        # 最終プロンプト作成
        final_prompt = create_final_prompt(args.prompt, generated_prompt)
        print(f"最終プロンプト: {final_prompt}")
        
        # 画像生成
        image_name = generate_image_with_comfyui(workflow_data, final_prompt, args.comfyui_url)
        
        # 画像保存
        output_path = save_image(image_name, args.article, args.comfyui_url)
        
        print(f"画像が正常に生成されました: {output_path}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1)

if __name__ == "__main__":
    main() 