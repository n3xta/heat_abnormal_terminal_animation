@echo off
REM Heat Abnormal - Terminal Animation Engine
REM Windows启动脚本

echo 🎬 启动Heat Abnormal动画引擎...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未添加到PATH
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
pip show colorama >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 正在安装依赖...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查音频文件
if not exist "assets\heat_abnormal.wav" (
    echo ⚠️  音频文件不存在: assets\heat_abnormal.wav
    echo 请将音频文件放在assets目录中
    pause
    exit /b 1
)

REM 运行程序
echo ✅ 启动动画引擎...
python main.py

pause 