import streamlit as st
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader

#---------------------AUTHENTICATION--

if 'authentication_status' not in st.session_state:
    st.session_state['key'] = None
if 'obj' not in st.session_state:
    st.session_state['obj'] = None

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout("logout", "sidebar")
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


# if st.session_state["authentication_status"]:
#     try:
#         if authenticator.reset_password(st.session_state["username"]):
#             st.success('Password modified successfully')
#     except Exception as e:
#         st.error(e)


# try:
#     email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
#     if email_of_registered_user:
#         st.success('User registered successfully')
# except Exception as e:
#     st.error(e)

#-----------------WELCOME PAGE
# if st.session_state["authentication_status"] and st.session_state["obj"] == "candidate":
#     st.write(f'Welcome to Session candidate')
# elif st.session_state["authentication_status"] and st.session_state["obj"] == "company":
#     st.write(f'Welcome to Session company')
