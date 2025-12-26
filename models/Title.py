from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from utils.database import Base

class Title(Base):
    __tablename__ = "titles"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    rarity: Mapped[str] = mapped_column(Text)
    text: Mapped[str] = mapped_column(Text)
    normText: Mapped[str] = mapped_column(Text)
    songs: Mapped[str] = mapped_column(Text)