import json
import streamlit as st
from rag_logic import RAG
import os 


if 'chats' not in st.session_state:
    st.session_state.chats = []
else : 
    pass
st.title('Pocket-RAG')
def read_files():
    files = os.listdir('pdf')
    paths = [os.path.join('pdf', i ) for i in files]
    return paths

if os.path.exists('pdf'):
    pass
else :
    os.mkdir('pdf')


# RAG init
# rag = RAG()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Write your question ..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# file picker : 


with st.sidebar:
    search = st.text_input('Search' , placeholder='Search chat')
    st.divider()
    
    with st.container(key='file_picker'):
        
        
        files = st.selectbox('Select file' , options=[i for i in read_files()])
        if st.button('Analyse' ):
            st.session_state.chats.append(files)
            st.toast('start chat' ,icon="🔥")
        st.caption('Chats')

    with st.container(key='chats'):    
        for i in st.session_state.chats:
            st.write(i)



with open('chats/chats.json' ,'w') as file:
    json.dump({'chats' : st.session_state.chats} ,file)
            