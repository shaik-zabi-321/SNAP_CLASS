import streamlit as st
from src.database.config import supabase
import time
from src.database.db import enroll_student_subject


@st.dialog("Enroll in subjects")
def enroll_dialog():

    st.write("Enter the subject code")

    join_code = st.text_input("Subject code", placeholder="eg 101")

    if st.button("Enroll now", type='primary', width='stretch'):
        if join_code:
            res = supabase.table('subjects').select(
                'subject_id', 'name', 'subject_code').eq('subject_code', join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']
                check = supabase.table('subject_students').select(
                    '*').eq('subject_id', subject['subject_id']).eq('student_id', student_id).execute()
                if check.data:
                    st.warning("You are Already Enrolled")
                else:
                    enroll_student_subject(student_id, subject['subject_id'])
                    st.toast("Sucessfully enrolled")
                    time.sleep(2)
                    st.rerun()
            else:
                st.warning("plaese enter the correct code")
