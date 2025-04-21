#!/bin/bash

echo "요한랭(YohanLanguage) 실행기"

if [ "$#" -eq 0 ]; then
    echo "사용법: ./run_ylang.sh 파일명.yl"
    exit 1
fi

python3 ylang.py "$1"
echo "실행 완료!" 