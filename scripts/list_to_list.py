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
			if cards[i]['card_name'] == cards[j]['card_name'] and "token" not in cards[j]['shape'] and "Basic" not in cards[j]['type']:
				skipdex.append(cards[j]['number'])
	
	master_list = []
	cards_mono = []
	cards_multi = []
	cards_brown = []
	cards_land = []
	cards_basic = []
	cards_token = []
	
	#F: now go over the cards again
	for i in range(len(cards)):
		#F: skip the card if it's in the skipdex
		if cards[i]['number'] in skipdex:
			continue
		card = cards[i]
		# filter sorting tags
		notes = card['notes']
		if '!sort' in notes:
			#F: notes = index of !sort + 6 to the end of the string
			card['notes'] = notes[notes.index('!sort') + 6:]
		else:
			card['notes'] = 'zzz'

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

		# sort types
		#EDIT - replace the array index with JSON keys; 10 = shape, 1 = color, 3 = type
		if 'token' in card['shape']:
			cards_token.append(card)
		elif len(card['color']) > 1:
			cards_multi.append(card)
		elif card['color'] == '':
			if 'Basic' in card['type']:
				cards_basic.append(card)
			elif 'Land' in card['type']:
				cards_land.append(card)
			else:
				cards_brown.append(card)
		else:
			cards_mono.append(card)

	# prepare monocolor lists
	cards_w = []
	cards_u = []
	cards_b = []
	cards_r = []
	cards_g = []
	
	#EDIT - replace the array index with JSON keys
	for card in cards_mono:
		if card['color'] == 'W':
			cards_w.append(card)
		if card['color'] == 'U':
			cards_u.append(card)
		if card['color'] == 'B':
			cards_b.append(card)
		if card['color'] == 'R':
			cards_r.append(card)
		if card['color'] == 'G':
			cards_g.append(card)

	row_count = max(len(cards_w),len(cards_u),len(cards_b),len(cards_r),len(cards_g))
	#F: put all the monocolor things into a big array
	cards_mono_arr = [cards_w, cards_u, cards_b, cards_r, cards_g]
	
	for x in range(len(cards_mono_arr)):
		card_arr = cards_mono_arr[x]
		cards_mono_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	#F: blank1 and blank2 are references to blank pngs for spoilers
	for row in range(row_count):
		for card_arr in cards_mono_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	for x in range(5):
		master_list.append(blank2)

	# prepare gold lists
	cards_wu = []
	cards_ub = []
	cards_br = []
	cards_rg = []
	cards_gw = []
	cards_wb = []
	cards_bg = []
	cards_gu = []
	cards_ur = []
	cards_rw = []

	cards_wub = []
	cards_ubr = []
	cards_brg = []
	cards_rgw = []
	cards_gwu = []
	cards_rwb = []
	cards_gur = []
	cards_wbg = []
	cards_urw = []
	cards_bgu = []

	cards_gold = []

	for card in cards_multi:
		if colorEquals(card['color'], 'WU'):
			cards_wu.append(card)
		elif colorEquals(card['color'], 'UB'):
			cards_ub.append(card)
		elif colorEquals(card['color'], 'BR'):
			cards_br.append(card)
		elif colorEquals(card['color'], 'RG'):
			cards_rg.append(card)
		elif colorEquals(card['color'], 'GW'):
			cards_gw.append(card)
		elif colorEquals(card['color'], 'WB'):
			cards_wb.append(card)
		elif colorEquals(card['color'], 'BG'):
			cards_bg.append(card)
		elif colorEquals(card['color'], 'GU'):
			cards_gu.append(card)
		elif colorEquals(card['color'], 'UR'):
			cards_ur.append(card)
		elif colorEquals(card['color'], 'RW'):
			cards_rw.append(card)
		elif colorEquals(card['color'], 'GWU'):
			cards_gwu.append(card)
		elif colorEquals(card['color'], 'WUB'):
			cards_wub.append(card)
		elif colorEquals(card['color'], 'UBR'):
			cards_ubr.append(card)
		elif colorEquals(card['color'], 'BRG'):
			cards_brg.append(card)
		elif colorEquals(card['color'], 'RGW'):
			cards_rgw.append(card)
		elif colorEquals(card['color'], 'RWB'):
			cards_rwb.append(card)
		elif colorEquals(card['color'], 'GUR'):
			cards_gur.append(card)
		elif colorEquals(card['color'], 'WBG'):
			cards_wbg.append(card)
		elif colorEquals(card['color'], 'URW'):
			cards_urw.append(card)
		elif colorEquals(card['color'], 'BGU'):
			cards_bgu.append(card)
		else:
			cards_gold.append(card)
	
	# ally pairs
	row_count = max(len(cards_wu),len(cards_ub),len(cards_br),len(cards_rg),len(cards_gw))
	cards_ally_arr = [cards_wu, cards_ub, cards_br, cards_rg, cards_gw]

	for x in range(len(cards_ally_arr)):
		card_arr = cards_ally_arr[x]
		cards_ally_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	#F: blank1 and blank2 are references to blank pngs for spoilers
	for row in range(row_count):
		for card_arr in cards_ally_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	for x in range(5):
		master_list.append(blank2)

	# enemy pairs
	row_count = max(len(cards_wb),len(cards_bg),len(cards_gu),len(cards_ur),len(cards_rw))
	cards_enemy_arr = [cards_wb, cards_bg, cards_gu, cards_ur, cards_rw]

	for x in range(len(cards_enemy_arr)):
		card_arr = cards_enemy_arr[x]
		cards_enemy_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in cards_enemy_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	for x in range(5):
		master_list.append(blank2)

	shard_count = len(cards_gwu) + len(cards_wub) + len(cards_ubr) + len(cards_brg) + len(cards_rgw)
	wedge_count = len(cards_rwb) + len(cards_gur) + len(cards_wbg) + len(cards_urw) + len(cards_bgu)

	# shards
	row_count = max(len(cards_gwu),len(cards_wub),len(cards_ubr),len(cards_brg),len(cards_rgw))
	cards_shard_arr = [cards_gwu, cards_wub, cards_ubr, cards_brg, cards_rgw]

	for x in range(len(cards_shard_arr)):
		card_arr = cards_shard_arr[x]
		cards_shard_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for row in range(row_count):
		for card_arr in cards_shard_arr:
			if row >= len(card_arr):
				if shard_count > 5:
					master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if shard_count > 0 and (shard_count >= 5 or wedge_count >= 5):
		for x in range(5):
			master_list.append(blank2)

	# wedges
	row_count = max(len(cards_rwb),len(cards_gur),len(cards_wbg),len(cards_urw),len(cards_bgu))
	cards_wedge_arr = [cards_rwb, cards_gur, cards_wbg, cards_urw, cards_bgu]

	for x in range(len(cards_wedge_arr)):
		card_arr = cards_wedge_arr[x]
		cards_wedge_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in cards_wedge_arr:
			if row >= len(card_arr):
				if wedge_count > 5:
					master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if shard_count > 0 or wedge_count > 0:
		if (shard_count + wedge_count) % 5 != 0:
			for x in range(5 - ((shard_count + wedge_count) % 5)):
				master_list.append(blank1)

		for x in range(5):
			master_list.append(blank2)

	# 4c+ cards
	cards_gold = sorted(cards_gold, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for card in cards_gold:
		master_list.append({'card_name':card['card_name'],'number':card['number'],'shape':card['shape']})

	if len(cards_gold) % 5 != 0:
		for x in range(5 - (len(cards_gold) % 5)):
			master_list.append(blank1)

	if len(cards_gold) > 0:
		for x in range(5):
			master_list.append(blank2)

	# artifacts
	cards_brown = sorted(cards_brown, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for card in cards_brown:
		master_list.append({'card_name':card['card_name'],'number':card['number'],'shape':card['shape']})

	if len(cards_brown) % 5 != 0:
		for x in range(5 - (len(cards_brown) % 5)):
			master_list.append(blank1)

	for x in range(5):
		master_list.append(blank2)

	# lands
	# prepare colored land lists
	lands_w = []
	lands_u = []
	lands_b = []
	lands_r = []
	lands_g = []

	lands_wu = []
	lands_ub = []
	lands_br = []
	lands_rg = []
	lands_gw = []
	lands_wb = []
	lands_bg = []
	lands_gu = []
	lands_ur = []
	lands_rw = []

	lands_wub = []
	lands_ubr = []
	lands_brg = []
	lands_rgw = []
	lands_gwu = []
	lands_rwb = []
	lands_gur = []
	lands_wbg = []
	lands_urw = []
	lands_bgu = []

	lands_other = []

	for card in cards_land:
		if colorEquals(card['color_identity'], 'W'):
			lands_w.append(card)
		elif colorEquals(card['color_identity'], 'U'):
			lands_u.append(card)
		elif colorEquals(card['color_identity'], 'B'):
			lands_b.append(card)
		elif colorEquals(card['color_identity'], 'R'):
			lands_r.append(card)
		elif colorEquals(card['color_identity'], 'G'):
			lands_g.append(card)
		elif colorEquals(card['color_identity'], 'WU'):
			lands_wu.append(card)
		elif colorEquals(card['color_identity'], 'UB'):
			lands_ub.append(card)
		elif colorEquals(card['color_identity'], 'BR'):
			lands_br.append(card)
		elif colorEquals(card['color_identity'], 'RG'):
			lands_rg.append(card)
		elif colorEquals(card['color_identity'], 'GW'):
			lands_gw.append(card)
		elif colorEquals(card['color_identity'], 'WB'):
			lands_wb.append(card)
		elif colorEquals(card['color_identity'], 'BG'):
			lands_bg.append(card)
		elif colorEquals(card['color_identity'], 'GU'):
			lands_gu.append(card)
		elif colorEquals(card['color_identity'], 'UR'):
			lands_ur.append(card)
		elif colorEquals(card['color_identity'], 'RW'):
			lands_rw.append(card)
		elif colorEquals(card['color_identity'], 'GWU'):
			lands_gwu.append(card)
		elif colorEquals(card['color_identity'], 'WUB'):
			lands_wub.append(card)
		elif colorEquals(card['color_identity'], 'UBR'):
			lands_ubr.append(card)
		elif colorEquals(card['color_identity'], 'BRG'):
			lands_brg.append(card)
		elif colorEquals(card['color_identity'], 'RGW'):
			lands_rgw.append(card)
		elif colorEquals(card['color_identity'], 'RWB'):
			lands_rwb.append(card)
		elif colorEquals(card['color_identity'], 'GUR'):
			lands_gur.append(card)
		elif colorEquals(card['color_identity'], 'WBG'):
			lands_wbg.append(card)
		elif colorEquals(card['color_identity'], 'URW'):
			lands_urw.append(card)
		elif colorEquals(card['color_identity'], 'BGU'):
			lands_bgu.append(card)
		else:
			lands_other.append(card)
	
	# monocolor
	row_count = max(len(lands_w),len(lands_u),len(lands_b),len(lands_r),len(lands_g))
	lands_mono_arr = [lands_w, lands_u, lands_b, lands_r, lands_g]

	for x in range(len(lands_mono_arr)):
		card_arr = lands_mono_arr[x]
		lands_mono_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in lands_mono_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if row_count > 0:
		for x in range(5):
			master_list.append(blank2)

	# ally pairs
	row_count = max(len(lands_wu),len(lands_ub),len(lands_br),len(lands_rg),len(lands_gw))
	lands_ally_arr = [lands_wu, lands_ub, lands_br, lands_rg, lands_gw]

	for x in range(len(lands_ally_arr)):
		card_arr = lands_ally_arr[x]
		lands_ally_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in lands_ally_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if row_count > 0:
		for x in range(5):
			master_list.append(blank2)

	# enemy pairs
	row_count = max(len(lands_wb),len(lands_bg),len(lands_gu),len(lands_ur),len(lands_rw))
	lands_enemy_arr = [lands_wb, lands_bg, lands_gu, lands_ur, lands_rw]

	for x in range(len(lands_enemy_arr)):
		card_arr = lands_enemy_arr[x]
		lands_enemy_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in lands_enemy_arr:
			if (row >= len(card_arr)):
				master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if row_count > 0:
		for x in range(5):
			master_list.append(blank2)

	land_shard_count = len(lands_gwu) + len(lands_wub) + len(lands_ubr) + len(lands_brg) + len(lands_rgw)
	land_wedge_count = len(lands_rwb) + len(lands_gur) + len(lands_wbg) + len(lands_urw) + len(lands_bgu)

	# shards
	row_count = max(len(lands_gwu),len(lands_wub),len(lands_ubr),len(lands_brg),len(lands_rgw))
	lands_shard_arr = [lands_gwu, lands_wub, lands_ubr, lands_brg, lands_rgw]

	for x in range(len(lands_shard_arr)):
		card_arr = lands_shard_arr[x]
		lands_shard_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for row in range(row_count):
		for card_arr in lands_shard_arr:
			if row >= len(card_arr):
				if land_shard_count > 5:
					master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if land_shard_count >= 5 or land_wedge_count >= 5:
		for x in range(5):
			master_list.append(blank2)

	# wedges
	row_count = max(len(lands_rwb),len(lands_gur),len(lands_wbg),len(lands_urw),len(lands_bgu))
	lands_wedge_arr = [lands_rwb, lands_gur, lands_wbg, lands_urw, lands_bgu]

	for x in range(len(lands_wedge_arr)):
		card_arr = lands_wedge_arr[x]
		lands_wedge_arr[x] = sorted(card_arr, key=lambda x : (x['rarity'], x['notes'], x['number']))
	
	for row in range(row_count):
		for card_arr in lands_wedge_arr:
			if row >= len(card_arr):
				if land_wedge_count > 5:
					master_list.append(blank1)
			else:
				ca = card_arr[row]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if land_shard_count > 0 or land_wedge_count > 0:
		if (land_shard_count + land_wedge_count) % 5 != 0:
			for x in range(5 - ((land_shard_count + land_wedge_count) % 5)):
				master_list.append(blank1)

	if len(cards_land) - len(lands_other) > 0:
		for x in range(5):
			master_list.append(blank2)

	# other lands
	lands_other = sorted(lands_other, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for card in lands_other:
		master_list.append({'card_name':card['card_name'],'number':card['number'],'shape':card['shape']})

	if len(lands_other) % 5 != 0:
		for x in range(5 - (len(lands_other) % 5)):
			master_list.append(blank1)

	if len(lands_other) > 0 and (len(cards_basic) > 0 or len(cards_token) > 0):
		for x in range(5):
			master_list.append(blank2)

	# basic lands
	#F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
	#EDIT - replace them with the appropriate JSON keys
	cards_basic = sorted(cards_basic, key=lambda x : (x['rarity'], x['notes'], x['number']))

	# if you're reading this, leave me alone, I did this in like 2 minutes I know it's bad code
	#F: well, I probably wouldn't be able to do much better to be completely fair
	basic_types = []
	for card in cards_basic:
		#F: 3 = type
		#EDIT - you know the deal
		if card['type'] not in basic_types:
			basic_types.append(card['type'])

	if len(basic_types) == 0:
		land_count = 0
	else:
		land_count = int(len(cards_basic) / len(basic_types)) # number of different basic arts
	for n in range(land_count): 
		for x in range(len(cards_basic)):
			if (x % land_count == n):
				#F: 0 = name
				#EDIT - you know the deal
				ca = cards_basic[x]
				master_list.append({'card_name':ca['card_name'],'number':ca['number'],'shape':ca['shape']})

	if len(cards_basic) % 5 != 0:
		for x in range(5 - (len(cards_basic) % 5)):
			master_list.append(blank1)

	if len(cards_basic) > 0:
		for x in range(5):
			master_list.append(blank2)

	# tokens
	#F: x[2] = rarity, x[len(x) - 1] = notes, x[4] = card number
	#EDIT - replace them with the appropriate JSON keys
	cards_token = sorted(cards_token, key=lambda x : (x['rarity'], x['notes'], x['number']))

	for card in cards_token:
		#F: 0 = name
		#EDIT - you know the deal
		master_list.append({'card_name':card['card_name'],'number':card['number'],'shape':card['shape']})

	if len(cards_token) % 5 != 0:
		for x in range(5 - (len(cards_token) % 5)):
			master_list.append(blank1)

	#F: lists/SET-list.txt finally comes into play
	with open(outputList, 'w', encoding="utf-8-sig") as f:
		json.dump(master_list, f)

def colorEquals(color, match):

	return sorted("".join(dict.fromkeys(color))) == sorted("".join(dict.fromkeys(match)))
