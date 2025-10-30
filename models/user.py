from datetime import date, datetime
from sqlalchemy import Date, DateTime, String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, BaseType

class DbUser(Base):
    __tablename__ = "User"
    id:Mapped[BaseType.int_primary_key]
    email:Mapped[str] = mapped_column(String(60), unique=True)
    password:Mapped[str] = mapped_column(String(120))
    username:Mapped[str] = mapped_column(String(30), unique=True)
    givenname:Mapped[str] = mapped_column(String(30))
    surname:Mapped[str] = mapped_column(String(30))
    birthday:Mapped[date] = mapped_column(Date)
    gender:Mapped[int] = mapped_column(Integer)
    active:Mapped[bool] = mapped_column(Boolean)
    # items:Mapped[list["DbItem"]] = relationship("DbItem", back_populates="owner", lazy="noload", cascade="all, delete-orphan")
    create_time:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, email:str, password:str, username:str, givenname:str, surname:str, birthday:date, gender:int, active:bool) -> None:
        self.email = email
        self.password = password  # password should be hashed before store in database
        self.username = username
        self.givenname = givenname
        self.surname = surname
        self.birthday = birthday
        self.gender = gender
        self.active = active


    def __repr__(self) -> str:
        return f"DbUser(id={self.id}, email={self.email}, password={self.password}, name={self.username}, name={self.givenname}, name={self.surname}, birthday={self.birthday}, gender={self.gender}, active={self.active})"
