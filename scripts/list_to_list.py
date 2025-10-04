import os
import sys
import re
import json

#F = Fungustober's notes

def convertList(setCode):
	#F: inputList = sets/SET-files/SET.json
	inputList = os.path.join('sets', setCode + '-files', setCode + '.json')
	#F: outputList = lists/SET-list.json
	outputList = os.path.join('lists', setCode + '-list.json')
	
	#create the two blanks as dictionaries so we can fit them into the JSON structure
	blank1 = {'card_name':'e'}
	blank2 = {'card_name':'er'}
	#F: open up the inputList file
	with open(inputList, encoding='utf-8-sig') as f:
		raw = json.load(f)
	cards = raw['cards']

	#F: array of cards to skip
	skipdex = []
	#CE: array of special sort groups
	sort_groups = []
	#F: This gets any alt-arts in a single set and adds their card number to a list of cards to skip.
	#CE: And also appends all available groups to the set
	for i in range(len(cards)):
		match = re.search(r'!group ([^ \n]+)', cards[i]['notes'])
		if match and match.group() not in sort_groups:
			sort_groups.append(match.group())
		if "token" in cards[i]['shape'] or "Basic" in cards[i]['type']:
			continue
		for j in range(i):
			if cards[i]['card_name'] == cards[j]['card_name'] and "token" not in cards[j]['shape'] and "Basic" not in cards[j]['type']:
				skipdex.append(cards[j]['number'])

	final_list = []
	cards_mono = []
	cards_multi = []
	cards_brown = []
	cards_land = []
	cards_basic = []
	cards_token = []

	colors = [ 'W', 'U', 'B', 'R', 'G' ]
	guilds = [ 'WU', 'UB', 'BR', 'RG', 'GW', 'WB', 'BG', 'GU', 'UR', 'RW' ]
	shards = [ 'WUB', 'UBR', 'BRG', 'RGW', 'GWU', 'WBG', 'BGU', 'GUR', 'URW', 'RWB' ] # and wedges

	cards_sorted = {
		'W': [],
		'U': [],
		'B': [],
		'R': [],
		'G': [],
		'WU': [],
		'UB': [],
		'BR': [],
		'RG': [],
		'GW': [],
		'WB': [],
		'BG': [],
		'GU': [],
		'UR': [],
		'RW': [],
		'WUB': [],
		'UBR': [],
		'BRG': [],
		'RGW': [],
		'GWU': [],
		'WBG': [],
		'BGU': [],
		'GUR': [],
		'URW': [],
		'RWB': [],
		'gold': [],
		'C': [],
		'WL': [],
		'UL': [],
		'BL': [],
		'RL': [],
		'GL': [],
		'WUL': [],
		'UBL': [],
		'BRL': [],
		'RGL': [],
		'GWL': [],
		'WBL': [],
		'BGL': [],
		'GUL': [],
		'URL': [],
		'RWL': [],
		'L': [],
		'basic': [],
		'token': [],
		'mp': [],
		'': []
	}

	for group in sort_groups:
		cards_sorted[group] = []

	#CE: set up previews if necessary
	if 'unpreviewed' in raw and raw['unpreviewed'] == 'empty':
		previewed_path = os.path.join('sets', setCode + '-files', 'previewed.txt')
		if os.path.isfile(previewed_path):
			with open(previewed_path, encoding='utf-8-sig') as f:
				previewed = f.read().split('\n')

	#F: now go over the cards again
	for card in cards:
		#F: skip the card if it's in the skipdex
		if card['number'] in skipdex or ('previewed' in locals() and card['card_name'] not in previewed):
			continue

		#CE: fix for devoid cards
		if 'devoid' in card['rules_text'].lower():
			card['color'] = card['color_identity']

		#CE: fix for split cards
		if 'split' in card['shape']:
			card['color'] = "".join(set(card['color'] + card['color2']))

		# sort types
		if '!group' in card['notes']:
			for group in sort_groups:
				pattern = re.compile(re.escape(group) + r'(?:\n|$)')
				if pattern.search(card['notes']):
					cards_sorted[group].append(card)
		elif 'token' in card['shape']:
			cards_sorted['token'].append(card)
		elif 'masterpiece' in card['rarity']: # masterpiece
			cards_sorted['mp'].append(card)
		elif len(card['color']) > 1:
			assigned = False
			for guild in guilds:
				if colorEquals(card['color'], guild):
					cards_sorted[guild].append(card)
					assigned = True
			if not assigned:
				cards_sorted['gold'].append(card)
		elif card['color'] == '':
			if 'Basic' in card['type']:
				cards_sorted['basic'].append(card)
			elif 'Land' in card['type']:
				assigned = False
				for c in colors:
					if colorEquals(card['color_identity'], c):
						cards_sorted[c + 'L'].append(card)
						assigned = True
				for guild in guilds:
					if colorEquals(card['color_identity'], guild):
						cards_sorted[guild + 'L'].append(card)
						assigned = True
				if not assigned:
					cards_sorted['L'].append(card)
			else:
				cards_sorted['C'].append(card)
		else:
			for c in colors:
				if card['color'] == c:
					cards_sorted[c].append(card)

		# clean rarities
		if card['rarity'] == 'common':
			card['rarity'] = 4
		elif card['rarity'] == 'uncommon':
			card['rarity'] = 3
		elif card['rarity'] == 'rare':
			card['rarity'] = 2
		elif card['rarity'] == 'mythic':
			card['rarity'] = 1
		else:
			card['rarity'] = 5

		# filter sorting tags
		notes = card['notes']
		if '!sort' in notes:
			#F: notes = index of !sort + 6 to the end of the string
			card['notes'] = notes[notes.index('!sort') + 6:]
		else:
			card['notes'] = 'zzz'

		# clean shape
		if 'Battle' in card['type']:
			card['shape'] = card['shape'] + ' split'

	if len(cards_sorted['gold']) >= 10: # probably has a decent number of tri-color cards
		tmp = cards_sorted['gold']
		cards_sorted['gold'] = []
		for card in tmp:
			assigned = False
			for shard in shards: # and wedges
				if colorEquals(card['color_identity'], shard): # or wedge
					cards_sorted[shard].append(card)
					assigned = True
			if not assigned:
				cards_sorted['gold'].append(card)

	preview_path = 'resources'
	if os.path.isfile(os.path.join('sets', setCode + '-files', 'preview-order.json')):
		preview_path = os.path.join('sets', setCode + '-files')

	with open(os.path.join(preview_path, 'preview-order.json'), encoding='utf-8-sig') as j:
		list_order = json.load(j)

	for r in list_order:
		row_count = 0
		cards_arr = []
		code = setCode
		if 'set' in r:
			if r['logo']:
				final_list.append('l->' + r['set'])
				for x in range(5):
					final_list.append(blank2)
			code = r['set']
			external = os.path.join('sets', code + '-files', code + '.json')
			ext_cards = []
			with open(external, encoding='utf-8-sig') as j:
				ext_js = json.load(j)
			for card in ext_js['cards']:
				if r['cards'][0] in card['notes']:
					ext_cards.append(card)
			cards_arr.append(ext_cards)
			row_count = len(ext_cards)
		elif 'html' in r:
			final_list.append('h->' + r['html'])
			for x in range(5):
					final_list.append(blank2)
			continue
		else:
			for index in r['cards']:
				if index not in cards_sorted:
					print(f'INFO: Group {index} not found in any card notes.')
					index = ''
				row_count = max(row_count, len(cards_sorted[index]))
				cards_arr.append(cards_sorted[index])

		if (row_count > 0):
			if 'title' in r and len(final_list) > 0:
				del final_list[-1]
				final_list.append('a->' + r['title'])
			for x in range(len(cards_arr)):
				if len(cards_arr[x]) > 0 and 'Basic' not in cards_arr[x][0]['type']:
					if len(r['cards']) == 1 and r['cards'][0] in sort_groups:
						cards_arr[x] = sorted(cards_arr[x], key=lambda x : (x['notes'], x['rarity'], x['number']))
					else:
						cards_arr[x] = sorted(cards_arr[x], key=lambda x : (len(x['color']), x['rarity'], x['notes'], x['number'])) # start with len() for 3+c cards
					# otherwise, preserve order of basics from set file

			for row in range(row_count):
				for arr in cards_arr:
					if (row >= len(arr)):
						final_list.append(blank1)
					else:
						ca = arr[row]
						final_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape'],'set':code,'position':('' if 'position' not in ca else ca['position'])})

			if len(r['cards']) == 1: # single-card categories
				if not row_count % 5 == 0:
					for x in range(5 - (row_count % 5)):
						final_list.append(blank1)

			for x in range(5):
				final_list.append(blank2)

	#F: lists/SET-list.txt finally comes into play
	with open(outputList, 'w', encoding="utf-8-sig") as f:
		json.dump(final_list, f, indent=4)

def colorEquals(color, match):
	return sorted("".join(dict.fromkeys(color))) == sorted("".join(dict.fromkeys(match)))