from services.user_service import get_user

def get_routes():
    print("Route: /users")
    user = get_user()
    print(f"Loaded user: {user}")
