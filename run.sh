#!/bin/bash
# Heat Abnormal - Terminal Animation Engine
# Unix/Linux启动脚本

echo "🎬 启动Heat Abnormal动画引擎..."
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python未安装"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

# 使用python3或python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    PYTHON_CMD="python"
    PIP_CMD="pip"
fi

echo "使用Python: $PYTHON_CMD"

# 检查依赖是否安装
if ! $PIP_CMD show colorama &> /dev/null; then
    echo "📦 正在安装依赖..."
    $PIP_CMD install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败"
        exit 1
    fi
fi

# 检查音频文件
if [ ! -f "assets/heat_abnormal.wav" ]; then
    echo "⚠️  音频文件不存在: assets/heat_abnormal.wav"
    echo "请将音频文件放在assets目录中"
    exit 1
fi

# 运行程序
echo "✅ 启动动画引擎..."
$PYTHON_CMD main.py

echo ""
echo "程序已结束" 