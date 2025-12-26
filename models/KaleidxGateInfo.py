from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text, Date
from utils.database import Base

class KaleidxGateInfo(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    localizedName: Mapped[str] = mapped_column(Text)
    startDate: Mapped[str] = mapped_column(Date)
    area: Mapped[str] = mapped_column(Text)
    requirements: Mapped[str] = mapped_column(Text)
    track1: Mapped[str] = mapped_column(Text)
    track2: Mapped[str] = mapped_column(Text)
    track3: Mapped[str] = mapped_column(Text)
    track1Abstract: Mapped[str] = mapped_column(Text)
    track2Abstract: Mapped[str] = mapped_column(Text)
    track3Abstract: Mapped[str] = mapped_column(Text)
    colorCode: Mapped[str] = mapped_column(Text)
    image: Mapped[str] = mapped_column(Text)