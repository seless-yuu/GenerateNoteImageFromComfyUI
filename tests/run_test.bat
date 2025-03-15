@echo off
chcp 932
echo テスト実行開始

REM ollamaプロセスの確認と起動
powershell -Command "$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue; if (-not $ollamaProcess) { echo 'ollamaを起動します...'; Start-Process ollama -WindowStyle Hidden; }"

REM ollamaの起動完了を待機
echo ollamaの起動を確認しています...
:WAIT_OLLAMA
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method 'GET' -TimeoutSec 1; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" > nul 2>&1
if errorlevel 1 (
    echo ollamaの起動を待っています...
    timeout /t 2 /nobreak > nul
    goto WAIT_OLLAMA
)
echo ollamaの起動を確認しました

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json ^
  --clear-cache ^
  --ollama-model gemma3:4b

echo テスト実行完了
pause 