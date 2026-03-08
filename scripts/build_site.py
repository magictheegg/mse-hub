import os
import sys
import shutil
import json
import glob
import re

import image_flip
import card_edge_trimmer
import list_to_list
import print_draft_file
import print_html_for_index
import print_html_for_set
import print_html_for_sets_page
import print_cockatrice_file

import markdown

#F = Fungustober's notes

def genAllCards(codes):
	card_input = {'cards':[]}
	set_input = {'sets':[]}
	#F: ...goes over all the set codes,
	for code in codes:
		#CE: non-indented JSON is driving me insane
		prettifyJSON(os.path.join('sets', code + '-files', code + '.json'))	
		#F: grabs the corresponding file,
		with open('data/collectionleague/packs.json') as f:
			packs = json.load(f)
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
				if 'v_mana' in raw:
					card['v_mana'] = raw['v_mana']
				#CE: Designer notes (for Rachel)
				d_notes_path = os.path.join('sets', code + '-files', 'card-notes', card['card_name'] + '.md')
				if os.path.exists(d_notes_path):
					with open(d_notes_path, encoding='utf-8') as md:
						card['designer_notes'] = markdown.markdown(md.read())
				card_input['cards'].append(card)
			set_data = {}
			set_data['set_code'] = code
			set_data['set_name'] = raw['name']
			set_data['formats'] = raw['formats']
			set_data['designer'] = raw['designer']
			if code in packs['theme']: set_data['pack'] = True
			set_input['sets'].append(set_data)
	#F: opens a path,
	with open(os.path.join('lists', 'all-cards.json'), 'w', encoding='utf-8') as f:
		#F: turns the dictionary into a json object, and puts it into the all-cards.json file
		#F: json.dump actually preserves the \n's and the \\'s and whatnot, so we won't have to escape them ourselves
		json.dump(card_input, f, indent=4)
	with open(os.path.join('lists', 'all-sets.json'), 'w', encoding='utf-8') as f:
		json.dump(set_input, f, indent=4)

def prettifyJSON(filepath):
	with open(filepath, encoding='utf-8-sig') as f:
		js_data = json.load(f)
	with open(filepath, 'w', encoding='utf-8-sig') as f:
		json.dump(js_data, f, indent=4)

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

def removeStaleFiles(set_dir):
	filesToKeep = [ 'img', 'icon.png', 'logo.png' ]
	for entry in os.scandir(set_dir):
		#CE: ignore default or generated files
		if entry.name in [ '.DS_Store', '__pycache__', 'README.md', 'versions' ]:
			continue
		s_dir = os.path.join(set_dir, entry.name)
		for set_entry in os.scandir(s_dir):
			filename, file_extension = os.path.splitext(set_entry.name)
			if set_entry.name not in filesToKeep and file_extension != '.json':
				if set_entry.is_dir():
					shutil.rmtree(set_entry)
				else:
					os.remove(set_entry)

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

#CE: remove stale files from set directories
removeStaleFiles('sets')

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
	if 'draft_structure' in raw and not raw['draft_structure'] == 'none' and not os.path.isfile(os.path.join('custom', 'sets', code + '-files', code + '-draft.txt')):
		# try:
		print_draft_file.generateFile(code)
			# print('Generated draft file for {0}.'.format(code))
		# except Exception as e:
		# 	print('Unable to generate draft file for {0}: {1}'.format(code, e))

	#CE: trims border radius of images
	if raw['trimmed'] == 'n':
		raw['trimmed'] = 'y'
		card_edge_trimmer.batch_process_images(code)

	with open(os.path.join('sets', code + '-files', code + '.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(raw, f, indent=4)

	#F: list_to_list.convertList is a long and important function
	list_to_list.convertList(code)

#CE: only create set_order file if no custom one is provided
custom_order = os.path.join('lists', 'set-order.json')
if not os.path.exists(custom_order):
	set_order_data = {
		"": set_order
	}
	with open(custom_order, 'w', encoding='utf-8') as f:
		json.dump(set_order_data, f, indent=4)

for code in set_codes:
	#F: more important functions
	#CE: moving this down after we create the 'set-order.json' file
	print_html_for_set.generateHTML(code)

# print_html_for_sets_page.generateHTML()
# print_html_for_index.generateHTML()
print_cockatrice_file.generateFile(set_codes)