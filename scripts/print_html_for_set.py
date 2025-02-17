import os
import sys
import json
import markdown
import re

#F = Fungustober's notes

def generateHTML(code):
	#F: /sets/SET.html
	output_html_file = "sets/" + code + ".html"
	
	with open(os.path.join('lists', 'all-sets.json'), encoding='utf-8-sig') as f:
		data = json.load(f)
		for s in data['sets']:
			if s['set_code'] == code:
				set_name = s['set_name']
				break

	# Start creating the HTML file content
	html_content = '''<html>
<head>
  <title>''' + set_name + '''</title>
  <link rel="icon" type="image/x-icon" href="/sets/''' + code + '''-files/icon.png">
  <link rel="stylesheet" href="/resources/mana.css">
  <link rel="stylesheet" href="/resources/header.css">
</head>
<style>
		@font-face {
			font-family: 'Beleren Small Caps';
			src: url('/resources/beleren-caps.ttf');
		}
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
	.banner {
		width: 100%;
		background-color: #bbbbbb;
	}
	.banner-container {
		width: 85%;
		max-width: 1100px;
		display: grid;
		grid-template-columns: 1fr 1fr;
		align-items: center;
		margin: auto;
	}
	.set-banner {
		font-family: Beleren;
		display: flex;
		gap: 30px;
		align-items: center;
		justify-items: center;
		font-size: 26px;
		color: #171717;
		margin: auto;
		padding-top: 10px;
		padding-bottom: 10px;
		justify-self: left;
		width: 100%;
		white-space: nowrap;
	}
	.set-banner img {
		width: 50px;
	}
	.set-banner a {
		font-size: 18px;
		padding-top: 6px;
		color: #1338be;
		text-decoration: none;
	}
	.set-banner a:hover {
		color: #0492c2;
	}
	.select-text {
		display: flex;
		align-items: center;
		justify-content: left;
		gap: 8px;
		font-size: 14.5px;
		justify-self: right;
		text-align: center;
	}
	select {
		background-color: #fafafa;
		border: 1px solid #656565;
		border-radius: 8px;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		text-align: center;
		color: #171717;
		font-size: 13px;
		height: 30px;
	}
	.button-container {
		width: 50%;
		max-width: 900px;
		margin: auto;
		padding: 15px 0 5px 0;
		border-bottom: 2px solid #171717;
		display: grid;
		grid-template-columns: 1fr 1fr;
	}
	.button-container button {
		font-family: Beleren;
		font-size: 30px;
		width: 100%;
		justify-self: center;
		border: none;
		background: none;
		cursor: pointer;
	}
	.button-container button:hover {
		color: #797979;
	}
	.button-container button:disabled {
		color: #797979;
		cursor: auto;
	}
	.grid-container {
		display: grid;
		grid-template-columns: auto;
		padding-top: 30px;
		padding-bottom: 30px;
		max-width: 1200px;
		margin: auto;
	}
	.splash-container {
		width: 70%;
		max-width: 1200px;
		margin: auto;
		justify-items: center;
	}
	.image-grid-container {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		width: 70%;
		max-width: 1200px;
		margin: auto;
		gap: 5px;
		justify-items: center;
		padding-top: 30px;
		padding-bottom: 30px;
	}
	@media ( max-width: 750px ) {
		.image-grid-container {
			grid-template-columns: 1fr 1fr;  
		}
	}
	.image-grid {
		width: 70%;
		margin: auto;
		display: grid;
		grid-template-columns: minmax(150px, 1fr) minmax(300px, 2fr);
		gap: 50px;
		padding-bottom: 10px;
		justify-items: left;
	}
	.image-grid img {
		position: relative;
	}
	.card-image {
		float: left;
		width: 100%;
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
	.img-container {
		position: relative;
		width: 100%;
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
	.img-container .hidden-text {
		position: absolute;
		font-family: Beleren;
		top: 5%;
		left: 9%;
		font-size: .97vw;
		color: rgba(0, 0, 0, 0);
	}
	h1 {
		font-family: 'Beleren Small Caps';
		font-size: 48px;
		margin: 24px 0;
	}
	h2 {
		font-family: 'Beleren';
		font-size: 30px;
		margin: 15px 0;
	}
</style>
<body>
	'''
	
	#F: /resources/snippets/header.txt
	with open(os.path.join('resources', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
	<div class="banner">
		<div class="banner-container">
			<div class="set-banner" id="set-banner">
				<img class="set-logo" src="/sets/''' + code + '''-files/icon.png">
				<div class="set-title">''' + set_name + '''</div>'''

	#F: sets/SET-files/SET-draft.txt
	if os.path.exists(os.path.join('sets', code + '-files', code + '-draft.txt')):
		html_content += '''<a href="/sets/''' + code + '''-files/''' + code + '''-draft.txt" download>Draft me!</a>
		'''

	html_content += '''
			</div>
			<div class="select-text">Cards displayed as<select name="display" id="display"><option value="cards-only">Cards Only</option><option value="cards-text">Cards + Text</option></select>sorted by<select name="sort-by" id="sort-by"><option value="set-code">Set Number</option><option value="name">Name</option><option value="mv">Mana Value</option><option value="color">Color</option><option value="rarity">Rarity</option></select> : <select name="sort-order" id="sort-order"><option value="ascending">Asc</option><option value="descending">Desc</option></select></div>
		</div>
	</div>

	<div class="button-container" id="buttons">
		<button style="border-right: 1px solid #171717;" onclick="switchView('splash')" id="splash-button">Splash</button><button onclick="switchView('cards')"id="cards-button">Cards</button>
	</div>

	<div class="splash-container" id="splash">
	'''

	splashpath = os.path.join('sets', code + '-files', 'splash.md')
	if os.path.isfile(splashpath):
		with open(splashpath, 'r', encoding='utf-8') as md_file:
			md_content = md_file.read()

		md_html = markdown.markdown(md_content)

		img_re = r'%([^%]*)%'
		for img_name in re.findall(img_re, md_html):
			img_name_re = r'%' + img_name + '%'
			if img_name == 'logo' or img_name == 'icon':
				img_path = os.path.join('/sets', code + '-files', img_name + '.png')
			else:
				with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
					set_json = json.load(f)
				for card in set_json['cards']:
					if card['card_name'] == img_name:
						img_path = os.path.join('/sets', code + '-files', 'img', str(card['number']) + ('t' if 'token' in card['shape'] else '') + '_' + img_name + '.png')
						break
					img_path = 'missing'
			md_html = re.sub(img_name_re, img_path, md_html)
		html_content += md_html

	html_content +=	'''
	</div>

	<div class="grid-container" id="grid">
	</div>

	<div class="image-grid-container" id="imagesOnlyGrid">
	</div>

	<script>
		let card_list_arrayified = [];
		let set_list_arrayified = [];
		let specialchars = "";
		let displayStyle = "";

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

			for (let i = 0; i < card_list_arrayified.length; i++)
			{
				if (card_list_arrayified[i].set == "''' + code + '''")
				{
					set_list_arrayified.push(card_list_arrayified[i]);
				}
			}
			'''

	if os.path.isfile(splashpath):
		html_content += '''		switchView('splash');'''
	else:
		html_content += '''		buttons.style.display = 'none';
		setCardView();'''

	html_content += '''
		});

		document.getElementById("sort-by").onchange = displayChangeListener;
		document.getElementById("display").onchange = displayChangeListener;
		document.getElementById("sort-order").onchange = displayChangeListener;
  
		function displayChangeListener() {
			setCardView();
		}

		function switchView(view) {
			if (view == "splash")
			{
				splash.style.display = '';
				imagesOnlyGrid.style.display = 'none';
				grid.style.display = 'none';
			}
			else if (view == "cards")
			{
				setCardView();
			}

			document.getElementById("splash-button").disabled = (view == "splash");
			document.getElementById("cards-button").disabled = (view == "cards");
		}

		function setCardView() {
			displayStyle = document.getElementById("display").value;

			splash.style.display = 'none';
			imagesOnlyGrid.style.display = displayStyle == "cards-only" ? '' : 'none';
			grid.style.display = displayStyle == "cards-only" ? 'none' : '';

			updatePageContents();
		}

		function updatePageContents() {
			if (displayStyle == "cards-only")
			{
				cardGrid = document.getElementById("imagesOnlyGrid");
			}
			else
			{
				cardGrid = document.getElementById("grid");
			}

			let set_cards = [];
			let set_tokens_basics = [];

			for (const card of set_list_arrayified)
			{
				if (card.shape.includes("token") || card.type.includes("Basic"))
				{
					set_tokens_basics.push(card);
				}
				else
				{
					set_cards.push(card);
				}
			}

			set_cards.sort(compareFunction);
			set_tokens_basics.sort(compareFunction);
			if (document.getElementById("sort-order").value == "descending")
			{
				set_cards.reverse();
				set_tokens_basics.reverse();
			}
			set_list_sorted = set_cards.concat(set_tokens_basics);
			cardGrid.innerHTML = "";

			for (const card of set_list_sorted)
			{
				cardGrid.append(gridifyCard(card));
			}
		}

		'''

	#F: /resources/snippets/compare-function.txt
	#F: this is where compareFunction is from
	with open(os.path.join('resources', 'snippets', 'compare-function.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		'''

	#F: /resources/snippets/tokenize-symbolize.txt
	#F: this holds the isDecimal function used in compare-function.txt, as well as something for encoding/decoding symbols
	with open(os.path.join('resources', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet
	
	html_content += '''

		function gridifyCard(card_stats, card_text = false, rotate_card = false, designer_notes = false) {
			const card_name = card_stats.card_name;

			if (displayStyle == "cards-only")
			{
				return buildImgContainer(card_stats, true, rotate_card);
			}

		'''

	#F: /resources/snippets/img-container-defs.txt
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
			const url = new URL('search', window.location.origin);
			url.searchParams.append('search', document.getElementById("search").value);
			window.location.href = url;
		}

		'''

	#F: resources/snippets/random-card.txt
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

	print(f"HTML file saved as {output_html_file}")