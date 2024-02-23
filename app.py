import streamlit as st

def main():
    st.title("VIVI - Revolutionizing Hiring with Virtual Interviews")
    
    # Get user input for their name
    user_name = st.text_input("Enter your name:")
    
    # Display personalized greeting
    if user_name:
        greeting = f"Hello, {user_name}! Welcome to VIVI."
        st.write(greeting)

if __name__ == "__main__":
    main()
