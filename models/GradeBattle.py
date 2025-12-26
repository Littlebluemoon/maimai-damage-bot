from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class GradeBattle(Base):
    __tablename__ = "dan"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(Text)
    lvLower: Mapped[str] = mapped_column(Text)
    lvUpper: Mapped[str] = mapped_column(Text)
    max: Mapped[int] = mapped_column(Integer)
    great: Mapped[int] = mapped_column(Integer)
    good: Mapped[int] = mapped_column(Integer)
    miss: Mapped[int] = mapped_column(Integer)
    clear: Mapped[int] = mapped_column(Integer)
    t1: Mapped[int] = mapped_column(Integer)
    t1_diff: Mapped[int] = mapped_column(Integer)
    t2: Mapped[int] = mapped_column(Integer)
    t2_diff: Mapped[int] = mapped_column(Integer)
    t3: Mapped[int] = mapped_column(Integer)
    t3_diff: Mapped[int] = mapped_column(Integer)
    t4: Mapped[int] = mapped_column(Integer)
    t4_diff: Mapped[int] = mapped_column(Integer)