import os
import json
import re
from datetime import datetime
import utils

def xml_escape(text: str):
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
			match = re.match(r'([^<]+)(?:<([^<]+)>)?', token)
			if not match:
				print(f'Warning: could not process {instruction} name "{token}". Ignoring')
				continue

			name, num = match.groups()
			if not num:
				extra = ''
			elif num.isdecimal() or num == "x" or num == "X":
				extra = f' count="{num}"'
			elif num == "persistent" or num == "conjure":
				extra = ' persistent=""'
			else:
				print(f'Warning: unknown {instruction} parameter <{num}>. Ignoring')
				extra = ''
			related.append(f'<{tag}{extra}>{xml_escape(name)}</{tag}>')

	return related

def get_number(card, back):
	return f'{card['number']}{'' if 'double' not in card['shape'] else 'b' if back else 'a'}'

def get_tablerow(card_type):
	return (
		2 if 'Creature' in card_type else
		0 if 'Land' in card_type else
		3 if 'Instant' in card_type or 'Sorcery' in card_type else
		1
	)

def get_text(card, back, flipped):
	combine_texts = not back and not flipped and ('split' in card['shape'] or 'adventure' in card['shape'] or 'aftermath' in card['shape'])
	return (
		f'{card[f'rules_text{'2' if back or flipped else ''}']}' +
		(f'\n---\n({'Front' if back else 'Back'}): {card[f'card_name{'' if back else '2'}']}' if 'double' in card['shape'] else '') +
		(f'\n{card['rules_text3']}' if 'rules_text3' in card and card['rules_text3'] else '') +
		(f'\n\n---\n\n{get_text(card, True, False)}' if combine_texts else '')
	).strip()

def render_card(set_data, card, /, *, back=False, flipped=False):
	is_split = 'split' in card['shape'] or 'aftermath' in card['shape']
	is_two_cards = is_split or 'adventure' in card['shape']
	suffix = '2' if back or flipped else ''

	card_type = card[f'type{suffix}'].strip() + (f' // {card[f'type2'].strip()}' if is_two_cards and card[f'type2'] and card[f'type2'] != card[f'type'] else '')
	layout = (
		'mutate' if 'Mutate' in card[f'rules_text{suffix}'] else
		'saga' if 'Saga' in card_type else
		'normal'
	)
	shape_to_layout = {
		'double': 'transform',
		'flip': 'flip',
		'split': 'split',
		'battle': 'battle',
		'adventure': 'adventure',
		'aftermath': 'aftermath',
		'leveler': 'leveler',
	}
	for shape, new_layout in shape_to_layout.items():
		if shape in card['shape']:
			layout = new_layout
			break

	mana_cost = format_cost(card[f'cost{suffix}']) + (f' // {format_cost(card[f'cost2'])}' if is_two_cards else '')
	cmc = cost_to_cmc(card[f'cost{suffix}']) + (cost_to_cmc(card[f'cost2']) if is_split else 0)
	# For the <side>, canon flip cards have their side set to "back" in Cockatrice for their flipped version to transform it back when it leaves the battlefield
	props = f'''
				<layout>{layout}</layout>
				<side>{'back' if back or flipped else 'front'}</side>
				<type>{xml_escape(card_type)}</type>
				<maintype>{xml_escape(get_maintype(card[f'type{suffix}']))}</maintype>
				<manacost>{xml_escape(mana_cost)}</manacost>
				<cmc>{cmc}</cmc>'''

	if len(card[f'color{suffix}']):
		props += f'''
				<colors>{card[f'color{suffix}']}</colors>'''

	color_identity = card['color_identity'].replace('C', '')
	if len(color_identity):
		props += f'''
				<coloridentity>{color_identity}</coloridentity>'''

	if len(card[f'pt{suffix}']):
		props += f'''
				<pt>{xml_escape(card[f'pt{suffix}'])}</pt>'''

	if len(card[f'loyalty{suffix}']):
		props += f'''
				<loyalty>{xml_escape(card[f'loyalty{suffix}'])}</loyalty>'''

	card_name = (f'{card[f'card_name']} // {card[f'card_name2']}' if is_two_cards else card[f'card_name{suffix}']) + (f' {card['set']}' if 'token' in card['shape'] else '')
	card_string = f'''
		<card>
			<name>{xml_escape(card_name)}</name>
			<text>{re.sub(r'\[/?i\]', '', xml_escape(get_text(card, back, flipped)))}</text>
			<set rarity="{'rare' if card['rarity'] == 'cube' else card['rarity']}" picurl="{xml_escape(utils.get_picurl(set_data, card, back))}" num="{get_number(card, back)}">{xml_escape(card['set'])}</set>
			<prop>{props}
			</prop>
			<tablerow>{get_tablerow(card_type)}</tablerow>'''

	if 'token' in card['shape']:
		card_string += '''
			<token>1</token>'''

	if flipped:
		card_string += '''
			<upsidedown>1</upsidedown>'''

	related = get_related(card['notes'], '!tokens', 'related')
	if 'double' in card['shape']:
		related.append(f'<related attach="transform">{xml_escape(card['card_name' if back else 'card_name2'])}</related>')
	if 'flip' in card['shape']:
		related.append(f'<related attach="transform">{xml_escape(card['card_name' if flipped else 'card_name2'])}</related>')
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
		card_string += render_card(set_data, card, back=True)

	if 'flip' in card['shape'] and not flipped:
		card_string += render_card(set_data, card, flipped=True)

	return card_string

def generateFile(code):
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as j:
		set_data = json.load(j)

	cockatrice_string = f'''<?xml version='1.0' encoding='UTF-8'?>
<cockatrice_carddatabase version='4'>
	<sets>
		<set>
			<name>{xml_escape(code)}</name>
			<longname>{xml_escape(set_data['name'])}</longname>
			<settype>Custom</settype>
			<releasedate>{datetime.today().strftime('%Y-%m-%d')}</releasedate>
		</set>
	</sets>
	<cards>'''

	for card in set_data['cards']:
		cockatrice_string += render_card(set_data, card)

	cockatrice_string += '''
	</cards>
</cockatrice_carddatabase>'''

	with open(os.path.join('sets', code + '-files', code + '.xml'), 'w', encoding='utf-8') as f:
		f.write(cockatrice_string)
