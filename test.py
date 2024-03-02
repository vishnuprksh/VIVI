import streamlit as st

# from lib.agents import

from typing import Literal, TypedDict

from streamlit.runtime.uploaded_file_manager import UploadedFile


class UserData(TypedDict):
    fullname: str
    role: str
    experience: int | float
    about: str
    resume: UploadedFile | None



def sidebar():
    # Display Omdena logo
    # st.sidebar.image("images/omdena.png", use_column_width=True)

    # Display location and project information
    st.sidebar.markdown(
        """
        **Project:** Interview Chatbot
        """
    )

    st.sidebar.markdown("---")

    # Display form and input fields in the sidebar
    with st.sidebar.form("user_data_form"):
        st.write("### User Information")

        # Full name
        fullname = st.text_input("Full Name", help="Enter your full name (First & Last name)")

        # Role
        role = st.text_input("Role", help="Enter the role you are applying for (Data Scientist, Data Analyst, etc.)")

        # Years of experience
        experience = st.number_input("Years of Experience", min_value=0, max_value=20, value=0, help="Enter your years of experience")

        # About
        about = st.text_area("About", max_chars=400, help="Tell us about yourself")

        # Resume uploader
        resume = st.file_uploader("Upload Resume", type=["pdf", "docx"], help="Upload your resume here")

        # Submit button
        submit = st.form_submit_button("Submit")

        # Validation
        if submit:
            if not fullname or not role or not experience or not about:
                st.error("Please fill out all the required fields.")
            else:
                st.success("Your data has been submitted successfully")

                # Save user data
                st.session_state.user_data = {"fullname": fullname, "role": role, "experience": experience, "about": about, "resume": resume}

    st.sidebar.markdown("---")

    # Display footer - Copyright info
    st.sidebar.markdown("`©2023 by Binary Bandits. All rights reserved.`", unsafe_allow_html=True)


def chat():
    # Check if user data is available in the session state
    user_data = st.session_state.user_data

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    prompt = st.text_input("Type a message...", key="user_input", disabled=not user_data)

    if not user_data:
        # Display welcome message from assistant if user data is None
        welcome_message = "Hi there! Before we start, please fill out the form so I can better assist you. 📝"

        # Add welcome message to chat history only if it's not already present
        if not st.session_state.messages or st.session_state.messages[-1]["content"] != welcome_message:
            with st.chat_message("assistant"):
                st.markdown(welcome_message)

            st.session_state.messages.append({"role": "assistant", "content": welcome_message})
    elif user_data and prompt:
        # Display user message in chat message container
        st.chat_message("user").markdown(f"**You:** {prompt}")

        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": f"**You:** {prompt}"})

        response = f"HR: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(f"**HR:** {response}")

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": f"**HR:** {response}"})

    # Greet the user and start the interview questions after successful form submission
    if user_data and not st.session_state.greeted:
        # Greet the user with their name and the role they applied for
        greeting_message = (
            f"Hi {user_data['fullname']}! Welcome to the interview for the {user_data['role']} position. 🌟"
        )
        with st.chat_message("assistant"):
            st.markdown(greeting_message)

        # Add greeting message to chat history
        st.session_state.messages.append({"role": "assistant", "content": greeting_message})

        # Start asking interview questions
        interview_start_message = (
            "Let's get started with the interview questions. "
            "I'll ask a series of questions, and you can respond when you're ready. 😊"
        )
        with st.chat_message("assistant"):
            st.markdown(interview_start_message)

        # Add interview start message to chat history
        st.session_state.messages.append({"role": "assistant", "content": interview_start_message})

        # Mark the user as greeted to avoid repeating this section
        st.session_state.greeted = True

def page_config():
    # Set the page config
    st.set_page_config(
        page_title="Chatbot",  # The title of the web page
        page_icon="💬",  # The icon of the web page, can be an emoji or a file path
        initial_sidebar_state="expanded",  # Expanded sidebar
    )

def page_session():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Initialize user data
    if "user_data" not in st.session_state:
        st.session_state.user_data = None

    # Initialize greeting
    if "greeted" not in st.session_state:
        st.session_state.greeted = False

def main():
    # Page session
    page_session()

    # Page config
    page_config()

    # Sidebar
    sidebar()

    # Chat UI
    chat()


if __name__ == "__main__":
    main()




    [{"role": "user", "content": "You are a chatbot designed to ask me questions about my career. Ask me the first question."}]