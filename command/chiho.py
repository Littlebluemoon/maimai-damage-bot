from discord.ext import commands
from paginator import Paginator


from datasource.Chiho import get_chiho_items_by_id, get_chiho_data_by_family, get_chiho_data_by_name, \
	get_chiho_data_by_family_and_order, generate_chiho_item_embed


@commands.command()
async def chiho(ctx, mode, query, order=None):
	if mode == 'help' or not query:
		# TODO: Help command here
		pass
	elif mode == 'item':
		# Try to find chiho by name
		if not order:
			chiho_data = get_chiho_data_by_name(query)
			if not chiho_data:
				family = get_chiho_data_by_family(query)
				if family:
					chiho_data = family[-1]
		else:
			chiho_data = get_chiho_data_by_family_and_order(query, order)
		items = get_chiho_items_by_id(chiho_data.id)
		pages, files = generate_chiho_item_embed(items)
		files = [[i] for i in files]
		await Paginator.Multi().start(ctx, pages=pages, files=files)
