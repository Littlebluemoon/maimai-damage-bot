from sqlalchemy import Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from utils.database import Base

class StatsBase(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    charter: Mapped[str] = mapped_column(Text)
    tap: Mapped[int] = mapped_column(Integer)
    brk: Mapped[int] = mapped_column(Integer)
    xtp: Mapped[int] = mapped_column(Integer)
    bxx: Mapped[int] = mapped_column(Integer)
    hld: Mapped[int] = mapped_column(Integer)
    xho: Mapped[int] = mapped_column(Integer)
    bho: Mapped[int] = mapped_column(Integer)
    bxh: Mapped[int] = mapped_column(Integer)
    str: Mapped[int] = mapped_column(Integer)
    bst: Mapped[int] = mapped_column(Integer)
    xst: Mapped[int] = mapped_column(Integer)
    xbs: Mapped[int] = mapped_column(Integer)
    ttp: Mapped[int] = mapped_column(Integer)
    tho: Mapped[int] = mapped_column(Integer)
    sld: Mapped[int] = mapped_column(Integer)
    bsl: Mapped[int] = mapped_column(Integer)
    num_tap: Mapped[int] = mapped_column(Integer)
    num_hld: Mapped[int] = mapped_column(Integer)
    num_sld: Mapped[int] = mapped_column(Integer)
    num_ttp: Mapped[int] = mapped_column(Integer)
    num_brk: Mapped[int] = mapped_column(Integer)
    num_all: Mapped[int] = mapped_column(Integer)


class Stats00(StatsBase):
    __tablename__ = "stats_00"


class Stats01(StatsBase):
    __tablename__ = "stats_01"


class Stats02(StatsBase):
    __tablename__ = "stats_02"


class Stats03(StatsBase):
    __tablename__ = "stats_03"


class Stats04(StatsBase):
    __tablename__ = "stats_04"