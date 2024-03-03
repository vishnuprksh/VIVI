from langchain.vectorstores.faiss import FAISS
from langchain.text_splitter import SpacyTextSplitter
import streamlit as st
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from templates import templates
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from tags import Message
from langchain.chains import ConversationChain
from langchain.chains import RetrievalQA

def embeddings(text):
	text_splitter = SpacyTextSplitter()
	texts = text_splitter.split_text(text)
	embeddings = OpenAIEmbeddings()
	docsearch = FAISS.from_texts(texts, embeddings)
	retriever = docsearch.as_retriever(search_tupe='similarity search')
	return retriever

def initialize_session_state(jd):
    if "retriever" not in st.session_state:
        st.session_state.retriever = embeddings(jd)

    if "chain_type_kwargs" not in st.session_state:
        Behavioral_Prompt = PromptTemplate(input_variables=["context", "question"],
                                          template=templates.behavioral_template)
        st.session_state.chain_type_kwargs = {"prompt": Behavioral_Prompt}
    # interview history
    if "history" not in st.session_state:
        st.session_state.history = []
        st.session_state.history.append(Message("ai", "Hello there! I am your interviewer today. I will access your soft skills through a series of questions. Let's get started! Please start by saying hello or introducing yourself. Note: The maximum length of your answer is 4097 tokens!"))

    # token count
    if "token_count" not in st.session_state:
        st.session_state.token_count = 0
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationBufferMemory()
    if "guideline" not in st.session_state:
        llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0.8)
        st.session_state.guideline = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type_kwargs=st.session_state.chain_type_kwargs, chain_type='stuff',
            retriever=st.session_state.retriever, memory=st.session_state.memory).invoke(
            "Create an interview guideline and prepare total of 8 questions. Make sure the questions test the soft skills")
  
    if "conversation" not in st.session_state:
        llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.8)
        PROMPT = PromptTemplate(
            input_variables=["history", "input"],
            template=templates.conversation_template)
        st.session_state.conversation = ConversationChain(prompt=PROMPT, llm=llm,
                                                       memory=st.session_state.memory)
        

    if "feedback" not in st.session_state:
        llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",
        temperature = 0.5)
        st.session_state.feedback = ConversationChain(
            prompt=PromptTemplate(input_variables = ["history", "input"], template = templates.conversation_template),
            llm=llm,
            memory = st.session_state.memory
        )