import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status

from models.login import LoginResponse, LoginRequest

from sqlmodel import select
from sqlmodel import Session

from services.database import get_session
from models.users import User

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, session: Session = Depends(get_session)) -> LoginResponse:

    """
    Functionality to authenticate user
    """
    # get user from database
    result = session.exec(
        select(User).where(User.email == payload.email.lower())
    )
    user = result.one_or_none()

    # using bcrypt to hash payload password and match with password in database
    password_matches = user is not None and bcrypt.checkpw(
        payload.password.encode("utf-8"), user.password_hash.encode("utf-8")
    )

    if user is None or not password_matches or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    response = LoginResponse(authenticated=True)
    return response
