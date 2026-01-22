from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer
from utils.database import Base

class Plate(Base):
	__tablename__ = "plates"
	id: Mapped[str] = mapped_column(Text, primary_key=True)
	name: Mapped[str] = mapped_column(Text)
	norm_text: Mapped[str] = mapped_column(Text)
	songs: Mapped[str] = mapped_column(Text)