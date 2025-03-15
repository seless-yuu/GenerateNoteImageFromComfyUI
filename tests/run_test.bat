@echo off
chcp 932
echo �e�X�g���s�J�n

REM ollama�v���Z�X�̊m�F
powershell -Command "$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue; if (-not $ollamaProcess) { echo 'ollama���N�����܂�...'; Start-Process ollama -WindowStyle Hidden; Start-Sleep -Seconds 5 }"

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json ^
  --clear-cache ^
  --ollama-model gemma3:4b

echo �e�X�g���s����
pause 