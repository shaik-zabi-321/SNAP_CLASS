from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(
        pwd.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")


def check_pass(pwd, hased):
    return bcrypt.checkpw(pwd.encode(), hased.encode())


def check_teacher_exist(username):
    # check unique username return flase if name alresdy exist

    response = supabase.table("teachers").select(
        "username").eq("username", username).execute()
    return len(response.data) > 0


def create_techer(username, password, name):
    data = {"username": username,
            "password": hash_pass(password), "name": name}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teachers").select(
        "*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response .data


def create_students(new_name, face_embedding=None, voice_embedding=None):
    data = {'name': new_name, 'face_embedding': face_embedding,
            'voice_embedding': voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subjects(sub_id, name, section, teacher_id):
    data = {
        "subject_id": sub_id,
        "name": name,
        "subject_code": sub_id,
        "section": section,
        "teacher_id": teacher_id
    }
    response = supabase.table('subjects').insert(data).execute()
    return response.data


def get_teacher_subjects(teacher_id):
    response = supabase.table('subjects').select(
        "*,subject_students(count),attendance_logs(timestamp)").eq("teacher_id", teacher_id).execute()

    subjects = response.data

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get(
            'count', 0) if sub.get('subject_students') else 0
        attendence = sub.get('attendance_logs', [])
        unique_session = len(set(log['timestamp'] for log in attendence))
        sub['total_classes'] = unique_session
        sub.pop('subject_students', None)
        sub.pop('attendence_logs', None)
    return subjects


def enroll_student_subject(student_id, subject_id):
    data = {"student_id": student_id, "subject_id": subject_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response


def unenroll_student_subject(student_id, subject_id):
    response = supabase.table('subject_students').delete().eq(
        'subject_id', subject_id).eq('student_id', student_id).execute()
    return response


def get_student_subjects(student_id):
    response = supabase.table('subject_students').select(
        "*,subjects(*)").eq("student_id", student_id).execute()
    return response.data


def get_student_attendence(student_id):
    response = supabase.table('attendance_logs').select(
        "*,subjects(*)").eq("student_id", student_id).execute()
    return response.data


def create_attendence(logs):
    response = supabase.table('attendance_logs').insert(logs).execute()
    return response.data
