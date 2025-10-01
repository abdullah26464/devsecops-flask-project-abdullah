from uuid import uuid4
from bcrypt import hashpw, gensalt
import os
from models import RegistrationCode, User, Note, Session


def setup_db():
    with Session() as session:
        # ✅ Registration codes
        if session.query(RegistrationCode).count() == 0:
            # Use env var for static code, fallback to random
            static_code = os.environ.get("STATIC_REGISTRATION_CODE", str(uuid4()))
            session.add(RegistrationCode(static_code))

            # Add random codes
            for _ in range(10):
                session.add(RegistrationCode(str(uuid4())))
            session.commit()

        # ✅ Users (only if no users exist)
        if session.query(User).count() == 0:
            # Get creds from env vars (never hardcode)
            default_user_email = os.environ.get("DEFAULT_USER_EMAIL", "user@evfa.com")
            default_user_pass = os.environ.get("DEFAULT_USER_PASS", "user")

            default_admin_email = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@evfa.com")
            default_admin_pass = os.environ.get("DEFAULT_ADMIN_PASS", "admin")

            user_pw_hash = hashpw(default_user_pass.encode(), gensalt()).decode("utf-8")
            admin_pw_hash = hashpw(default_admin_pass.encode(), gensalt()).decode("utf-8")

            user = User(default_user_email, user_pw_hash)
            admin = User(default_admin_email, admin_pw_hash, True)

            session.add(user)
            session.add(admin)
            session.commit()

        # ✅ Notes
        if session.query(Note).count() == 0:
            user = session.query(User).filter_by(is_admin=False).first()
            admin = session.query(User).filter_by(is_admin=True).first()

            user_note = Note(
                title="Shared User Note",
                text="A simple note, shared by a normal user",
                private=False,
                user_id=user.id if user else None,
            )
            admin_note = Note(
                title="Private admin note",
                text="A private note, created by an admin user",
                private=True,
                user_id=admin.id if admin else None,
            )
            session.add(user_note)
            session.add(admin_note)
            session.commit()
