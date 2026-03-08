import streamlit as st
from openai import OpenAI

# Ollama 연결
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

MODEL = "qwen3:8b"

st.set_page_config(page_title="Ollama Chat", layout="wide")
st.title("🦙 Local Ollama Chat")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("메시지를 입력하세요"):
    
    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # LLM 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        response = client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.messages,
            stream=True
        )

        for chunk in response:
            delta = chunk.choices[0].delta.content
            if delta:
                full_response += delta
                message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response}
    )