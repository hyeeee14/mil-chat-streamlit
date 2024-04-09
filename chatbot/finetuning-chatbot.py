import openai
import streamlit as st
import os
import sys
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
from streamlit_chat import message

load_dotenv()

prompts = """

Your name is '미리 Miri', and you play the role of Chatbot that answers defense-related information like a soldier in his 20s
You have to be very empathetic and kind.
You have to use "존댓말"

When you start the conversation, briefly introduce yourself and ask me questions about your questions.
You have to always answer in Korean and speak in honorifics like a male soldier in his 20s.
A new soldier in the military should operate as a chatbot to solve questions.

From now on, you will be conversing with the user following the steps below.
You MUST follow each step(Step 1 ~ Step 3) even when the user doesn't seem to have any stress!!

Step 1 : For Initial greeting, introduce yourself briefly with your name. Say "안녕하세요. 저는 국방 관련 정보를 제공하는 챗봇입니다! 궁금한 것을 질문해주세요."
Step 2 : If you get a question, please refer to the explanation below and answer it.
Step 3 : Despite the above description, whenever the user says "고마워", just give "<대화가 종료되었습니다.>" and stop the conversation.

Only tasks that HELP learning, such as
1. 국방 관련 용어 뜻 알려주기 - Tell me the meaning of terms related to national defense
2. 군인과의 자연스러운 대화 나누기 - general common-sense conversations with army

"""

# OpenAI API 키 설정
#openai.api_key = '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'
#openai.organization='org-e3djfw9Vuf0b33C9eDUFgPms' #hailab
#openai.organization='org-KHEem5rOas7LTMSWAHxKXtCO' #personal

# ChatGPT에 대한 OpenAI Engine 설정
#model = "ft:gpt-3.5-turbo-1106:personal::8tErwhgv" # finetuning
models = "gpt-4-1106-preview"

conversation_history = []

# Initialize chat history & 챗봇 대화 기록
if "messages" not in st.session_state:
    st.session_state.messages = []
    conversation_history = st.session_state.messages

# Streamlit 앱 제목 설정
st.title("Chatbot🤖")


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# 사용자 입력 받기
user = st.chat_message("user", avatar="🤔")
assistant = st.chat_message("assistant",avatar="🤖")

user_input = st.chat_input("Say something😊")
if user_input:
    #st.write(f"User: {user_input}")
    with user:
        st.write(user_input)
        





# 사용자 입력이 있을 때만 챗봇 응답 생성
if user_input:
    # 사용자 입력과 이전 대화 기록을 결합하여 OpenAI에 전달
    prompt_text = "\n".join(conversation_history + [f"사용자: {user_input}", "챗봇:"])


    # OpenAI에 대화 요청 보내기    
    client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"),
                    organization=os.getenv("OPENAI_ORGANIZATION"),
                    #api_key = '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',
                    #organization='org-e3djfw9Vuf0b33C9eDUFgPms' #hailab,                    
                    )
    response = client.chat.completions.create(
        model=models,
        messages=[
            {"role": "system", "content": prompts},
            {"role": "user", "content": user_input}
        ],
        #prompt=prompt_text,
        temperature=0.7,
        max_tokens=150
    )

    # 챗봇 응답 가져오기
    bot_reply = response.choices[0].message.content

    # 대화 기록에 사용자 입력과 챗봇 응답 추가
    conversation_history.append(f"사용자: {user_input}")
    conversation_history.append(f"챗봇: {bot_reply}")

    # 챗봇 응답 출력
    message = assistant
    message.write(bot_reply)

    #st.text_area("챗봇 응답:", value=bot_reply, height=150)

