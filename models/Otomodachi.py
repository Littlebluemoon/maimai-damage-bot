from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class Otomodachi(Base):
    __tablename__ = "otomo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    rank: Mapped[str] = mapped_column(Text)
    boss: Mapped[int] = mapped_column(Integer)
    bossDifficulty: Mapped[int] = mapped_column(Integer)
    playerName: Mapped[str] = mapped_column(Text)
    bossStrength: Mapped[str] = mapped_column(Text)
    scoreRange: Mapped[str] = mapped_column(Text)