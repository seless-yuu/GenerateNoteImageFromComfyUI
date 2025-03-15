import requests
import json
import os
from pathlib import Path

# テスト用の単純なワークフロー
WORKFLOW = {
  "3": {
    "inputs": {
      "seed": 975993290467585,
      "steps": 20,
      "cfg": 5.45,
      "sampler_name": "euler",
      "scheduler": "sgm_uniform",
      "denoise": 1,
      "model": [
        "4",
        0
      ],
      "positive": [
        "16",
        0
      ],
      "negative": [
        "40",
        0
      ],
      "latent_image": [
        "53",
        0
      ]
    },
    "class_type": "KSampler"
  },
  "4": {
    "inputs": {
      "ckpt_name": "emi-2-5.safetensors"
    },
    "class_type": "CheckpointLoaderSimple"
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode"
  },
  "9": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage"
  },
  "16": {
    "inputs": {
      "text": "a beautiful landscape",
      "clip": [
        "42",
        0
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "40": {
    "inputs": {
      "text": "low quality, bad anatomy, bad proportions, blurry, deformed, mutated, ugly, watermark, signature, text, nsfw",
      "clip": [
        "42",
        0
      ]
    },
    "class_type": "CLIPTextEncode"
  },
  "42": {
    "inputs": {
      "clip_name1": "clip_l.safetensors",
      "clip_name2": "clip_g.safetensors",
      "type": "sdxl",
      "device": "default"
    },
    "class_type": "DualCLIPLoader"
  },
  "53": {
    "inputs": {
      "width": 1280,
      "height": 672,
      "batch_size": 1
    },
    "class_type": "EmptySD3LatentImage"
  }
}

def test_simple_prompt():
    """単純なプロンプトのテスト"""
    try:
        # APIエンドポイント
        comfyui_url = "http://127.0.0.1:8188"
        
        # プロンプト実行
        prompt_url = f"{comfyui_url}/prompt"
        response = requests.post(prompt_url, json={"prompt": WORKFLOW})
        
        if response.status_code != 200:
            print(f"エラー: {response.status_code} - {response.text}")
            return False
        
        print(f"レスポンス: {response.json()}")
        return True
    except Exception as e:
        print(f"テスト失敗: {e}")
        return False

if __name__ == "__main__":
    test_simple_prompt() 