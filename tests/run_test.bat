@echo off
chcp 932
echo テスト実行開始

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json

echo テスト実行完了
pause 