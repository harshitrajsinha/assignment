# import os

# import bcrypt
# from sqlmodel import Session, select

# from services.database import User, UserRole, create_tables, engine

# SEED_USERS = (
#     ("admin@eliciusenergy.com", UserRole.ADMIN),
#     ("harshit@gmail.com", UserRole.ADMIN),
#     ("newuser@gmail.com", UserRole.USER),
# )


# def get_seed_password() -> str:
#     password = os.getenv("SEED_USER_PASSWORD")
#     if not password:
#         raise RuntimeError("Set SEED_USER_PASSWORD before running the user seed.")
#     if len(password) < 12:
#         raise RuntimeError("SEED_USER_PASSWORD must contain at least 12 characters.")
#     return password


# def seed_users() -> None:
#     password_hash = bcrypt.hashpw(
#         get_seed_password().encode("utf-8"), bcrypt.gensalt()
#     ).decode("utf-8")

#     create_tables()
#     with Session(engine) as session:
#         for email, role in SEED_USERS:
#             user = session.exec(select(User).where(User.email == email)).first()
#             if user is None:
#                 session.add(
#                     User(email=email, password_hash=password_hash, role=role)
#                 )
#             else:
#                 user.role = role
#                 user.is_active = True
#         session.commit()


# if __name__ == "__main__":
#     seed_users()



from sqlmodel import select
from models.users import User, UserRole


def seed_users(session) -> None:
    users = [
        User(
            email="admin@eliciusenergy.com",
            password_hash="$2b$12$zx7oZdO2jYQmhJK6Gu4FI.h5qeP9MtPicqixNb1gGjVt7Cv.amsZe",
            is_active=True,
            role=UserRole.ADMIN,
        ),
        User(
            email="harshit@gmail.com",
            password_hash="$2b$12$jGfJqfTrkgsxaF.KEyok9OW8GPW1eojoTSzsILnVYkGvfgOC0tDpq",
            is_active=True,
            role=UserRole.ADMIN,
        ),
    ]

    for user in users:
        existing_user = session.exec(
            select(User).where(User.email == user.email)
        ).first()

        if not existing_user:
            session.add(user)
    session.commit()
