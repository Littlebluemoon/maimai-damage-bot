from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class Chiho(Base):
	__tablename__ = "chiho"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	name: Mapped[str] = mapped_column(Text)
	localized_name: Mapped[str] = mapped_column(Text)
	family: Mapped[str] = mapped_column(Text)
	family_order: Mapped[int] = mapped_column(Integer)
	version: Mapped[str] = mapped_column(Text)
	release_original: Mapped[str] = mapped_column(Text)
	is_available: Mapped[str] = mapped_column(Text)
	available_until: Mapped[str] = mapped_column(Text)
	notes: Mapped[str] = mapped_column(Text)
