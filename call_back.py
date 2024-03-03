# from IPython.display import Audio
from langchain_community.callbacks import get_openai_callback
import streamlit as st
from tags import Message

def answer_call_back():
    with get_openai_callback() as cb:
        # user input
        human_answer = st.session_state.answer
        # transcribe audio
        input = human_answer

        st.session_state.history.append(
            Message("human", input)
        )
        # OpenAI answer and save to history
        llm_answer = st.session_state.conversation.run(input)

        # save audio data to history
        st.session_state.history.append(
            Message("ai", llm_answer)
        )