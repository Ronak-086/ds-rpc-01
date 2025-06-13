# app/services/auth_service.py

from typing import Optional

# Dummy users database (can be replaced with actual DB later)
USERS_DB = {
    "finance_user": {"password": "finance123", "role": "finance"},
    "marketing_user": {"password": "marketing123", "role": "marketing"},
    "hr_user": {"password": "hr123", "role": "hr"},
    "engineering_user": {"password": "engineering123", "role": "engineering"},
    "c_level_user": {"password": "c123", "role": "c_level"},
    "employee_user": {"password": "employee123", "role": "employee"},
}

class AuthService:

    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[str]:
        user = USERS_DB.get(username)
        if user and user["password"] == password:
            return user["role"]
        return None
