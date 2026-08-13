import streamlit as st

from src.ui.style_base_layout import (
    style_base_layout,
    style_background_dashboard
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.database.db import (
    check_teacher_exist,
    create_techer,
    teacher_login
)


# =========================================================
# TEACHER SCREEN
# =========================================================

def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    # Decide whether to show Login or Register
    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type == "login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f""" welcome,{teacher_data['name']}""")


def login_teacher(username, password):
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


# =========================================================
# TEACHER LOGIN SCREEN
# =========================================================

def teacher_screen_login():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # LEFT COLUMN
    with c1:
        header_dashboard()

    # RIGHT COLUMN
    with c2:

        # GO BACK TO HOME
        if st.button(
            "Go back to Home",
            key="teacher_login_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

        st.header(
            "Login using password",
            text_alignment="center"
        )

        st.space()

        # USERNAME
        teacher_username = st.text_input(
            "Enter Username",
            placeholder="shaik zabi"
        )

        st.space()

        # PASSWORD
        teacher_password = st.text_input(
            "Enter password",
            type="password",
            placeholder="enter password"
        )

        st.divider()

        # LOGIN AND REGISTER BUTTONS
        btnc1, btnc2 = st.columns(
            [1, 1],
            gap="small"
        )

        with btnc1:
            login_clicked = st.button(
                "Login",
                icon=":material/passkey:",
                width="stretch"
            )

        with btnc2:
            register_clicked = st.button(
                "Register",
                type="primary",
                icon=":material/person_add:",
                width="stretch"
            )

        # LOGIN ACTION
        if login_clicked:

            if login_teacher(teacher_username, teacher_password):

                st.toast("Welcome back!")

                import time
                time.sleep(1)

                st.rerun()

            else:
                st.error("Invalid username or password")

        # REGISTER ACTION
        if register_clicked:
            st.session_state.teacher_login_type = "register"
            st.rerun()

    footer_dashboard()


# =========================================================
# REGISTER TEACHER
# =========================================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_pass_confirm
):

    # Check empty fields
    if (
        not teacher_username
        or not teacher_name
        or not teacher_password
        or not teacher_pass_confirm
    ):
        return False, "All fields are required"

    # Check username
    if check_teacher_exist(teacher_username):
        return False, "Username already exists"

    # Check password confirmation
    if teacher_password != teacher_pass_confirm:
        return False, "Passwords don't match"

    # Create teacher
    try:

        create_techer(
            teacher_username,
            teacher_password,
            teacher_name
        )

        return True, "Successfully created"

    except Exception as e:

        print("Registration error:", e)

        return False, f"Registration error: {e}"


# =========================================================
# TEACHER REGISTER SCREEN
# =========================================================

def teacher_screen_register():

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    # LEFT COLUMN
    with c1:
        header_dashboard()

    # RIGHT COLUMN
    with c2:

        # GO BACK TO HOME
        if st.button(
            "Go back to Home",
            key="teacher_register_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

        st.header(
            "Register your teacher profile",
            text_alignment="center"
        )

        st.space()

        # USERNAME
        teacher_username = st.text_input(
            "Enter Username",
            placeholder="shaik zabi"
        )

        st.space()

        # NAME
        teacher_name = st.text_input(
            "Enter name",
            placeholder="shaik zabi"
        )

        st.space()

        # PASSWORD
        teacher_password = st.text_input(
            "Enter password",
            type="password",
            placeholder="enter password"
        )

        st.space()

        # CONFIRM PASSWORD
        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            placeholder="enter password"
        )

        st.divider()

        # REGISTER AND LOGIN BUTTONS
        btnc1, btnc2 = st.columns(
            [1, 1],
            gap="small"
        )

        with btnc1:
            register_clicked = st.button(
                "Register now",
                icon=":material/person_add:",
                width="stretch"
            )

        with btnc2:
            login_clicked = st.button(
                "Login instead",
                type="primary",
                icon=":material/passkey:",
                width="stretch"
            )

        # REGISTER ACTION
        if register_clicked:

            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_password,
                confirm_password
            )

            if success:

                st.success(message)

                import time
                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

        # LOGIN ACTION
        if login_clicked:
            st.session_state.teacher_login_type = "login"
            st.rerun()

    footer_dashboard()
