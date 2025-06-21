# agent/key_extractor_agent.py
import pandas as pd
import json
import os

def extract_template(file_path: str, output_path: str = "resource/template.json"):
    """Excel 템플릿 파일에서 컬럼 구조를 추출하여 JSON으로 저장합니다."""
    df = pd.read_excel(file_path)
    keys = df.columns.tolist()
    template = {key: "" for key in keys}
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    return f"템플릿 구조가 추출되어 {output_path}에 저장되었습니다. 컬럼 수: {len(keys)}"

# AutoGen 에이전트용 함수 정의
def template_extractor_function(file_path: str, output_path: str = "resource/template.json"):
    """템플릿 추출 에이전트의 메인 함수"""
    try:
        result = extract_template(file_path, output_path)
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 시스템 메시지
TEMPLATE_EXTRACTOR_SYSTEM_MESSAGE = """당신은 문서 구조 분석 전문가입니다.
Excel 템플릿 파일에서 필수 항목들과 구조를 추출하는 역할을 담당합니다.
- 템플릿의 컬럼 구조를 분석합니다
- 필수 입력 항목들을 식별합니다
- 템플릿 구조를 JSON 형태로 저장합니다
- 다른 에이전트들이 참조할 수 있도록 구조화된 정보를 제공합니다"""

