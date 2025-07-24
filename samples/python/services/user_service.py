from utils.formatter import format_user

def get_user():
    user = {"name": "Alice", "role": "admin"}
    return format_user(user)
