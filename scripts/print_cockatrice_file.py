import os
import json
import re
from datetime import datetime

def escape_and_format(text: str):
	return text.replace('&', '&amp;') \
				.replace('"', '&quot;') \
				.replace('“', '&quot;') \
				.replace('”', '&quot;') \
				.replace('\'', '&apos;') \
				.replace('’', '&apos;') \
				.replace('<', '&lt;') \
				.replace('>', '&gt;') \

def format_cost(cost):
	if len(cost) == 0: return ''
	symbols = re.split(r'\{([^{}]+)\}', cost)
	cost = ''
	for symbol in symbols:
		if len(symbol) == 0: continue
		if symbol.isdecimal(): 
			cost += symbol
			continue
		cost += '/'.join(symbol)
	return cost

def cost_to_cmc(cost):
	symbols = re.split(r'\{([^{}]+)\}', cost)
	cmc = 0
	for symbol in symbols:
		if len(symbol) == 0 or symbol == "X" or symbol == "Y": continue
		try:
			num = re.match(r'\d+', symbol).group(0)
			cmc += int(num)
		except:
			cmc += 1
	return cmc

def get_maintype(type):
	first_half = type.split('\u2014')[0].strip()
	return first_half.split(' ')[-1].strip()

def get_related(notes, instruction, tag):
	related = []
	for line in notes.split('\n'):
		if not line.startswith(instruction):
			continue

		tokens = line[len(instruction) + 1:].split(';')
		for token in tokens:
			name, num = re.match(r'([^<]+)(?:<([^<]+)>)?', token).groups()
			if not num:
				extra = ''
			elif num.isdecimal() or num == "x" or num == "X":
				extra = f' count="{num}"'
			elif num == "persistent" or num == "conjure":
				extra = ' persistent=""'
			else:
				print(f'Warning: unknown !tokens parameter <{num}>. Ignoring')
				extra = ''
			related.append(f'<{tag}{extra}>{escape_and_format(name)}</{tag}>')

	return related

def get_picurl(github_path, set_data, card, back):
	return (
		f'https://{github_path}/sets/{card['set']}-files/img/'
		f'{card['number']}{'t' if 'token' in card['shape'] else ''}{'' if 'double' not in card['shape'] else '_back' if back else '_front'}_{card[f'card_name{'2' if back else ''}']}'
		f'.{set_data['image_type']}'
	)

def get_number(card, back):
	return f'{card['number']}{'' if 'double' not in card['shape'] else 'b' if back else 'a'}'

def get_tablerow(card_type):
	return (
		2 if 'Creature' in card_type else
		0 if 'Land' in card_type else
		3 if 'Instant' in card_type or 'Sorcery' in card_type else
		1
	)

def render_card(set_data, github_path, card, back=False):
	suffix = '2' if back else ''
	props = f'''
				<layout>{'split' if 'split' in card['shape'] else 'transform' if 'double' in card['shape'] else 'normal'}</layout>
				<side>front</side>
				<type>{escape_and_format(card[f'type{suffix}'].strip())}</type>
				<maintype>{escape_and_format(get_maintype(card[f'type{suffix}']))}</maintype>
				<manacost>{escape_and_format(format_cost(card[f'cost{suffix}']))}</manacost>
				<cmc>{cost_to_cmc(card[f'cost{suffix}'])}</cmc>'''

	if len(card[f'color{suffix}']):
		props += f'''
				<colors>{card[f'color{suffix}']}</colors>'''

	color_identity = card['color_identity'].replace('C', '')
	if len(color_identity):
		props += f'''
				<coloridentity>{color_identity}</coloridentity>'''

	if len(card[f'pt{suffix}']):
		props += f'''
				<pt>{escape_and_format(card[f'pt{suffix}'])}</pt>'''

	if len(card[f'loyalty{suffix}']):
		props += f'''
				<loyalty>{escape_and_format(card[f'loyalty{suffix}'])}</loyalty>'''

	card_type = card[f'type{suffix}']
	card_string = f'''
		<card>
			<name>{escape_and_format(card[f'card_name{suffix}'] + (f' {card['set']}' if 'token' in card['shape'] else ''))}</name>
			<text>{re.sub(r'\[/?i\]', '', escape_and_format(card[f'rules_text{suffix}']))}</text>
			<set rarity="{'rare' if card['rarity'] == 'cube' else card['rarity']}" picurl="{escape_and_format(get_picurl(github_path, set_data, card, back))}" num="{get_number(card, back)}">{escape_and_format(card['set'])}</set>
			<prop>{props}
			</prop>
			<tablerow>{get_tablerow(card_type)}</tablerow>'''

	if 'token' in card['shape']:
		card_string += '''
			<token>1</token>'''

	if 'split' in card['shape']:
		card_string += '''
			<upsidedown>1</upsidedown>'''

	related = get_related(card['notes'], '!tokens', 'related')
	if 'double' in card['shape']:
		related.append(f'<related attach="transform">{escape_and_format(card['card_name' if back else 'card_name2'])}</related>')
	if len(related):
		card_string += f'''
			{'\n			'.join(related)}'''

	reverse_related = get_related(card['notes'], '!related', 'reverse_related')
	if len(reverse_related):
		card_string += f'''
			{'\n			'.join(reverse_related)}'''

	if '!tapped' in card['notes']:
		card_string += f'''
			<cipt>1</cipt>'''

	card_string += '''
		</card>'''

	if 'double' in card['shape'] and not back:
		card_string += render_card(set_data, github_path, card, True)

	return card_string

def generateFile(code):
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as j:
		set_data = json.load(j)

	github_path = os.path.split(os.getcwd())[1] # this gets the current working directory, so it's an easy failcase

	cockatrice_string = f'''<?xml version='1.0' encoding='UTF-8'?>
<cockatrice_carddatabase version='4'>
	<sets>
		<set>
			<name>{escape_and_format(code)}</name>
			<longname>{escape_and_format(set_data['name'])}</longname>
			<settype>Custom</settype>
			<releasedate>{datetime.today().strftime('%Y-%m-%d')}</releasedate>
		</set>
	</sets>
	<cards>'''

	for card in set_data['cards']:
		cockatrice_string += render_card(set_data, github_path, card)

	cockatrice_string += '''
	</cards>
</cockatrice_carddatabase>'''

	with open(os.path.join('sets', code + '-files', code + '.xml'), 'w', encoding='utf-8') as f:
		f.write(cockatrice_string)
