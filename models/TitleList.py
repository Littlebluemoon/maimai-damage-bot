from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class TitleList(Base):
    __tablename__ = "title_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    titles: Mapped[str] = mapped_column(Text)
