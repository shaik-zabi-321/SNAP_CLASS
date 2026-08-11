from src.components.header import header_home
from src.ui.my_style import local_css
import streamlit as st


def home_screen():
    local_css()
    header_home()

    st.markdown("<p style='color:#8a7862; font-size:15px; margin-bottom:20px;'>Choose your portal to continue</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('🧑‍🏫  Teacher Portal'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    with col2:
        if st.button('🎓  Student Portal'):
            st.session_state['login_type'] = 'student'
            st.rerun()
