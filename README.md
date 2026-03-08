# 文档审核助手

一个智能教学文档审核工具，AI会理解教学文档的观点，然后对审核文档进行评价和建议。

## 功能

- 📖 **教学文档理解**: 上传教学文档，AI会提取核心观点和理念
- 🔍 **智能审核**: 基于已学习的教学知识，对新文档进行审核评价
- 📁 **多格式支持**: 支持 PDF、Word、文本、Markdown
- 💾 **临时会话**: 本次会话中自动记住教学文档知识

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 获取API Key

1. 访问 [智谱AI开放平台](https://open.bigmodel.cn/)
2. 注册账号并获取 API Key

### 3. 启动后端

```bash
cd backend
python main.py
```

### 4. 启动前端

直接用浏览器打开 `frontend/index.html`，或者使用静态服务器：

```bash
npx serve frontend
```

## 使用流程

1. 输入你的智谱AI API Key
2. 点击「提交教学文档」标签，上传或粘贴教学文档
3. 点击「理解文档」，AI会分析并显示文档要点
4. 点击「审核文档」标签，上传待审核的文档
5. 点击「审核文档」，AI会基于已学习的知识进行评价

## 技术栈

- 后端: FastAPI + Python
- 前端: 原生 HTML/CSS/JS
- AI: 智谱GLM-4 API
- 文档解析: PyPDF2, python-docx
