from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class IconList(Base):
    __tablename__ = "plate_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    plates: Mapped[str] = mapped_column(Text)
