import streamlit as st
from src.components.header import header_home
from src.components.footer import footer_home
from src.ui.style_base_layout import style_base_layout, style_background_home


def home_screen():

    header_home()
    style_background_home()
    style_base_layout()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.header("I'm a student")
        # placeholder until a restyled student mascot is ready
        st.markdown(
            "<p style='font-size:80px; text-align:left; margin:0 0 10px;'>🎓</p>",
            unsafe_allow_html=True
        )
        if st.button('Scan me in', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'student'
            st.rerun()

    with col2:
        st.header("I'm a teacher")
        # placeholder until a restyled teacher mascot is ready
        st.markdown(
            "<p style='font-size:80px; text-align:left; margin:0 0 10px;'>🧑‍🏫</p>",
            unsafe_allow_html=True
        )
        if st.button('Take attendance', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'teacher'
            st.rerun()

    footer_home()
