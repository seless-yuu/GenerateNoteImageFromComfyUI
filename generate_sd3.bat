@echo off
chcp 65001

rem プロンプトから画像を生成するテスト
python .\generate_image.py ^
    --prompt-file prompt.json ^
    --fixed-prompt "masterpiece, best quality, amazing quality, very aesthetic, high resolution, absurdres, scenery, (anime style, faily style, pencil painting:1.3), beautiful adult 1girl, silver hair, silky hair, medium hair, bob cut, blue eyes, medium breasts, BREAK, Introducing, {content}" ^
    --workflow comfyui_workflow_sd3.json ^
    --output hero_origin.webp ^
    --clear-cache ^
    --webp-quality 80

rem 生成した画像をリサイズ
python .\resize_image.py ^
    --input hero_origin.webp ^
    --output hero.webp ^
    --width 1280 ^
    --height 670 ^
    --quality 80

echo.
echo テスト完了
pause 