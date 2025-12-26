from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class KaleidxKeyConditions(Base):
    __tablename__ = "keyConditions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    conditionShort: Mapped[str] = mapped_column(Text)
    color: Mapped[str] = mapped_column(Text)
    trackList: Mapped[str] = mapped_column(Text)