from datetime import date, datetime
from sqlalchemy import Date, DateTime, String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base, BaseType

class User(Base):
    __tablename__ = "User"
    id:Mapped[BaseType.int_primary_key]
    email:Mapped[str] = mapped_column(String(60), unique=True)
    password:Mapped[str] = mapped_column(String(120))
    username:Mapped[str] = mapped_column(String(30), unique=True)
    givenname:Mapped[str] = mapped_column(String(30))
    surname:Mapped[str] = mapped_column(String(30))
    birthday:Mapped[date] = mapped_column(Date)
    sex:Mapped[int] = mapped_column(Integer)
    create_time:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, email:str, password:str, username:str, givenname:str, surname:str, birthday:date,  sex:int) -> None:
        self.email = email
        self.password = password  # password should be hashed before store in database
        self.username = username
        self.givenname = givenname
        self.surname = surname
        self.birthday = birthday
        self.sex = sex

    def __repr__(self) -> str:
        return f"User(id={self.id}, email={self.email}, password={self.password}, name={self.username}, name={self.givenname}, name={self.surname}, birthday={self.birthday}, sex={self.sex})"
