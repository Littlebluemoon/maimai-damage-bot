from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class IconList(Base):
    __tablename__ = "icon_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    icons: Mapped[str] = mapped_column(Text)
