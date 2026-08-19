import streamlit as st
from src.database.db import create_subjects
from src.database.db import create_attendence


def show_attendance_results(df, logs):
    st.write("Please review attendence before confirming")
    st.dataframe(df, hide_index=True, width='stretch')
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Discard", width='stretch'):
            st.session_state.voice_attendence_results = None
            st.session_state.attendence_images = []

            st.rerun()
    with col2:
        if st.button('Confirm & Save '):
            try:
                create_attendence(logs)
                st.session_state.attendence_images = []
                st.session_state.voice_attendence_results = None
                st.rerun()
            except Exception as e:
                st.error('sync failed')


@st.dialog("Attendence results")
def add_attendence_logs(df, logs):
    show_attendance_results(df, logs)
