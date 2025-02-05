import os
import sys
import json

#F = Fungustober's notes

def generateHTML(card):
	code = card['set']
	card_name = card['card_name']
	card_name_cleaned = card_name
	card_type = card['type']
	with open(os.path.join('resources', 'replacechars.txt'), encoding='utf-8-sig') as f:
		chars = f.read()
	for char in chars:
		card_name_cleaned = card_name_cleaned.replace(char, '')
	card_num = card['number']
	#F: /cards/SET/NUM_NAME.html
	output_html_file = "cards/" + code + "/" + str(card_num) + "_" + card_name_cleaned + ".html"
	
	with open(os.path.join('lists', 'all-sets.json'), encoding='utf-8-sig') as f:
		data = json.load(f)
		for s in data['sets']:
			if s['set_code'] == code:
				set_name = s['set_name']
				break
	
	# Start creating the HTML file content
	html_content = '''<html>
<head>
  <title>''' + card['card_name'] + '''</title>
  <link rel="icon" type="image/x-icon" href="/sets/''' + code + '''-files/icon.png">
  <link rel="stylesheet" href="/resources/mana.css">
  <link rel="stylesheet" href="/resources/header.css">
</head>
<style>
	@font-face {
	  font-family: Beleren;
	  src: url('/resources/beleren.ttf');
	}
	body {
		font-family: 'Helvetica', 'Arial', sans-serif;
		overscroll-behavior: none;
		margin: 0px;
		background-color: #f3f3f3;
	}
	a {
		text-decoration: none;
	}
	.banner-container {
		width: 100%;
		background-color: #bbbbbb;
		display: flex;
		justify-items: center;
		align-items: center;
	}
	.set-banner {
		font-family: Beleren;
		display: flex;
		gap: 30px;
		align-items: center;
		justify-items: center;
		font-size: 40px;
		color: #171717;
		margin: auto;
		padding-top: 10px;
		padding-bottom: 10px;
	}
	.set-banner img {
		width: 100px;
	}
	.image-grid {
		padding-top: 40px;
		width: 70%;
		max-width: 1000px;
		margin: auto;
		display: grid;
		grid-template-columns: minmax(200px, 2fr) minmax(200px, 2.5fr);
		gap: 30px;
		padding-bottom: 10px;
		justify-items: center;
	}
	.image-grid img {
		position: relative;
	}
	.card-image {
		float: left;
		width: 100%;
		max-width: 375px;
		height: auto;
		display: block;
	}
	.card-text {
		padding-top: 20px;
		padding-bottom: 20px;
		background: #fcfcfc;
		width: 100%;
		border: 1px solid #d5d9d9;
		border-top: 3px solid #171717;
		border-bottom: 3px solid #171717;
		border-radius: 6px;
		height: fit-content;
		min-height: 75%;
		margin-top: 3%;
		display: flex;
		flex-direction: column;
	}
	.card-text div {
		white-space: normal;
		font-size: 15px;
		padding-bottom: 10px;
		padding-left: 12px;
		padding-right: 12px;
		line-height: 155%;
	}
	.card-text .name-cost {
		font-weight: bold;
		font-size: 20px;
		white-space: pre-wrap;
	}
	.card-text .type {
		font-size: 16px;
	}
	.card-text .pt {
		font-weight: bold;
	}
	.card-text br {
		content: "";
		display: block;
		margin-bottom: 5px;
	}
	.card-text .printings {
		margin-top: auto;
		font-size: 12px;
		font-weight: bold;
		padding-bottom: 0px;
	}
	.printings {
		display: none;
	}
	.printings a {
		color: #1338be;
		text-decoration: none;
	}
	.printings a:hover {
		color: #0492c2;
	}
	.img-container {
	  position: relative;
	  align-self: center;
	}
	.img-container img {
	  width: 100%;
	  height: auto;
	}
	.img-container .btn {
		background: url('/img/flip.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 15%;
		height: 11%;
		cursor: pointer;
		border: none;
		position: absolute;
		left: 50%;
		top: 48%;
		transform: translate(-50%, -50%);
		opacity: 0.5;
	}
	.img-container .btn:hover {
		background: url('/img/flip-hover.png') no-repeat;
		background-size: contain;
		background-position: center;
	}
	.img-container .h-img {
		transform: rotate(90deg);
		width: 80%;
	}
	.img-container a {
		height: 100%;
		display: grid;
		justify-self: center;
		align-items: center;
		justify-items: center;
	}
	.img-container a > * {
		grid-row: 1;
		grid-column: 1;
	}
	.hidden {
		display: none;
	}
</style>
<body>
	'''

	with open(os.path.join('resources', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		snippet = f.read().replace('domain', os.path.basename(os.getcwd()))
		html_content += snippet

	html_content += '''

	<input type="text" id="display" class="hidden" value="cards-and-text"> <!-- here to make img-container-defs snippet work properly -->
	<div class="banner-container">
		<a class="set-banner" id="set-banner" href="/sets/''' + code + '''">
			<img class="set-logo" src="/sets/''' + code + '''-files/icon.png">
			<div class="set-title">''' + set_name + '''</div>
		</a>
	</div>

	<div class="grid-container" id="grid">
	</div>
	'''

	other_printings = []
	#F: lists/all-cards.json
	with open(os.path.join('lists', 'all-cards.json'), encoding='utf-8-sig') as f:
		cards = json.load(f)
	cards = cards['cards']
	for i in range(len(cards)):
		card_stats = cards[i]
		if card_stats['card_name'] == card_name and card_stats['type'] == card_type and (card_stats['set'] != code or card_stats['number'] != card_num) and 'token' not in card_stats['shape']:
			other_printings.append(card_stats)
	if other_printings != []:
		html_content += '''<div class="printings" id="other-printings">Other Printings: '''
		for printing in other_printings:
			set_code = printing['set']
			html_content += '''<a href="/cards/''' + set_code + '''/''' + str(printing['number']) + '''_''' + card_name_cleaned + '''">''' + set_code + '''</a>'''
			if printing != other_printings[len(other_printings) - 1]:
				html_content += ''' • '''
		html_content += '''</div>
		'''
	
	html_content += '''
	<script>
		let card_list_arrayified = [];
		let specialchars = "";

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet
	
	html_content += '''
			await fetch('/cards/''' + code + '''/''' + str(card_num) + '''_''' + card_name_cleaned + '''.json')
				.then(response => response.json())
				.then(json => {
					card = json;
			}).catch(error => console.error('Error:', error));

			document.getElementById("grid").appendChild(gridifyCard(card, false, true));
			if (document.getElementById("other-printings"))
			{
				document.getElementById("card-text").appendChild(document.getElementById("other-printings"));
				document.getElementById("other-printings").style.display = "block";
			}
		});

		'''
	
	with open(os.path.join('resources', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function gridifyCard(card_stats, card_text = false, rotate_card = false) {
			card_stats = card;
			const card_name = card_stats.card_name;

		'''
	
	with open(os.path.join('resources', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		document.getElementById("search").addEventListener("keypress", function(event) {
		  if (event.key === "Enter") {
				event.preventDefault();
				search();
		  }
		});

		function search() {
			window.location = ("/search?search=" + document.getElementById("search").value);
		}

		'''

	with open(os.path.join('resources', 'snippets', 'random-card.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
	</script>
</body>
</html>'''

	# Write the HTML content to the output HTML file
	with open(output_html_file, 'w', encoding='utf-8-sig') as file:
		file.write(html_content)
		print(card_name + " HTML page written")
