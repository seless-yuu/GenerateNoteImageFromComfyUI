import requests
import json
import time

def test_comfyui_api():
    """ComfyUI APIの接続テスト"""
    try:
        # APIエンドポイント
        comfyui_url = "http://127.0.0.1:8188"
        
        # オブジェクトリスト取得
        objects_url = f"{comfyui_url}/object_info"
        response = requests.get(objects_url)
        response.raise_for_status()
        
        # レスポンスを表示
        print("=== 利用可能なオブジェクトタイプ ===")
        objects_info = response.json()
        for obj_type in objects_info.keys():
            print(f"- {obj_type}")
        
        # 履歴取得
        history_url = f"{comfyui_url}/history"
        response = requests.get(history_url)
        response.raise_for_status()
        
        # 履歴情報を表示
        print("\n=== 履歴情報 ===")
        history = response.json()
        for prompt_id, data in history.items():
            print(f"プロンプトID: {prompt_id}")
            if len(data.get('prompt', {})) > 0:
                print(f"  ノード数: {len(data['prompt'].get('nodes', {}))} 個")
            
            # 最後の成功したワークフローを取得
            if 'outputs' in data:
                print("  出力あり")
                with open('last_successful_workflow.json', 'w') as f:
                    json.dump(data['prompt'], f, indent=2)
                print("  成功したワークフローを 'last_successful_workflow.json' に保存しました")
                break
        
        print("\nComfyUI APIテスト完了")
        return True
    except Exception as e:
        print(f"ComfyUI APIテスト失敗: {e}")
        return False

if __name__ == "__main__":
    test_comfyui_api() 