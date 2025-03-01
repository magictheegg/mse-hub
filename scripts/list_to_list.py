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
	#F: This gets any alt-arts in a single set and adds their card number to a list of cards to skip.
	for i in range(len(cards)):
		for j in range(i):
			if cards[i]['card_name'] == cards[j]['card_name'] and "token" not in cards[i]['shape'] and "Basic" not in cards[i]['type']:
				skipdex.append(cards[j]['number'])
	
	master_list = []
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
		'sort_group1': [],
		'sort_group2': []
	}

	#F: now go over the cards again
	for card in cards:
		#F: skip the card if it's in the skipdex
		if card['number'] in skipdex:
			continue

		# sort types
		#EDIT - replace the array index with JSON keys; 10 = shape, 1 = color, 3 = type
		if '!sort_group1' in card['notes']:
			cards_sorted['sort_group1'].append(card)
		elif '!sort_group2' in card['notes']:
			cards_sorted['sort_group2'].append(card)
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
		elif '!last' not in notes:
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
		for index in list_order[r]:
			row_count = max(row_count, len(cards_sorted[index]))
			cards_arr.append(cards_sorted[index])

		if (row_count > 0):
			for x in range(len(cards_arr)):
				if len(cards_arr[x]) > 0 and 'Basic' not in cards_arr[x][0]['type']:
					cards_arr[x] = sorted(cards_arr[x], key=lambda x : (len(x['color']), x['rarity'], x['notes'], x['number'])) # start with len() for 3+c cards
					# otherwise, preserve order of basics from set file

			for row in range(row_count):
				for arr in cards_arr:
					if (row >= len(arr)):
						master_list.append(blank1)
					else:
						ca = arr[row]
						master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

			if len(list_order[r]) == 1: # single-card categories
				if not row_count % 5 == 0:
					for x in range(5 - (row_count % 5)):
						master_list.append(blank1)

			for x in range(5):
				master_list.append(blank2)

	#F: lists/SET-list.txt finally comes into play
	with open(outputList, 'w', encoding="utf-8-sig") as f:
		json.dump(master_list, f)

def colorEquals(color, match):
	return sorted("".join(dict.fromkeys(color))) == sorted("".join(dict.fromkeys(match)))