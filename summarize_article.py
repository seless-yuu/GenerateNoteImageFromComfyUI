import argparse
import json
import gc
import datetime

def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='記事文章から画像生成用プロンプトを生成するツール')
    parser.add_argument('--article', required=True, help='Markdown形式の記事ファイルパス')
    parser.add_argument('--output', required=True, help='生成したプロンプトを保存するJSONファイルパス')
    parser.add_argument('--ollama-model', default='gemma3:4b', help='ollamaの使用するモデル名')
    return parser.parse_args()

def read_article(file_path):
    """Markdown記事ファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"記事ファイルの読み込みに失敗しました: {e}")

def generate_prompt_from_article(article_text, model_name):
    """ollamaを使用して記事から画像生成プロンプトを生成"""
    try:
        # 関数スコープでollamaをインポートし、使用後にクリーンアップできるようにする
        import ollama
        
        system_prompt = """
        あなたは記事から画像生成AIのためのプロンプトを作成するエキスパートです。
        記事内容を分析し、最適な画像を生成するための英語プロンプトを作成してください。
        プロンプトは具体的な被写体、シーン、雰囲気、色調などの要素を含めてください。
        ただしプロンプトのみを出力し、説明や追加テキストは含めないでください。
        """
        
        print(f"ollamaモデル '{model_name}' を使用して画像生成プロンプトを作成しています...")
        
        # ollamaの処理をスコープ内に閉じ込める
        def get_ollama_response():
            return ollama.chat(
                model=model_name,
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
        
        # プロンプト生成
        response = get_ollama_response()
        generated_prompt = response['message']['content'].strip()
        
        # モデルを明示的に解放
        if hasattr(ollama, 'terminate') and callable(ollama.terminate):
            ollama.terminate()
        
        # メモリ解放を強制
        del ollama
        gc.collect()
        
        print("ollamaのメモリを解放しました")
        return generated_prompt
    except Exception as e:
        raise Exception(f"プロンプト生成に失敗しました: {e}")

def save_prompt(prompt, output_path):
    """生成したプロンプトをJSONファイルに保存"""
    try:
        data = {
            'generated_prompt': prompt,
            'timestamp': str(datetime.datetime.now())
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise Exception(f"プロンプトの保存に失敗しました: {e}")

def main():
    try:
        # 引数のパース
        args = parse_arguments()
        
        # 記事の読み込み
        article_text = read_article(args.article)
        
        # プロンプト生成 (ollamaを使用)
        generated_prompt = generate_prompt_from_article(article_text, args.ollama_model)
        print(f"生成されたプロンプト: {generated_prompt}")
        
        # プロンプトを保存
        save_prompt(generated_prompt, args.output)
        print(f"プロンプトを保存しました: {args.output}")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        exit(1)

if __name__ == "__main__":
    main() 