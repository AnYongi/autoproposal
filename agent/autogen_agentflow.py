# agent/autogen_agentflow.py
from autogen import UserProxyAgent, AssistantAgent, GroupChat, GroupChatManager
from agent.filereader_agent import save_uploaded_files, file_reader_function, FILE_READER_SYSTEM_MESSAGE
from agent.key_extractor_agent import extract_template, template_extractor_function, TEMPLATE_EXTRACTOR_SYSTEM_MESSAGE
from agent.sample_filler_agent import generate_sample, sample_generator_function, SAMPLE_GENERATOR_SYSTEM_MESSAGE
from agent.tone_analyzer_agent import extract_tone_style, tone_analyzer_function, TONE_ANALYZER_SYSTEM_MESSAGE
from agent.report_writer_agent import fill_template_excel, report_writer_function, REPORT_WRITER_SYSTEM_MESSAGE

RESOURCE_DIR = "resource"
DOC_DIR = f"{RESOURCE_DIR}/Doc"
TEMPLATE_PATH = f"{RESOURCE_DIR}/template.json"
SAMPLE_PATH = f"{RESOURCE_DIR}/sample.json"
PROMPT_PATH = f"{RESOURCE_DIR}/prompt.json"
TEMPLATE_XLSX = f"{RESOURCE_DIR}/template.xlsx"
GENERATED_XLSX = f"{RESOURCE_DIR}/generated_output.xlsx"

def create_agents():
    """AutoGen 에이전트들을 생성하고 설정합니다."""
    
    # User Proxy Agent (사용자 대리)
    user_proxy = UserProxyAgent(
        name="User",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={"work_dir": "workspace"},
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # File Reader Agent
    file_reader = AssistantAgent(
        name="FileReaderAgent",
        system_message=FILE_READER_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # Template Extractor Agent
    template_extractor = AssistantAgent(
        name="KeyExtractorAgent", 
        system_message=TEMPLATE_EXTRACTOR_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # Sample Generator Agent
    sample_generator = AssistantAgent(
        name="SampleFillerAgent",
        system_message=SAMPLE_GENERATOR_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # Tone Analyzer Agent
    tone_analyzer = AssistantAgent(
        name="ToneAnalyzerAgent",
        system_message=TONE_ANALYZER_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # Report Writer Agent
    report_writer = AssistantAgent(
        name="ReportWriterAgent",
        system_message=REPORT_WRITER_SYSTEM_MESSAGE,
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    return user_proxy, file_reader, template_extractor, sample_generator, tone_analyzer, report_writer

def run_autogen_workflow(uploaded_files: list, template_file: str = None):
    """AutoGen 멀티에이전트 워크플로우를 실행합니다."""
    
    # 에이전트 생성
    user_proxy, file_reader, template_extractor, sample_generator, tone_analyzer, report_writer = create_agents()
    
    # Group Chat 설정
    groupchat = GroupChat(
        agents=[user_proxy, file_reader, template_extractor, sample_generator, tone_analyzer, report_writer],
        messages=[],
        max_round=50
    )
    manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": [{"model": "gpt-4"}]})
    
    # Step 1: 파일 저장
    user_proxy.initiate_chat(
        file_reader,
        message=f"다음 파일들을 {DOC_DIR} 디렉토리에 저장해주세요: {uploaded_files}"
    )
    
    # Step 2: 템플릿 구조 추출
    if template_file:
        user_proxy.initiate_chat(
            template_extractor,
            message=f"템플릿 파일 {template_file}에서 구조를 추출하여 {TEMPLATE_PATH}에 저장해주세요."
        )
    
    # Step 3: 샘플 데이터 생성
    user_proxy.initiate_chat(
        sample_generator,
        message=f"기존 문서들({DOC_DIR})에서 샘플 데이터를 추출하여 {SAMPLE_PATH}에 저장해주세요. 템플릿은 {TEMPLATE_PATH}를 참조하세요."
    )
    
    # Step 4: 문체 분석
    user_proxy.initiate_chat(
        tone_analyzer,
        message=f"기존 문서들({DOC_DIR})에서 공통 표현과 문체를 분석하여 {PROMPT_PATH}에 저장해주세요."
    )
    
    # Step 5: 최종 보고서 생성
    user_proxy.initiate_chat(
        report_writer,
        message=f"템플릿 {TEMPLATE_XLSX}에 샘플 데이터 {SAMPLE_PATH}를 적용하여 최종 보고서 {GENERATED_XLSX}를 생성해주세요."
    )
    
    return GENERATED_XLSX

# 기존 함수형 워크플로우 (AutoGen 없이 실행)
def run_functional_workflow(uploaded_files: list):
    """함수형 워크플로우 (AutoGen 없이 직접 함수 호출)"""
    # Step 1: Save uploaded files
    save_uploaded_files(uploaded_files, DOC_DIR)

    # Step 2: Extract template
    extract_template(TEMPLATE_XLSX, TEMPLATE_PATH)

    # Step 3: Generate sample values
    generate_sample(DOC_DIR, TEMPLATE_PATH, SAMPLE_PATH)

    # Step 4: Extract prompt/tone
    extract_tone_style(DOC_DIR, PROMPT_PATH)

    # Step 5: Generate final report
    fill_template_excel(TEMPLATE_XLSX, SAMPLE_PATH, GENERATED_XLSX)

    return GENERATED_XLSX

# Optional: call via agent proxy simulation
if __name__ == "__main__":
    dummy_files = ["resource/Doc/지출품의서_스마트팜정보시스템구축_서버랙마운트구매.xlsx",
                   "resource/Doc/지출품의서_스마트팜정보시스템구축_원격회의용웹캠구매.xlsx"]
    
    # AutoGen 워크플로우 실행 (OpenAI API 키가 필요한 경우)
    # result = run_autogen_workflow(dummy_files)
    
    # 함수형 워크플로우 실행 (API 키 없이도 실행 가능)
    result = run_functional_workflow(dummy_files)
    print("✅ 생성 완료:", result)
