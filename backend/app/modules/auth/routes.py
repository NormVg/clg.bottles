"""Sign up, sign in, sign out, and the current user."""

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from pydantic import BaseModel

from ...utils.db import get_connection
from .service import AuthService

router = APIRouter(prefix="/api/auth")

COOKIE_NAME = "session_token"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30


class SignupInput(BaseModel):
    name: str
    email: str
    password: str


class LoginInput(BaseModel):
    email: str
    password: str


def get_auth_service():
    connection = get_connection()
    try:
        yield AuthService(connection)
    finally:
        connection.close()


def get_current_user(session_token: str | None = Cookie(default=None)):
    """The signed-in user, or 401. Every bookmark route depends on this."""
    if not session_token:
        raise HTTPException(status_code=401, detail="sign in first.")
    connection = get_connection()
    try:
        user = AuthService(connection).user_for_token(session_token)
    finally:
        connection.close()
    if user is None:
        raise HTTPException(status_code=401, detail="sign in first.")
    return user


def set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
    )


@router.post("/signup", status_code=201)
def signup(
    input: SignupInput,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    try:
        user, token = service.signup(input.name, input.email, input.password)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    set_session_cookie(response, token)
    return user


@router.post("/login")
def login(
    input: LoginInput,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    try:
        user, token = service.login(input.email, input.password)
    except ValueError as error:
        raise HTTPException(status_code=401, detail=str(error))
    set_session_cookie(response, token)
    return user


@router.post("/logout", status_code=204)
def logout(
    response: Response,
    session_token: str | None = Cookie(default=None),
    service: AuthService = Depends(get_auth_service),
):
    if session_token:
        service.logout(session_token)
    response.delete_cookie(COOKIE_NAME)


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    return user
