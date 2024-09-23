from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from auth.database import Base

metadata = MetaData()


# user = Table(
#     "user",
#     metadata,
#     Column("id", Integer, primary_key=True),
#     Column("email", String, nullable=False),
#     Column("username", String, nullable=False),
#     Column("registered_at", TIMESTAMP, default=datetime.utcnow),
#     Column("hashed_password", String, nullable=False),
#     Column("is_active", Boolean, default=True, nullable=False),
#     Column("is_superuser", Boolean, default=False, nullable=False),
#     Column("is_verified", Boolean, default=False, nullable=False),
# )



class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False),
    username = Column(String, nullable=False),
    registered_at = Column(TIMESTAMP, default=datetime.utcnow),
    hashed_password = Column(String, nullable=False),
    is_active = Column(Boolean, default=True, nullable=False),
    is_superuser = Column(Boolean, default=False, nullable=False),
    is_verified = Column(Boolean, default=False, nullable=False)

class Note(Base):
    __tablename__ = "note"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    user_id = Column(Integer, ForeignKey(User.c.id))
    user = relationship("User", back_populates="notes")