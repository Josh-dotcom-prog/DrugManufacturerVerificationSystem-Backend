from datetime import datetime, timezone, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from app.models.users import User, UserToken, ApprovalStatus
from sqlalchemy.exc import IntegrityError



class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user: User) -> None:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError:
            self.session.rollback()
            raise

    def update_user(self, user: User) -> None:
        try:
            self.session.merge(user)
            self.session.commit()
            self.session.refresh(user)
        except IntegrityError:
            self.session.rollback()
            raise

    def get_user_by_id(self, user_id: int) -> User:
        stmt = select(User).where(User.id == user_id)
        return self.session.execute(stmt).scalars().first()

    def add_user_token(self, user_token: UserToken) -> None:
        try:
            self.session.add(user_token)
            self.session.commit()
            self.session.refresh(user_token)
        except IntegrityError:
            self.session.rollback()
            raise

    def get_user_token(self, refresh_key: str, access_key: str, user_id: int) -> UserToken:
        stmt = (
            select(UserToken)
            .options(joinedload(UserToken.user))
            .where(
                UserToken.refresh_key == refresh_key,
                UserToken.access_key == access_key,
                UserToken.user_id == user_id,
                UserToken.expires_at > datetime.now(timezone.utc)
            )
        )
        return self.session.execute(stmt).scalars().first()

    def update_user_token(self, user_token: UserToken) -> None:
        try:
            user_token.expires_at = datetime.now(timezone.utc)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise


    def get_user_by_email(self, email: str) -> User:
        stmt = select(User).where(User.email == email)
        return self.session.execute(stmt).scalars().first()

    #Funtion that gets a user by mobile number
    def get_user_by_mobile(self, mobile: int) -> User:
        user = self.session.query(User).where(User.phone_number == mobile).first()
        return user

    def get_all_users(self):
        return self.session.query(User).all()

    def get_users_by_approval_status(self, status: ApprovalStatus) -> list[User]:
        return self.session.query(User).filter(User.approval_status == status.value).all()