@echo off
echo 正在启动工具集合网站...
echo 请稍候，这可能需要几秒钟...

REM 设置Python环境变量
set PYTHONPATH=%~dp0

REM 启动Flask应用
python %~dp0build_exe.py

echo 如果浏览器没有自动打开，请手动访问: http://localhost:5000
pause
