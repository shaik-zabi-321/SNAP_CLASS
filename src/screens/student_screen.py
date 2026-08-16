import numpy as np
import streamlit as st
from src.ui.style_base_layout import (
    style_base_layout,
    style_background_dashboard
)
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from PIL import Image
from src.pipelines.facepipeline import predict_attendance, get_face_embeddings, train_classifier
from src.database.db import get_all_students, create_students, get_student_attendence, get_student_subjects, unenroll_student_subject
from src.pipelines.voice_pipeline import get_voice_embedding
import time
from src.components.enrolldialog import enroll_dialog


def student_dashboard():

    student_data = st.session_state.student_data
    student_id = student_data['student_id']
    st.subheader(f""" welcome,{student_data['name']}""")
    # LEFT COLUMN

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    # LEFT COLUMN
    with c1:
        header_dashboard()

        # RIGHT COLUMN
    with c2:

        # logout
        if st.button("Log out", key="teacher_login_back_btn", shortcut="control+backspace"):
            st.session_state['is_logged_in'] = False
            del st.session_state.student_data
            st.rerun()

        st.space()

    col1, col2 = st.columns(2)
    with col1:
        st.header("Your Enrolled Subjects")
    with col2:
        if st.button("Enroll in subjects"):
            enroll_dialog()
    st.divider()

    with st.spinner("Loading your enrolled subjects"):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)

    stats_map = {}

    for log in logs:
        sid = log['subject_id']
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]['total'] += 1

        if logs.get('is_present'):
            stats_map[sid]['attended'] += 1

    cols = st.columns(2)

    for i, sub_node in enumerate(subjects):
        sub = sub_node['subjects']
        sid = sub['subject_id']
        stats = stats_map.get(sid, {'total': 0, 'attended': 0})

        def unenroll_btn():
            if st.button("unenroll from this subject ", type='tertiary', key=f"unenroll_{sid}"):
                unenroll_student_subject(student_id, sid)
                st.toast("Sucessfully unenrolled")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ("", 'total', stats['total']),
                    ("", 'attended', stats['attended']),
                ],
                footer_callback=unenroll_btn()
            )

    footer_dashboard()


def student_screen():
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return

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
            type='secondary',
            key="teacher_login_back_btn",
            shortcut="control+backspace"
        ):
            st.session_state.login_type = None
            st.rerun()

    st.header('Login using face id ', text_alignment='center')
    st.space()
    st.space()
    show_registration = False
    photo_source = st.camera_input("position your face in the center")
    if photo_source:
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning"):
            detected, all_ids, num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning('face not found')
            elif num_faces > 1:
                st.warning("multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s['student_id'] == student_id), None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f'welcome back {student['name']}')
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info('face not recogized you might be a new student ')

                show_registration = True
        if show_registration:
            with st.container(border=True):
                st.header("register new profile")
                new_name = st.text_input(
                    'enter your name ', placeholder="eg. shaik zabi")

                st.subheader("optional:voice enrollment ")
                st.info("enroll for voice only attendance ")

                audio_data = None
                try:
                    audio_data = st.audio_input(
                        "record a short pharse like iam present, may name is zabi ")
                except Exception as e:
                    st.error('audio data failed')
                if st.button('create account', type='primary'):
                    if new_name:
                        with st.spinner("in progress"):
                            img = np.array(Image.open(photo_source))
                            embeddings = get_face_embeddings(img)
                            if embeddings:
                                face_emb = embeddings[0].tolist()

                                voice_emb = None
                                if audio_data:
                                    voice_emb = get_voice_embedding(
                                        audio_data.read())

                                response_data = create_students(
                                    new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                                if response_data:
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state.student_data = response_data[0]
                                    st.toast(f'profile created hi {new_name}')
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error(
                                    "couldnt capture your facial features for registration")

                    else:
                        st.warning('please enter your name ')

    footer_dashboard()
