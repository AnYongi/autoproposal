# agent/sample_filler_agent.py
import glob
import json
import os
import pandas as pd

def generate_sample(doc_dir: str = "resource/Doc", template_path: str = "resource/template.json", output_path: str = "resource/sample.json"):
    """기존 문서들에서 각 항목별 샘플 값을 추출하여 저장합니다."""
    with open(template_path, "r", encoding="utf-8") as f:
        keys = json.load(f)
    
    filled = {key: [] for key in keys}
    
    for file in glob.glob(os.path.join(doc_dir, "*.xlsx")):
        df = pd.read_excel(file)
        for key in keys:
            if key in df.columns:
                filled[key].extend(df[key].dropna().astype(str).tolist())

    # 예시로 가장 많이 나온 값을 선택
    sample = {key: max(set(values), key=values.count) if values else "" for key, values in filled.items()}
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sample, f, indent=2, ensure_ascii=False)
    
    return f"샘플 데이터가 {output_path}에 저장되었습니다. 항목 수: {len(sample)}"

# AutoGen 에이전트용 함수 정의
def sample_generator_function(doc_dir: str = "resource/Doc", template_path: str = "resource/template.json", output_path: str = "resource/sample.json"):
    """샘플 생성 에이전트의 메인 함수"""
    try:
        result = generate_sample(doc_dir, template_path, output_path)
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 시스템 메시지
SAMPLE_GENERATOR_SYSTEM_MESSAGE = """당신은 데이터 분석 전문가입니다.
기존 문서들에서 각 항목별 대표적인 샘플 값을 추출하는 역할을 담당합니다.
- 기존 문서들의 데이터를 분석합니다
- 각 항목별로 가장 빈번한 값을 찾습니다
- 템플릿에 맞는 샘플 데이터를 생성합니다
- 일관성 있는 데이터 패턴을 제공합니다"""

