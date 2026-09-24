import os
import sys
import shutil
import json
import glob
import re

import list_to_list
import print_cockatrice_file
import print_draft_file
import print_html_for_index
import print_html_for_search
import print_html_for_preview
import print_html_for_card
import print_html_for_set
import print_html_for_sets_page
import print_html_for_deckbuilder
import print_html_for_deck_page
import print_html_for_articles
import print_html_for_decks_page

import markdown

#F = Fungustober's notes

def genAllCards(codes):
	card_input = {'cards':[]}
	set_input = {'sets':[]}
	#F: ...goes over all the set codes,
	for code in codes:
		#CE: check to see if the set is currently previewing
		previewed_path = os.path.join('sets', code + '-files', 'previewed.txt')
		previewed_cards = None
		if os.path.exists(previewed_path):
			with open(previewed_path, encoding='utf-8-sig') as f:
				previewed_cards = f.read().split('\n')
		#CE: non-indented JSON is driving me insane
		prettifyJSON(os.path.join('sets', code + '-files', code + '.json'))	
		#F: grabs the corresponding file,
		with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
			#F: puts its card data into a temp dictionary,
			raw = json.load(f)
			if raw.get('hidden'):
				continue
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
					with open(d_notes_path, encoding='utf-8-sig') as md:
						card['designer_notes'] = markdown.markdown(md.read())
				if previewed_cards == None or card['card_name'] in previewed_cards:
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
		json.dump(card_input, f, indent=4)
	with open(os.path.join('lists', 'all-sets.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(set_input, f, indent=4)

def generateFormats():
	default_path = os.path.join('resources', 'default-formats.json')
	custom_path = os.path.join('custom', 'lists', 'formats.json')
	output_path = os.path.join('lists', 'formats.json')

	with open(default_path, 'r', encoding='utf-8-sig') as f:
		data = json.load(f)

	if os.path.exists(custom_path):
		with open(custom_path, 'r', encoding='utf-8-sig') as f:
			data = json.load(f)

	with open(output_path, 'w', encoding='utf-8-sig') as f:
		json.dump(data, f, indent=4)

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
			if set_entry.name not in filesToKeep and file_extension != '.json' and file_extension != '.xml':
				if set_entry.is_dir():
					shutil.rmtree(set_entry)
				else:
					os.remove(set_entry)

#CE: legacy file removal
for entry in os.scandir('.'):
	if '-spoiler' in entry.name:
		os.remove(entry)

#CE: auto-generate site-config.json
repo_name = os.path.basename(os.getcwd()).lower()
default_config = {
	"base_url": f"https://{repo_name}"
}
with open(os.path.join('resources', 'site-config.json'), 'w', encoding='utf-8-sig') as f:
	json.dump(default_config, f, indent=4)

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

generateFormats()

if os.path.exists('articles'):
	# Recursive cleanup of .html files
	for root, dirs, files in os.walk('articles'):
		for file in files:
			if file.endswith('.html'):
				os.remove(os.path.join(root, file))
	
	# Prune empty subdirectories
	for root, dirs, files in os.walk('articles', topdown=False):
		for dir in dirs:
			dir_path = os.path.join(root, dir)
			if not os.listdir(dir_path):
				os.rmdir(dir_path)

#CE: remove stale files from set directories
removeStaleFiles('sets')

#CE: copy the entire custom tree
portCustomFiles('custom', '')

#CE: reload config in case it was overwritten by custom files
import utils
utils.load_config()

#F: sort them
set_codes.sort()

#F: then call a previously defined function, which...

genAllCards(set_codes)

set_order = []
#F: iterate over set codes again
for code in set_codes:
	set_order.append(code)
	set_dir = code + '-files'
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
		raw = json.load(f)
	if 'draft_structure' not in raw or not raw['draft_structure'] == 'none' and not os.path.isfile(os.path.join('custom', 'sets', code + '-files', code + '-draft.txt')):
		try:
			print_draft_file.generateFile(code)
			print('Generated draft file for {0}.'.format(code))
		except Exception as e:
			print('! Unable to generate draft file for {0}: {1}'.format(code, e))

	# CE: Trice
	if not os.path.isfile(os.path.join('custom', 'sets', code + '-files', code + '.xml')):
		try:
			print_cockatrice_file.generateFile(code)
			print('Generated Cockatrice file for {0}.'.format(code))
		except Exception as e:
			print('! Unable to generate Cockatrice file for {0}: {1}'.format(code, e))

	#CE: this code is all for version history
	if 'version' not in raw:
		versions = glob.glob(os.path.join('sets', 'versions', '*_' + code + '*'))
		if len(versions) == 0:
			shutil.copyfile(os.path.join('sets', code + '-files', code + '.json'), os.path.join('sets', 'versions', '1_' + code + '.json'))
			prettifyJSON(os.path.join('sets', 'versions', '1_' + code + '.json'))
			raw['version'] = 1
			with open(os.path.join('sets', 'versions', 'changelogs', 'chl_' + code + '.txt'), 'w', encoding='utf-8-sig') as f:
				f.write('VERSION 1 CHANGELOG\n====================\n\nFirst version published.')
		else:
			regex = r'[/\\]([0-9]+)_'
			match = re.search(regex, versions[0])
			old_version = int(match.group(1))
			new_version = int(match.group(1)) + 1
			changed = False
			chl_string = 'VERSION ' + str(new_version) + ' CHANGELOG\n====================\n'
			added_string = ''
			removed_string = ''
			changed_string = ''
			with open(versions[0], encoding='utf-8-sig') as f:
				previous_data = json.load(f)
			# put the names into an array to reduce runtime
			prev_card_names = []
			for card in previous_data['cards']:
				if 'token' in card['type'] or 'Basic' in card['type']:
					prev_card_names.append('')
				else:
					prev_card_names.append(card['card_name'])
			for card in raw['cards']:
				# skip tokens and basics
				if 'token' in card['type'] or 'Basic' in card['type']:
					continue
				if card['card_name'] not in prev_card_names:
					changed = True
					added_string += card['card_name'] + ' added.\n'
				else:
					prev_card = previous_data['cards'][prev_card_names.index(card['card_name'])]
					prev_card_names[prev_card_names.index(card['card_name'])] = ''

					# ignore card number, since that often changes for reasons unrelated to the card itself
					card_copy = card.copy()
					prev_card_copy = prev_card.copy()
					card_copy.pop("number", None)
					prev_card_copy.pop("number", None)

					if card_copy != prev_card_copy:
						changed = True
						changed_string += card['card_name'] + '\n'
						for key in [ 'type', 'cost', 'rules_text', 'flavor_text', 'pt', 'special_text', 'loyalty', "artist" ]:
							if card[key] != prev_card[key]:
								changed_string += key + ': ' + prev_card[key] + ' => ' + card[key] + '\n'
						changed_string += '\n'
			for name in prev_card_names:
				if name != '':
					changed = True
					removed_string += name + ' removed.\n'

			with open(os.path.join('sets', 'versions', 'changelogs', 'chl_' + code + '.txt'), 'r+', encoding='utf-8-sig') as f:
				file_content = f.read()
				f.seek(0, 0)
				if not changed:
					to_write = '\n'.join( [ chl_string, 'No changes.\n' ] )
				else:
					to_write = '\n'.join([ chl_string, added_string, removed_string, changed_string ])
				f.write(to_write + '\n' + file_content)
			
			shutil.copyfile(os.path.join('sets', code + '-files', code + '.json'), os.path.join('sets', 'versions', str(new_version) + '_' + code + '.json'))
			prettifyJSON(os.path.join('sets', 'versions', str(new_version) + '_' + code + '.json'))
			os.remove(os.path.join('sets', 'versions', str(old_version) + '_' + code + '.json'))
			raw['version'] = new_version

	with open(os.path.join('sets', code + '-files', code + '.json'), 'w', encoding='utf-8-sig') as f:
		json.dump(raw, f, indent=4)

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
		json.dump(set_order_data, f, indent=4)

for code in set_codes:
	#F: more important functions
	#CE: moving this down after we create the 'set-order.json' file
	if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')) and not os.path.isfile(os.path.join('custom', 'previews', code + '.html')):
		print_html_for_preview.generateHTML(code)
	print_html_for_set.generateHTML(code)

print_html_for_sets_page.generateHTML()
print_html_for_search.generateHTML(set_codes)
print_html_for_deckbuilder.generateHTML(set_codes)
print_html_for_deck_page.generateHTML(set_codes)
# Clear existing global pages to ensure they only exist if content is present
for page in ['all-articles.html', 'decks.html']:
	if os.path.exists(page):
		os.remove(page)

print_html_for_index.generateHTML()

# Only generate Articles if content exists
has_articles = print_html_for_articles.generateHTML()
if not has_articles:
	print("No articles found; skipping all-articles.html")

# Only generate Decks if decks exist in Supabase for this hub
def check_for_decks():
	try:
		import urllib.request
		with open(os.path.join('resources', 'site-config.json'), encoding='utf-8-sig') as f:
			config = json.load(f)
			base_url = config.get('base_url', '')
			hub_name = base_url.split('https://')[1].split('.github.io')[0].lower() if 'https://' in base_url else 'unknown'
		
		url = f"https://mtjkkvtcmejzcpjmropd.supabase.co/rest/v1/decks?hub=eq.{hub_name}&select=id&limit=1"
		req = urllib.request.Request(url)
		req.add_header('apikey', 'sb_publishable_Hgyr2JJRsJRa1pYwoz-ijQ_ozfwnp9t')
		req.add_header('Authorization', 'Bearer sb_publishable_Hgyr2JJRsJRa1pYwoz-ijQ_ozfwnp9t')
		
		with urllib.request.urlopen(req) as response:
			data = json.loads(response.read().decode())
			return len(data) > 0
	except Exception as e:
		print(f"Warning: Could not check Supabase for decks: {e}")
		return True # Default to generating if check fails

if check_for_decks():
	print_html_for_decks_page.generateHTML()
else:
	print("No decks found for this hub; skipping decks.html")
