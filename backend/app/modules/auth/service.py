"""Sign up, sign in, sign out, and session lookup."""

from ...utils.security import hash_password, new_token, verify_password
from .repository import SessionRepository, UserRepository


class AuthService:
    def __init__(self, connection):
        self.users = UserRepository(connection)
        self.sessions = SessionRepository(connection)

    def signup(self, name: str, email: str, password: str):
        name = name.strip()
        email = email.strip().lower()
        if not name:
            raise ValueError("a name, please.")
        if "@" not in email:
            raise ValueError("that email does not look right.")
        if len(password) < 6:
            raise ValueError("use at least 6 characters.")
        if self.users.find_by_email(email) is not None:
            raise ValueError("that email already has an account.")
        user = self.users.create(name[:64], email, hash_password(password))
        token = new_token()
        self.sessions.create(token, user["id"])
        return self.user_dict(user), token

    def login(self, email: str, password: str):
        user = self.users.find_by_email(email.strip().lower())
        if user is None or not verify_password(password, user["password_hash"]):
            raise ValueError("wrong email or password.")
        token = new_token()
        self.sessions.create(token, user["id"])
        return self.user_dict(user), token

    def logout(self, token: str) -> None:
        self.sessions.delete(token)

    def user_for_token(self, token: str):
        row = self.sessions.find_user(token)
        return self.user_dict(row) if row is not None else None

    @staticmethod
    def user_dict(row) -> dict:
        return {
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "created_at": row["created_at"],
        }
