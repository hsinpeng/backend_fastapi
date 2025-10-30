from datetime import datetime
from sqlalchemy import DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base, BaseType

class DbItem(Base):
    __tablename__ = "Item"
    id:Mapped[BaseType.int_primary_key]
    title:Mapped[str] = mapped_column(String(30), unique=True)
    content:Mapped[str] = mapped_column(String)
    owner_id:Mapped[int] = mapped_column(Integer, ForeignKey("User.id", ondelete="cascade"))
    # owner:Mapped["DbUser"] = relationship("DbUser", back_populates="items")
    create_time:Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, title:str, content:str, owner_id:int) -> None:
        self.title = title
        self.content = content
        self.owner_id = owner_id

    def __repr__(self) -> str:
        return f"DbItem(id={self.id}, title={self.title}, content={self.content}, owner_id={self.owner_id})"
