from sqlalchemy import Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import Base

class SongData(Base):
    __tablename__ = "songdata"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(Text)
    artist: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(Text)
    version: Mapped[str] = mapped_column(Text)
    jacket: Mapped[str] = mapped_column(Text)
    bas: Mapped[float] = mapped_column(Float)
    adv: Mapped[float] = mapped_column(Float)
    exp: Mapped[float] = mapped_column(Float)
    mas: Mapped[float] = mapped_column(Float)
    rem: Mapped[float] = mapped_column(Float)
    release: Mapped[str] = mapped_column(Text)