@echo off
chcp 932
echo テスト実行開始

REM ollamaプロセスの確認
powershell -Command "$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue; if (-not $ollamaProcess) { echo 'ollamaを起動します...'; Start-Process ollama -WindowStyle Hidden; Start-Sleep -Seconds 5 }"

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json ^
  --clear-cache ^
  --ollama-model gemma3:4b

echo テスト実行完了
pause 