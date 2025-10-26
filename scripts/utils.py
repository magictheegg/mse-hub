import os

def get_github_path():
	return os.path.split(os.getcwd())[1] # this gets the current working directory, so it's an easy failcase

def get_picurl(set_data, card, back=False):
	return (
		f'https://{get_github_path()}/sets/{card['set']}-files/img/' +
		(f'{card['position']}' if 'position' in card else f'{card['number']}{'t' if 'token' in card['shape'] else ''}_{card[f'card_name']}') +
		('' if 'double' not in card['shape'] else '_back' if back else '_front') +
		f'.{card['image_type'] if 'image_type' in card else set_data['image_type']}'
	)
