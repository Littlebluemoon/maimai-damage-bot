from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class FrameList(Base):
    __tablename__ = "frame_list"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    frames: Mapped[str] = mapped_column(Text)
