Set-Content -Path README.md -Value @'
# 🎨 AI Image Generator

一个基于PyQt5的AI图片生成器，支持文生图和图生图功能。

---

## 功能特性

- ✅ **文生图**：输入文本描述即可生成精美图片
- ✅ **图生图**：上传图片进行二次创作
- ✅ **多尺寸支持**：支持多种图片尺寸比例
- ✅ **深色/浅色主题**：可切换深色和浅色界面
- ✅ **图片下载**：一键下载生成的原图
- ✅ **批量生成**：支持连续生成多张图片，历史记录保留

## 技术栈

- Python 3.x
- PyQt5
- Requests

## 安装依赖

```bash
pip install pyqt5 requests
```

## 使用方法

1. 运行程序：
```bash
python image_generator.py
```

2. 输入图片描述，点击生成按钮即可生成图片

3. 如需图生图，点击图片图标上传参考图片

4. 生成的图片会自动显示在界面上，可连续生成多张

## 配置说明

点击右上角设置按钮配置：
- API 地址：AI图片生成服务的API地址
- API Key：你的API密钥
- 保存路径：生成图片的默认保存目录

## 注意事项

- 需要有效的API密钥才能使用
- 确保网络连接正常
- 首次使用建议先测试文生图功能

---

# 🎨 AI Image Generator

An AI image generator based on PyQt5, supporting text-to-image and image-to-image features.

---

## Features

- ✅ **Text-to-Image**: Generate beautiful images by entering text descriptions
- ✅ **Image-to-Image**: Upload images for secondary creation
- ✅ **Multiple Sizes**: Support various image aspect ratios
- ✅ **Dark/Light Theme**: Switch between dark and light interface
- ✅ **Image Download**: One-click download of original generated images
- ✅ **Batch Generation**: Support continuous generation of multiple images with history preserved

## Tech Stack

- Python 3.x
- PyQt5
- Requests

## Installation

```bash
pip install pyqt5 requests
```

## Usage

1. Run the program:
```bash
python image_generator.py
```

2. Enter image description and click generate button

3. For image-to-image, click the image icon to upload reference image

4. Generated images will be displayed automatically, you can generate multiple images continuously

## Configuration

Click the settings button to configure:
- API URL: The API address of the AI image generation service
- API Key: Your API key
- Save Path: Default save directory for generated images

## Notes

- A valid API key is required
- Ensure network connection is stable
- Suggest testing text-to-image first
'@
