@echo off
chcp 932
echo �e�X�g���s�J�n

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json ^
  --clear-cache ^
  --ollama-model gemma3:4b

echo �e�X�g���s����
pause 