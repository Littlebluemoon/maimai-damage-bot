from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, Integer
from utils.database import Base

class Help(Base):
	__tablename__ = "help"
	command: Mapped[str] = mapped_column(Text, primary_key=True)
	desc: Mapped[str] = mapped_column(Text)