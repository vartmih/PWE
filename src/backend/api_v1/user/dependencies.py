from backend.api_v1.user.views import fastapi_users

current_active_user = fastapi_users.current_user(active=True)
