@echo off

echo 当前 Conda 环境：py36
CALL conda.bat activate py36
echo.

echo 当前 Python 版本：
python --version
echo.

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

pause

echo
