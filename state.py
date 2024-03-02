import streamlit as st

st.write("hi")

if prompt := st.chat_input("Write something: "):
    st.write(prompt)
