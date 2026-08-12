from src.database.config import supabase
import bcrypt


def hash_pass(pwd):
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt().decode())


def check_pass(pwd, hased):
    return bcrypt.checkpw(pwd.encode(), hased.code())


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
        "a").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher
    return None
