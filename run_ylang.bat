@echo off
echo 요한랭(YohanLanguage) 실행기

if "%1"=="" (
    echo 사용법: run_ylang.bat 파일명.yl
    exit /b 1
)

python ylang.py %1
echo 실행 완료!
pause 