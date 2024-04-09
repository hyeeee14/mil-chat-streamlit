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


st.header("Chatbot🤖", divider='rainbow')

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets[os.getenv("OPENAI_API_KEY")],
                organization=os.getenv("OPENAI_ORGANIZATION"))

# Set a default model
if "openai_model" not in st.session_state:
    
    st.session_state["openai_model"] = "gpt-4-1106-preview"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if user_input := st.chat_input("Say something😊"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user", avatar="🤔"):
        st.markdown(user_input)


    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})