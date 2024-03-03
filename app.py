import streamlit as st
from initialisation import initialize_session_state
from call_back import answer_call_back

# submit job description
jd = st.text_area("Please enter the job description here (If you don't have one, enter keywords, such as PostgreSQL or Python instead): ")
# auto play audio
# auto_play = st.checkbox("Let AI interviewer speak! (Please don't switch during the interview)")

if jd:
    # initialize session states
    initialize_session_state(jd)
	# feedback requested button 
    feedback = st.button("Get Interview Feedback")

    token_placeholder = st.empty()
    chat_placeholder = st.container()
    answer_placeholder = st.container()

	# if feedback button has been clicked, run the feedback chain and terminate the interview
    if feedback:
        evaluation = st.session_state.feedback.invoke("please give evalution regarding the interview")
        st.markdown(evaluation)
        st.stop()
    else:
        with answer_placeholder:
            answer = st.chat_input("Your answer")
            # run the callback function, generate response, and return a audio widget
            if answer:
                st.session_state['answer'] = answer
                answer_call_back()

        # chat_placeholder is use to display the chat history
        with chat_placeholder:
            for answer in st.session_state.history:
                if answer.origin == 'ai':
                    with st.chat_message("assistant"):
                        st.write(answer.message)
                else:
					# user inputs 
                    with st.chat_message("user"):
                        st.write(answer.message)
