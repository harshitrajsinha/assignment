import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status

from models import login

from sqlmodel import select
from sqlmodel import Session

from services.database import User, get_session

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=login.LoginResponse)
def login(
    payload: login.LoginRequest, session: Session = Depends(get_session)
) -> login.LoginResponse:
    """
    Functionality to authenticate user
    """
    
    result = session.execute(
        select(User).where(User.email == payload.email.lower())
    )
    user = result.scalar_one_or_none()

    # using bcrypt to has payload password and match with password in database
    password_matches = user is not None and bcrypt.checkpw(
        payload.password.encode("utf-8"), user.password_hash.encode("utf-8")
    )

    if user is None or not password_matches or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return login.LoginResponse(authenticated=True)
