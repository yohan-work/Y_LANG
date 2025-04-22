#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YohanLanguage (요한랭) 인터프리터
간단한 스택 기반 프로그래밍 언어
"""

import sys
import re

class YohanInterpreter:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.code_blocks = {}
        self.current_line = 0
        
    def push(self, value):
        """스택에 값을 푸시합니다."""
        self.stack.append(value)
        
    def pop(self):
        """스택에서 값을 팝합니다."""
        if not self.stack:
            raise Exception("스택이 비어있습니다!")
        return self.stack.pop()
    
    def interpret(self, code):
        """코드를 해석하고 실행합니다."""
        lines = code.strip().split('\n')
        self.current_line = 0
        
        while self.current_line < len(lines):
            line = lines[self.current_line].strip()
            self.current_line += 1
            
            if not line or line.startswith('#'):
                continue  # 주석이나 빈 줄 무시
                
            self.execute_command(line)
    
    def execute_command(self, command):
        """명령어를 실행합니다."""
        # 요한아 숫자 또는 문자열
        if command.startswith('요한아 ') and command != '요한아 출력해' and not any(command.startswith(prefix) for prefix in ['요한아 더해', '요한아 빼', '요한아 곱해', '요한아 나눠', '요한아 저장해', '요한아 불러와', '요한아 같니', '요한아 크니', '요한아 작니', '요한아 조건', '요한아 반복해', '요한아 거꾸로해', '요한아 복사해', '요한아 만약']):
            value = command[4:].strip()
            try:
                # 숫자인지 확인
                if value.isdigit() or (value.startswith('-') and value[1:].isdigit()):
                    self.push(int(value))
                else:
                    self.push(value)  # 문자열로 푸시
            except:
                self.push(value)  # 실패하면 문자열로 푸시
        
        # 요한아 출력해
        elif command == '요한아 출력해':
            value = self.pop()
            print(value)  # 값만 출력
        
        # 요한아 더해
        elif command == '요한아 더해':
            b = self.pop()
            a = self.pop()
            if isinstance(a, int) and isinstance(b, int):
                self.push(a + b)
            else:
                self.push(str(a) + str(b))
        
        # 요한아 빼
        elif command == '요한아 빼':
            b = self.pop()
            a = self.pop()
            if isinstance(a, int) and isinstance(b, int):
                self.push(a - b)
            else:
                raise Exception("숫자만 뺄 수 있습니다!")
        
        # 요한아 곱해
        elif command == '요한아 곱해':
            b = self.pop()
            a = self.pop()
            if isinstance(a, int) and isinstance(b, int):
                self.push(a * b)
            else:
                raise Exception("숫자만 곱할 수 있습니다!")
        
        # 요한아 나눠
        elif command == '요한아 나눠':
            b = self.pop()
            a = self.pop()
            if b == 0:
                raise Exception("0으로 나눌 수 없습니다!")
            if isinstance(a, int) and isinstance(b, int):
                self.push(a // b)  # 정수 나눗셈
            else:
                raise Exception("숫자만 나눌 수 있습니다!")
        
        # 요한아 저장해 변수명
        elif command.startswith('요한아 저장해 '):
            var_name = command[8:].strip()
            value = self.pop()
            self.variables[var_name] = value
        
        # 요한아 불러와 변수명
        elif command.startswith('요한아 불러와 '):
            var_name = command[8:].strip()
            if var_name not in self.variables:
                raise Exception(f"변수 '{var_name}'이 존재하지 않습니다!")
            self.push(self.variables[var_name])
        
        # 요한아 같니
        elif command == '요한아 같니':
            b = self.pop()
            a = self.pop()
            self.push(1 if a == b else 0)
        
        # 요한아 크니
        elif command == '요한아 크니':
            b = self.pop()
            a = self.pop()
            self.push(1 if a > b else 0)
        
        # 요한아 작니
        elif command == '요한아 작니':
            b = self.pop()
            a = self.pop()
            self.push(1 if a < b else 0)
        
        # 요한아 만약 (조건)
        elif command == '요한아 만약':
            # 조건(1 또는 0), 참일때 실행할 코드, 거짓일때 실행할 코드 순서로 스택에서 팝
            condition = self.pop()
            true_code = self.pop()
            
            if condition:
                lines = true_code.strip().split('\n')
                for line in lines:
                    if line.strip():
                        self.execute_command(line.strip())
        
        # 요한아 반복해 횟수
        elif command.startswith('요한아 반복해 '):
            count_str = command[8:].strip()
            try:
                count = int(count_str)
                code_block = self.pop()
                
                # 코드 블록을 여러 줄로 분리
                lines = code_block.strip().split('\n')
                
                for _ in range(count):
                    for line in lines:
                        if line.strip():
                            self.execute_command(line.strip())
            except ValueError:
                raise Exception(f"반복 횟수는 정수여야 합니다: {count_str}")
        
        # 요한아 복사해
        elif command == '요한아 복사해':
            value = self.stack[-1]  # 마지막 값 복사 (팝하지 않음)
            self.push(value)
        
        # 요한아 거꾸로해
        elif command == '요한아 거꾸로해':
            value = self.pop()
            if isinstance(value, str):
                self.push(value[::-1])
            else:
                raise Exception("문자열만 거꾸로 할 수 있습니다!")
        
        else:
            raise Exception(f"알 수 없는 명령어: {command}")

def main():
    print("요한랭 인터프리터 실행 중...")
    if len(sys.argv) < 2:
        print("사용법: python ylang.py 파일명.yl")
        sys.exit(1)
        
    filename = sys.argv[1]
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        print(f"파일을 읽는 중 오류 발생: {e}")
        sys.exit(1)
    
    interpreter = YohanInterpreter()
    try:
        interpreter.interpret(code)
        print("실행 완료!")
    except Exception as e:
        print(f"실행 오류: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 