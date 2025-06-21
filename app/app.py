# app/app.py
import streamlit as st
import os
import json
from agent.filereader_agent import save_uploaded_files
from agent.key_extractor_agent import extract_template
from agent.sample_filler_agent import generate_sample
from agent.tone_analyzer_agent import extract_tone_style
from agent.report_writer_agent import fill_template_excel
from agent.autogen_agentflow import run_functional_workflow, run_autogen_workflow

RESOURCE_DIR = "resource"
DOC_DIR = os.path.join(RESOURCE_DIR, "Doc")
TEMPLATE_PATH = os.path.join(RESOURCE_DIR, "template.json")
SAMPLE_PATH = os.path.join(RESOURCE_DIR, "sample.json")
PROMPT_PATH = os.path.join(RESOURCE_DIR, "prompt.json")

st.set_page_config(page_title="지출품의봇", page_icon="🧾", layout="wide")

st.title("🧾 지출품의봇 | 공공기관용 보고서 자동화 도우미")
st.markdown("---")

# 사이드바 설정
st.sidebar.title("⚙️ 설정")
workflow_mode = st.sidebar.selectbox(
    "워크플로우 모드",
    ["함수형 (빠름)", "AutoGen 멀티에이전트 (고급)"],
    help="함수형: 직접 함수 호출, AutoGen: AI 에이전트들이 협력하여 처리"
)

# Step 1: Upload documents
st.header("📄 1단계: 문서 업로드")

col1, col2 = st.columns(2)

with col1:
    template_file = st.file_uploader("📋 지출품의서 템플릿 파일 (.xlsx)", type="xlsx", help="빈 템플릿 양식 파일을 업로드하세요")

with col2:
    uploaded_docs = st.file_uploader("📁 기존 지출품의서 업로드 (2개 이상)", type="xlsx", accept_multiple_files=True, help="학습할 기존 문서들을 업로드하세요")

# 분석 버튼
if st.button("🔍 1️⃣ 문서 분석 및 템플릿 구조 생성", type="primary"):
    if not uploaded_docs or not template_file:
        st.warning("⚠️ 템플릿 파일과 예시 문서를 모두 업로드해주세요.")
    else:
        with st.spinner("문서를 분석하고 있습니다..."):
            try:
                # 파일 저장
                os.makedirs(DOC_DIR, exist_ok=True)
                os.makedirs(RESOURCE_DIR, exist_ok=True)
                
                # 템플릿 파일 저장
                template_path = os.path.join(RESOURCE_DIR, "template.xlsx")
                with open(template_path, "wb") as f:
                    f.write(template_file.getbuffer())
                
                # 예시 문서들 저장
                uploaded_file_paths = []
                for file in uploaded_docs:
                    file_path = os.path.join(DOC_DIR, file.name)
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    uploaded_file_paths.append(file_path)
                
                # 워크플로우 실행
                if workflow_mode == "함수형 (빠름)":
                    # 직접 함수 호출
                    extract_template(template_path, TEMPLATE_PATH)
                    generate_sample(DOC_DIR, TEMPLATE_PATH, SAMPLE_PATH)
                    extract_tone_style(DOC_DIR, PROMPT_PATH)
                else:
                    # AutoGen 워크플로우
                    run_autogen_workflow(uploaded_file_paths, template_path)
                
                st.success("✅ 분석 완료! 템플릿/샘플/문체 추출 완료")
                
                # 결과 미리보기
                if os.path.exists(TEMPLATE_PATH):
                    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
                        template_data = json.load(f)
                    st.json(template_data)
                
            except Exception as e:
                st.error(f"❌ 분석 중 오류가 발생했습니다: {str(e)}")

# Step 2: Generate report
st.header("📝 2단계: 자동 보고서 생성")

if os.path.exists(SAMPLE_PATH):
    with open(SAMPLE_PATH, 'r', encoding='utf-8') as f:
        sample_data = json.load(f)
    st.json(sample_data)

gen_file_name = st.text_input("저장할 파일명", value="result_지출품의서.xlsx", help="생성될 파일의 이름을 입력하세요")

if st.button("🚀 2️⃣ 자동 보고서 생성", type="primary"):
    if not os.path.exists(TEMPLATE_PATH) or not os.path.exists(SAMPLE_PATH):
        st.warning("⚠️ 먼저 1단계를 완료해주세요.")
    else:
        with st.spinner("보고서를 생성하고 있습니다..."):
            try:
                template_file_path = os.path.join(RESOURCE_DIR, "template.xlsx")
                result_path = os.path.join(RESOURCE_DIR, gen_file_name)
                
                fill_template_excel(template_file_path, SAMPLE_PATH, result_path)
                
                st.success("✅ 보고서 생성 완료!")
                
                # 다운로드 버튼
                with open(result_path, "rb") as f:
                    st.download_button(
                        label="📥 보고서 다운로드",
                        data=f.read(),
                        file_name=gen_file_name,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
            except Exception as e:
                st.error(f"❌ 보고서 생성 중 오류가 발생했습니다: {str(e)}")

# 상태 정보 표시
st.sidebar.markdown("---")
st.sidebar.subheader("📊 현재 상태")

if os.path.exists(TEMPLATE_PATH):
    st.sidebar.success("✅ 템플릿 구조 추출됨")
else:
    st.sidebar.error("❌ 템플릿 구조 없음")

if os.path.exists(SAMPLE_PATH):
    st.sidebar.success("✅ 샘플 데이터 생성됨")
else:
    st.sidebar.error("❌ 샘플 데이터 없음")

if os.path.exists(PROMPT_PATH):
    st.sidebar.success("✅ 문체 분석 완료")
else:
    st.sidebar.error("❌ 문체 분석 없음")

# 파일 목록 표시
if os.path.exists(DOC_DIR):
    files = os.listdir(DOC_DIR)
    if files:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📁 업로드된 파일")
        for file in files:
            st.sidebar.text(f"• {file}")
