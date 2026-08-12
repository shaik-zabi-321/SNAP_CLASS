import streamlit as st
from src.ui.style_base_layout import style_base_layout, style_background_dashboard
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exist, create_techer, teacher_login


def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    teacer_screen_login()

    if 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == "login":
        teacer_screen_login()
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacer_screen_login():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    teacher_username = st.text_input(
        "Enter Username", placeholder="shaik zabi")
    st.space()
    teacher_password = st.text_input(
        "Enter password", type='password', placeholder='enter password')
    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            if teacher_login(teacher_username, teacher_password):
                st.toast("welcome back")
                import time
                time.sleep(1)
                st.rerun()
            else:
                print("invalid username or password")

    with btnc2:
        st.button('Register', type='primary',
                  icon=':material/passkey:', width='stretch')
    footer_dashboard()


def register_teacher(teacher_username, teacher_name, teacher_password, teacher_pass_confirm):
    if not teacher_username or not teacher_name or not teacher_password:
        return False, "all feilds are required"
    if check_teacher_exist(teacher_username):
        return False, "user name already exists"
    if teacher_password != teacher_pass_confirm:
        return False, "password dosent match"
    try:
        create_techer(teacher_username, teacher_password, teacher_name)
        return True, "sucessfully created "
    except Exception as e:
        return False, "unexpected error "


def teacher_screen_register():
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", key='loginbackbtn', shortcut="control+backspace"):
            st.session_state['login_type'] = None
            st.rerun()

    st.header('Login using password', text_alignment='center')
    st.space()
    teacher_username = st.text_input(
        "Enter Username", placeholder="shaik zabi")
    st.space()

    teacher_name = st.text_input("Enter name", placeholder="shaik zabi")
    st.space()
    teacher_password = st.text_input(
        "Enter password", type='password', placeholder='enter password')

    confirm_password = st.text_input(
        "Confirm password", type='password', placeholder='enter password')
    st.divider()
    btnc1, btnc2 = st.columns(2)
    with btnc1:
        if st.button('register now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            sucess, message = register_teacher(
                teacher_username, teacher_name, teacher_password, teacher_pass_confirm)
            if sucess:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type = "login"

    with btnc2:
        if st.button('login instead', type='primary', icon=':material/passkey:', width='stretch'):
            st.session_state.teacher_login_type = 'login'

    footer_dashboard()

    st.header('Register your teacher profile')
