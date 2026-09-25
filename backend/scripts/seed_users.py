#############################################

# import bcrypt

# password = "my-secret-password"

# hashed_password = bcrypt.hashpw(
#     password.encode("utf-8"),
#     bcrypt.gensalt()
# )

# print(hashed_password)

################################################

# password = "my-secret-password"
# stored_hash = hashed_password

# if bcrypt.checkpw(
#     password.encode("utf-8"),
#     stored_hash
# ):
#     print("Password is correct")
# else:
#     print("Invalid password")

################################################

from sqlmodel import select
from models.users import User, UserRole


def seed_users(session) -> None:
    users = [
        User(
            email="admin@eliciusenergy.com",
            password_hash="$2b$12$e0RSYZbEvELgJ8fyqPWmO./j5pXcgGOsPOOuNmLvZlQKJ3221hOqq",
            is_active=True,
            role=UserRole.ADMIN,
        ),
        User(
            email="harshit@gmail.com",
            password_hash="$2b$12$IrwxzeWAKRsmVlX9KwXWO.8krSpr7sYyBfg3OuPnRpZdDTD8YmDSu",
            is_active=True,
            role=UserRole.ADMIN,
        ),
        User(
            email="newuser@gmail.com",
            password_hash="$2b$12$BQCTtPeng/nI.W8gHOX/6OyX6aCXiNJX9HIYVYM.kHaB.Evp36D.a",
            is_active=True,
            role=UserRole.USER,
        ),
    ]

    # first checking if data exists and only then adding to table, saves from re-seeding in case of server restart due to crash or hot reload (development)
    for user in users:
        existing_user = session.exec(
            select(User).where(User.email == user.email)
        ).first()

        if not existing_user:
            session.add(user)
    session.commit()
