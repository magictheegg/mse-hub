import os
import sys
import shutil
import json

import image_flip
import card_edge_trimmer
import list_to_list
import print_html_for_index
import print_html_for_search
import print_html_for_preview
import print_html_for_card
import print_html_for_set
import print_html_for_sets_page
import print_html_for_deckbuilder

import markdown

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
				if 'type2' in card:
					card['type2'] = card['type2'].replace('—', '–')
					card['rules_text2'] = card['rules_text2'].replace('—', '–')
					card['special_text2'] = card['special_text2'].replace('—', '–')
				card['image_type'] = 'png' if 'image_type' not in raw else raw['image_type']
				#CE: Designer notes (for Rachel)
				d_notes_path = os.path.join('sets', code + '-files', 'card-notes', card['card_name'] + '.md')
				if os.path.exists(d_notes_path):
					with open(d_notes_path, encoding='utf-8-sig') as md:
						card['designer_notes'] = markdown.markdown(md.read())
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

def portCustomFiles(custom_dir, export_dir):
	for entry in os.scandir(custom_dir):
		#CE: ignore default or generated files
		if entry.name in [ '.DS_Store', '__pycache__', 'README.md' ]:
			continue
		if entry.is_dir():
			c_dir = os.path.join(export_dir, entry.name)
			if not os.path.exists(c_dir): 
				os.makedirs(c_dir) 
			portCustomFiles(os.path.join(custom_dir, entry.name), c_dir)
		else:
			shutil.copy(entry.path, os.path.join(export_dir, entry.name))
			print(os.path.join(export_dir, entry.name) + ' added')

#CE: legacy file removal
for entry in os.scandir('.'):
	if '-spoiler' in entry.name:
		os.remove(entry)

#F: first, get all the set codes
set_codes = []

#CE: remove old files in /sets and /lists
for entry in os.scandir('sets'):
	if entry.is_dir() and entry.name[-6:] == '-files':
		set_codes.append(entry.name[:-6])
	elif entry.name != 'README.md' and os.path.isfile(entry):
		os.remove(entry)

for entry in os.scandir('lists'):
	if entry.name != 'README.md' and os.path.isfile(entry):
		os.remove(entry)

#CE: copy the entire custom tree
portCustomFiles('custom', '')

#F: sort them

set_codes.sort()

#F: then call a previously defined function, which...

genAllCards(set_codes)

set_order = []
#F: iterate over set codes again
for code in set_codes:
	set_order.append(code)
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

#CE: print html for card page
print_html_for_card.generateHTML()
print(f"HTML file for card display saved as card.html")

#CE: only create set_order file if no custom one is provided
custom_order = os.path.join('lists', 'set-order.json')
if not os.path.exists(custom_order):
	set_order_data = {
		"": set_order
	}
	with open(custom_order, 'w', encoding='utf-8-sig') as f:
		json.dump(set_order_data, f)

for code in set_codes:
	#F: more important functions
	#CE: moving this down after we create the 'set-order.json' file
	if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')):
		print_html_for_preview.generateHTML(code)
	print_html_for_set.generateHTML(code)

print_html_for_sets_page.generateHTML()
print_html_for_search.generateHTML(set_codes)
print_html_for_deckbuilder.generateHTML(set_codes)
print_html_for_index.generateHTML()
