import streamlit as st
import asyncio
from hello_ollama3 import chatFunction

st.set_page_config(page_title="여행 전문가 AI", layout="wide")
st.title("✈️ 여행 전문가 AI")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력
if prompt := st.chat_input("어디로 여행 가고 싶으신가요?"):

    # 사용자 메시지 저장
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    # LLM 호출
    with st.chat_message("assistant"):
        with st.spinner("생각 중..."):
            response = asyncio.run(chatFunction(prompt))
            st.markdown(response)

    # 응답 저장
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )