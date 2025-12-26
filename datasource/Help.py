from discord import Embed

from exceptions.HelpCommandException import CommandNotFoundException
from models.Help import Help
from utils.database import SessionLocal

session = SessionLocal()

def get_help_embed(command):
	cmd_obj = session.query(Help).filter(Help.command == command.lower()).one()
	if cmd_obj is None:
		raise CommandNotFoundException(f"This command is unavailable: **{command.lower()}**")
	return Embed(title=cmd_obj.command, description=cmd_obj.desc)