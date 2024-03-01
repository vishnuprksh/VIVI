from openai import OpenAI
import streamlit as st
from whisper import WhisperSTT


st.title("VIVI")

# text=WhisperSTT(openai_api_key=st.secrets["OPENAI_API_KEY"],language='en')

# if text:
#     st.write(text)


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages =[]

def get_response():
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "user", "content": "You are a chatbot designed to ask me questions about my career. Ask me the first question."}] + [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

get_response()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
    prompt = st.chat_input("Say something:")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})






