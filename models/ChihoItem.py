from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, Text
from utils.database import Base

class ChihoItem(Base):
	__tablename__ = "chiho_items"
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	chiho_id: Mapped[int] = mapped_column(Integer)
	item_id: Mapped[int] = mapped_column(Integer)
	name: Mapped[str] = mapped_column(Text)
	kind: Mapped[str] = mapped_column(Text)
	attachment_kind: Mapped[str] = mapped_column(Text)
	attachment: Mapped[str] = mapped_column(Text)
	distance: Mapped[int] = mapped_column(Integer)

