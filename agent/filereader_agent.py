# agent/filereader_agent.py
import shutil
import os
from typing import List

def save_uploaded_files(uploaded_files: List[str], target_dir: str = "resource/Doc"):
    """업로드된 파일들을 지정된 디렉토리에 저장합니다."""
    os.makedirs(target_dir, exist_ok=True)
    for file_path in uploaded_files:
        filename = os.path.basename(file_path)
        shutil.copy(file_path, os.path.join(target_dir, filename))
    return f"파일 {len(uploaded_files)}개가 {target_dir}에 저장되었습니다."

# AutoGen 에이전트용 함수 정의
def file_reader_function(uploaded_files: List[str], target_dir: str = "resource/Doc"):
    """파일 리더 에이전트의 메인 함수"""
    try:
        result = save_uploaded_files(uploaded_files, target_dir)
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 시스템 메시지
FILE_READER_SYSTEM_MESSAGE = """당신은 파일 처리 전문가입니다. 
업로드된 문서 파일들을 안전하게 저장하고 관리하는 역할을 담당합니다.
- Excel 파일들의 무결성을 확인합니다
- 파일들을 지정된 디렉토리에 체계적으로 저장합니다
- 저장 결과를 다른 에이전트들에게 보고합니다"""





