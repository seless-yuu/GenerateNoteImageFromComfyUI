# GenerateNoteImageFromComfyUI

Generate images from article text using ComfyUI and ollama.

## Overview

This program generates images from article text through the following steps:

1. Analyze the article using ollama to generate an image prompt
2. Combine the generated prompt with a fixed prompt
3. Generate an image using ComfyUI's API
4. Resize the image to the target size

## Requirements

- Python 3.x
- ComfyUI (running)
- ollama (will be automatically started if not running)

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Commands

The functionality is split into three separate commands:

### 1. Summarize Article

Generates a prompt from an article:

```bash
python summarize_article.py \
  --article <path_to_article.md> \
  --output <path_to_prompt.json>
```

### 2. Generate Image

Generates an image using the prompt:

```bash
python generate_image.py \
  --prompt-file <path_to_prompt.json> \
  --fixed-prompt "your_fixed_prompt {content}" \
  --workflow <path_to_workflow.json> \
  --output <path_to_output.webp> \
  --clear-cache \
  --webp-quality 80
```

### 3. Resize Image

Resizes the generated image while maintaining aspect ratio:

```bash
python resize_image.py \
  --input <path_to_input.webp> \
  --output <path_to_output.webp> \
  --width 1280 \
  --height 670 \
  --quality 80
```

## Parameters

### Summarize Article

- `--article`: Path to the Markdown article file
- `--output`: Path to save the generated prompt as JSON

### Generate Image

- `--prompt-file`: Path to the JSON file containing the generated prompt
- `--fixed-prompt`: Fixed prompt template. Use `{content}` where you want to insert the generated prompt
- `--workflow`: Path to ComfyUI workflow JSON file
- `--output`: Path to save the generated image
- `--clear-cache`: (Optional) Clear ComfyUI cache before generation
- `--webp-quality`: (Optional) WebP compression quality (0-100, default: 80)

### Resize Image

- `--input`: Path to the input image
- `--output`: Path to save the resized image
- `--width`: Target width in pixels
- `--height`: Target height in pixels
- `--quality`: (Optional) WebP compression quality (0-100, default: 80)

## Workflows

Two workflow configurations are provided for different models:

### SD2 Workflow

- Initial generation at 1024x576
- Upscale by factor 1.5 using Latent Upscale
- Second pass with denoise 0.6

### SD3 Workflow

- Initial generation at 1024x576
- Upscale by factor 1.3 using Latent Upscale
- Second pass with denoise 0.3

## Output

- Generated images are saved in WebP format with configurable quality
- Images can be automatically resized to target dimensions while maintaining aspect ratio
- Original aspect ratio is preserved during resizing

## Testing

You can test each functionality using the following batch files:

```bash
summarize.bat  # Test article summarization
generate_sd2.bat  # Test image generation with SD2 workflow
generate_sd3.bat  # Test image generation with SD3 workflow
```

Each batch file has the necessary parameters pre-configured and is ready to run.

## Error Handling

The program will:

- Display warnings if aspect ratios differ during resizing
- Show compression ratios and size changes
- Stop and display error messages if any errors occur during execution

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
