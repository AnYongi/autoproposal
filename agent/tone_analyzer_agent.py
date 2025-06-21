# agent/tone_analyzer_agent.py
from collections import Counter
import re
import glob
import os
import pandas as pd
import json

def extract_tone_style(doc_dir: str = "resource/Doc", output_path: str = "resource/prompt.json"):
    """기존 문서들에서 공통적인 표현과 문체를 추출합니다."""
    expressions = []
    for file in glob.glob(os.path.join(doc_dir, "*.xlsx")):
        df = pd.read_excel(file)
        for col in df.columns:
            text_values = df[col].dropna().astype(str).tolist()
            for val in text_values:
                # 명사구, 빈번한 표현 단위 추출 예시
                phrases = re.findall(r"[가-힣]{2,10}", val)
                expressions.extend(phrases)

    counter = Counter(expressions)
    prompt_data = {"common_expressions": counter.most_common(20)}
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(prompt_data, f, indent=2, ensure_ascii=False)
    
    return f"문체 분석 결과가 {output_path}에 저장되었습니다. 추출된 표현 수: {len(counter)}"

# AutoGen 에이전트용 함수 정의
def tone_analyzer_function(doc_dir: str = "resource/Doc", output_path: str = "resource/prompt.json"):
    """문체 분석 에이전트의 메인 함수"""
    try:
        result = extract_tone_style(doc_dir, output_path)
        return {"status": "success", "message": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 시스템 메시지
TONE_ANALYZER_SYSTEM_MESSAGE = """당신은 언어학 및 문체 분석 전문가입니다.
기존 문서들에서 조직의 특유한 표현과 문체를 분석하는 역할을 담당합니다.
- 공공기관 문서의 특유한 표현을 추출합니다
- 빈번하게 사용되는 용어들을 분석합니다
- 조직의 일관된 문체 패턴을 식별합니다
- 새로운 문서 작성 시 참조할 수 있는 표현 사전을 제공합니다"""

