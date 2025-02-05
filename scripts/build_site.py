import os
import sys
import shutil
import json

import image_flip
import card_edge_trimmer
import list_to_list
import print_html_for_index
import print_html_for_search
import print_html_for_spoiler
import print_html_for_card
import print_html_for_set
import print_html_for_sets_page
import print_html_for_deckbuilder
import print_json_for_cgs

#F = Fungustober's notes

def genAllCards(codes):
	card_input = {'cards':[]}
	set_input = {'sets':[]}
	#F: ...goes over all the set codes,
	for code in codes:
		#F: grabs the corresponding file,
		with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
			#F: puts its card data into a temp dictionary,
			raw = json.load(f)
			for card in raw['cards']:
				card['type'] = card['type'].replace('—', '–')
				card['rules_text'] = card['rules_text'].replace('—', '–')
				card['special_text'] = card['special_text'].replace('—', '–')
				if not card['rules_text']:
					card['rules_text'] = card['special_text']
				if 'type2' in card:
					card['type2'] = card['type2'].replace('—', '–')
					card['rules_text2'] = card['rules_text2'].replace('—', '–')
					card['special_text2'] = card['special_text2'].replace('—', '–')
				if not card['rules_text2']:
					card['rules_text2'] = card['special_text2']
				card['image_type'] = 'png' if 'image_type' not in raw else raw['image_type']
				#CGS: Requires image path
				token = "t" if "token" in str(card['shape']) else ""
				double = "_front" if "double" in str(card['shape']) else ""
				card['image_path'] = "/sets/" + str(card['set']) + "-files/img/" + str(card['number']) + token + "_" + str(card['card_name']) + double + ".png"
				#CGS: Requires card id
				card['card_id'] = card['set'] + '-' + str(card['number']) + token
				card_input['cards'].append(card)
			set_data = {}
			set_data['set_code'] = code
			set_data['set_name'] = raw['name']
			set_data['formats'] = raw['formats']
			set_input['sets'].append(set_data)
	#F: opens a path,
	with open(os.path.join('lists', 'all-cards.json'), 'w', encoding='utf-8-sig') as f:
		#F: turns the dictionary into a json object, and puts it into the all-cards.json file
		#F: json.dump actually preserves the \n's and the \\'s and whatnot, so we won't have to escape them ourselves
		json.dump(card_input, f)
	with open(os.path.join('lists', 'all-sets.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(set_input, f)

#F: first, get all the set codes

set_codes = []
for entry in os.scandir('sets'):
	if entry.is_dir() and entry.name[-6:] == '-files':
		set_codes.append(entry.name[:-6])
	elif entry.name != 'README.md' and os.path.isfile(entry):
		os.remove(entry)

#F: sort them

set_codes.sort()

#F: then call a previously defined function, which...

genAllCards(set_codes)

if os.path.isdir('cards'):
	shutil.rmtree('cards')
os.mkdir('cards')

set_order = []
#F: iterate over set codes again
for code in set_codes:
	set_order.append(code)
	#F: it makes a directory at cards/SET
	os.mkdir(os.path.join('cards', code))

	image_flip.flipImages(code)
	set_dir = code + '-files'
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
		raw = json.load(f)
	trimmed = raw['trimmed']
	if trimmed == 'n':
		raw['trimmed'] = 'y'
		card_edge_trimmer.batch_process_images(code)
		with open(os.path.join('sets', code + '-files', code + '.json'), 'w', encoding='utf-8-sig') as file:
			json.dump(raw, file)

	#F: list_to_list.convertList is a long and important function
	list_to_list.convertList(code)
	
	custom_dir = os.path.join('custom', set_dir)
	if os.path.isdir(custom_dir):
		for file in os.listdir(custom_dir):
			filepath = os.path.join(custom_dir, file)
			destination = os.path.join('sets', set_dir)
			if os.path.isdir(filepath):
				destination = os.path.join(destination, file)
				if os.path.isdir(destination):
					shutil.rmtree(destination)
				shutil.copytree(filepath, destination)
			else:
				shutil.copy(filepath, destination)
			print(filepath + ' added')

#F: grab lists/all-cards.txt & read it
with open(os.path.join('lists', 'all-cards.json'), encoding='utf-8-sig') as f:
	data = json.load(f)
#F: then the cards get put into an array
card_array = data['cards']
#F: iterate over the array
for card in card_array:
	card_name = card['card_name']
	with open(os.path.join('resources', 'replacechars.txt'), encoding='utf-8-sig') as f:
		chars = f.read()
	for char in chars:
		card_name = card_name.replace(char, '')
	#F: then open a path to cards/SET/NUM_NAME.json & write there
	with open(os.path.join('cards', card['set'], str(card['number']) + '_' + card_name + '.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(card, f)
	#F: and then generate the html file for the card
	print_html_for_card.generateHTML(card)
print(f"HTML card files saved as cards/<set>/<card>.html")

set_order_data = {
	"": set_order
}
with open(os.path.join('lists', 'set-order.json'), 'w', encoding='utf-8-sig') as f:
	json.dump(set_order_data, f)

custom_list_dir = os.path.join('custom', 'lists')
if os.path.isdir(custom_list_dir):
	for file in os.listdir(custom_list_dir):
		filepath = os.path.join(custom_list_dir, file)
		destination = 'lists'
		shutil.copy(filepath, destination)
		print(filepath + ' added')

for code in set_codes:
	#F: more important functions
	#CE: moving this down after we create the 'set-order.json' file
	if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')):
		print_html_for_spoiler.generateHTML(code)
	print_html_for_set.generateHTML(code)

custom_img_dir = os.path.join('custom', 'img')
if os.path.isdir(custom_img_dir):
	for file in os.listdir(custom_img_dir):
		filepath = os.path.join(custom_img_dir, file)
		destination = 'img'
		shutil.copy(filepath, destination)
		print(filepath + ' added')

print_html_for_sets_page.generateHTML()
print_html_for_search.generateHTML(set_codes)
print_html_for_deckbuilder.generateHTML(set_codes)
print_html_for_index.generateHTML()
print_json_for_cgs.generateJSON()







