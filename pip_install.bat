@echo off

echo ��ǰ Conda ������py36
CALL conda.bat activate py36
echo.

echo ��ǰ Python �汾��
python --version
echo.

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

pause

echo
