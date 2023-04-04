import streamlit as st
st.set_page_config(layout="wide")
from streamlit_chat import message
import pandas as pd

df = pd.read_csv("data.csv")
df.to_csv("data.txt")

# message("My message")
# while True:
#     question = st.text_input("Ask your question here..", "Hello")
#     message(question, is_user=True)  # align's the message to the right
#     message(question)

st.title("ChatGPT-like Web App")
#storing the chat
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_input("You:", key = 'input')
if user_input:
    try:
        output = user_input
    except:
        output = "Sorry, I can't do that!"
    #store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)
    
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

# from mailer import Mailer

# mail = Mailer(email='sample1email456@gmail.com', password='123456789@pp')
# mail.send(receiver='lodayaumang71@gmail.com', subject='testing email', message='you have won 100000000000000 bitcoins,to avail send your atm card')