import streamlit as st
from utils.streamlit_utils import get_state


def add_to_history(role, content):
    st.session_state.messages.append({'role': role, 'content': content})


current_state = get_state()
st.set_page_config(
    page_title='Build', page_icon='❀', layout='centered', initial_sidebar_state='auto', menu_items=None
)
st.info('text', icon='ℹ️')

if 'messages' not in st.session_state.keys():
    st.session_state.messages = [
        {'role': 'assistant', 'content': 'start travel'}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

if prompt := st.chat_input('Question'):
    with st.chat_message('user'):
        st.write(prompt)

    with st.chat_message('assistant'):
        with st.spinner('...'):
            response = current_state.llm.chat(prompt)
            st.write(str(response))
            add_to_history('assistant', str(response))
