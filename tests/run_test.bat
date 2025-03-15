@echo off
chcp 932
echo �e�X�g���s�J�n

REM ollama�v���Z�X�̊m�F�ƋN��
powershell -Command "$ollamaProcess = Get-Process ollama -ErrorAction SilentlyContinue; if (-not $ollamaProcess) { echo 'ollama���N�����܂�...'; Start-Process ollama -WindowStyle Hidden; }"

REM ollama�̋N��������ҋ@
echo ollama�̋N�����m�F���Ă��܂�...
:WAIT_OLLAMA
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://localhost:11434/api/tags' -Method 'GET' -TimeoutSec 1; if ($response.StatusCode -eq 200) { exit 0 } else { exit 1 } } catch { exit 1 }" > nul 2>&1
if errorlevel 1 (
    echo ollama�̋N����҂��Ă��܂�...
    timeout /t 2 /nobreak > nul
    goto WAIT_OLLAMA
)
echo ollama�̋N�����m�F���܂���

python ../article_to_image.py ^
  --article test_article.md ^
  --prompt "photorealistic, high quality, detailed, {content}" ^
  --workflow comfyui_workflow.json ^
  --clear-cache ^
  --ollama-model gemma3:4b

echo �e�X�g���s����
pause 