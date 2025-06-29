# 지출품의봇 (Expense Proposal Bot)

본 프로젝트는 Microsoft AutoGen 기반 멀티에이전트 시스템을 활용하여 공공 프로젝트 문서 중 하나인 **지출품의서**를 자동으로 작성해주는 Streamlit 기반 도구입니다. 특히 공공기관의 문체/표현 방식에 맞춰 문서를 생성하여 사용자 부담을 줄이는 것을 목표로 합니다.

---

## 🧩 프로젝트 개요

- **목적**: 지출품의서 작성 자동화 (템플릿 + 기존 문서 학습)
- **사용 기술**: MS AutoGen (multi-agent), Streamlit, Python
- **기능 요약**:
  1. 문서 템플릿 및 예시 업로드
  2. 템플릿 구조 및 필수 항목 학습
  3. 조직 맞춤 어투/표현 추출
  4. 자동 보고서 생성 및 다운로드 제공

---

## 🚀 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. Streamlit 앱 실행
```bash
streamlit run app/app.py
```

### 3. 브라우저에서 접속
```
http://localhost:8501
```

---

## 📁 현재 업로드된 파일 목록

| 파일명 | 설명 |
|--------|------|
| 지출품의서_스마트팜정보시스템구축_template.xlsx | 지출품의서 템플릿 파일 (양식 기반) |
| 지출품의서_스마트팜정보시스템구축_생육조사용품_저울장갑외구매.xlsx | 지출 예시: 생육조사용품(저울, 장갑 외) 구매 |
| 지출품의서_스마트팜정보시스템구축_서버랙마운트구매.xlsx | 지출 예시: 서버랙 마운트 구매 |
| 지출품의서_스마트팜정보시스템구축_원격회의용웹캠구매.xlsx | 지출 예시: 원격 회의용 웹캠 구매 |

---

## 🔧 구현된 기능

### ✅ 완료된 기능
1. **파일 업로드 및 관리**: Streamlit을 통한 직관적인 파일 업로드
2. **템플릿 구조 추출**: Excel 템플릿에서 컬럼 구조 자동 분석
3. **샘플 데이터 생성**: 기존 문서들에서 대표값 추출
4. **문체 분석**: 공공기관 특유의 표현 패턴 분석
5. **자동 보고서 생성**: 템플릿 + 샘플 데이터 조합으로 최종 문서 생성
6. **다운로드 기능**: 생성된 보고서 Excel 파일 다운로드

### 🤖 AutoGen 멀티에이전트 시스템
- **FileReaderAgent**: 파일 업로드 및 관리
- **KeyExtractorAgent**: 템플릿 구조 분석
- **SampleFillerAgent**: 샘플 데이터 생성
- **ToneAnalyzerAgent**: 문체 및 표현 분석
- **ReportWriterAgent**: 최종 보고서 작성

### 📊 워크플로우 모드
1. **함수형 (빠름)**: 직접 함수 호출로 빠른 처리
2. **AutoGen 멀티에이전트 (고급)**: AI 에이전트들이 협력하여 처리

---

## 📂 폴더 구조

```
project_root/
│
├── resource/
│   ├── Doc/                   # 업로드된 원본 문서
│   ├── template.json          # 문서 항목 구조
│   ├── sample.json            # 항목별 값 예시
│   ├── prompt.json            # 어투/문체 추출 결과
│   └── generated_output.xlsx  # 생성된 최종 보고서
│
├── app/
│   └── app.py                 # Streamlit 프론트엔드
│
├── agent/                     # AutoGen 에이전트 구성
│   ├── autogen_agentflow.py   # 메인 워크플로우 관리
│   ├── filereader_agent.py    # 파일 업로드 처리
│   ├── key_extractor_agent.py # 템플릿 구조 추출
│   ├── sample_filler_agent.py # 샘플 데이터 생성
│   ├── tone_analyzer_agent.py # 문체/어투 분석
│   └── report_writer_agent.py # 최종 보고서 생성
│
├── results/                   # 생성된 결과물 저장
├── requirements.txt           # 의존성 패키지 목록
└── README.md
```

---

## 🎯 사용 방법

### 1단계: 문서 업로드
1. 템플릿 파일 업로드 (빈 양식)
2. 기존 지출품의서 예시들 업로드 (2개 이상)
3. "문서 분석 및 템플릿 구조 생성" 버튼 클릭

### 2단계: 보고서 생성
1. 생성된 샘플 데이터 확인
2. 파일명 입력
3. "자동 보고서 생성" 버튼 클릭
4. 생성된 Excel 파일 다운로드

---

## 🔮 향후 확장 계획

- **다양한 문서 형식 지원**: 주간보고서, 회의록 등
- **AI 기반 내용 생성**: GPT를 활용한 더 정교한 내용 생성
- **템플릿 커스터마이징**: 사용자 정의 템플릿 지원
- **배치 처리**: 여러 문서 동시 생성
- **품질 검증**: 생성된 문서의 품질 자동 검증

---

본 프로토타입은 **지출품의서**에 특화되어 있으며, 향후 주간보고서나 회의록 등으로 확장 가능합니다.
