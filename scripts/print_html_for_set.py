import os
import sys
import json
import markdown
import re

#F = Fungustober's notes
#C = Codex's notes

def generateHTML(code):
	#F: /sets/SET.html
	output_html_file = "sets/" + code + ".html"
	previewing = os.path.exists(os.path.join('sets', code + '-files', 'previewed.txt'))
	
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
  <link rel="stylesheet" href="/resources/card-text.css">
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
		gap: 20px;
		align-items: center;
		margin: auto;
	}
	.set-banner {
		font-family: Beleren;
		display: flex;
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
		width: 60px;
		padding-right: 12px;
	}
	.set-banner a {
		font-size: 18px;
		color: #1338be;
		text-decoration: none;
	}
	.set-banner a:hover {
		color: #0492c2;
	}
	.select-text {
		display: ''' + ('none' if previewing else 'flex') + ''';
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
		display: none;
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
		padding-bottom: 20px;
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
		font-size: 36px;
		font-family: 'Beleren';
		color: #535353;
	}
	.small-caps {
		font-family: 'Beleren Small Caps';
		font-size: 46px;
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
	.overlay {
		position: absolute;
	    top: 50%;
	    left: 50%;
	    margin-right: -50%;
	    transform: translate(-50%, -50%);
	    height: 90%;
	    width: 90%;
		max-width: 1000px;
		background-color: #e3e3e3;
		border: 2px solid #171717;
		border-radius: 20px;
		display: none;
	}
	.overlay-title {
		font-family: 'Beleren';
		font-size: 34px;
	}
	.close-btn {
		background: url('/img/close.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 50px;
		height: 50px;
		border: none;
		cursor: pointer;
	}
	.copy-btn {
		background: url('/img/copy.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 50px;
		height: 50px;
		border: none;
		cursor: pointer;
	}
	.canvas {
		max-width: 95%;
		max-height: 95%;
		width: auto;
		height: auto;
		display: flex;
		justify-self: center;
	}
	.overlay-header {
		display: grid;
		height: 7%;
		grid-template-columns: 2fr 18fr 1fr 1fr;
		gap: 10px;
		padding: 1%;
		justify-self: center;
		justify-items: center;
		align-items: center;
	}
	.canvas-container {
		height: 89%;
		align-content: center;
		padding-bottom: 1%;
	}
	.extras-container {
		padding-left: 4px;
		display: flex;
		align-items: center;
	}
	.dot {
		font-family: 'Helvetica', 'Arial';
		white-space: pre;
	}
	a {
		cursor: pointer;
	}
	p {
		width: 100%;
	}
	p img {
		display: block;
		margin: auto;
	}
</style>
<body>
	'''
	
	#F: /resources/snippets/header.txt
	with open(os.path.join('scripts', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
	<div class="banner">
		<div class="banner-container">
			<div class="set-banner" id="set-banner">
				<img class="set-logo" src="/sets/''' + code + '''-files/icon.png">
				<div class="banner-text">
					<div class="set-title">''' + set_name + '''</div>
					<div class="extras-container">'''

	#F: sets/SET-files/SET-draft.txt
	if os.path.exists(os.path.join('sets', code + '-files', code + '-draft.txt')) and not previewing:
		html_content += '''<a href="/sets/''' + code + '''-files/''' + code + '''-draft.txt" download>Draft</a><div class="dot"> • </div>
			<a onclick="packOnePickOne()">P1P1</a><div class="dot"> • </div>
'''

	#C: sets/SET-files/SET.xml
		if os.path.exists(os.path.join('sets', code + '-files', code + '.xml')) and not previewing:
			html_content += '''<a href="/sets/''' + code + '''-files/''' + code + '''.xml" download>Play</a><div class="dot"> • </div>
'''

	html_content += '''			<a onclick="randomSetCard()">I'm Feeling Lucky</a>
				</div>
			</div>
		</div>
'''

	html_content += '''
			<div class="select-text">Cards displayed as<select name="display" id="display"><option value="cards-only">Cards Only</option><option value="cards-text">Cards + Text</option></select>sorted by<select name="sort-by" id="sort-by"><option value="set-code">Set Number</option><option value="name">Name</option><option value="mv">Mana Value</option><option value="color">Color</option><option value="rarity">Rarity</option><option value="cube">Cube</option></select> : <select name="sort-order" id="sort-order"><option value="ascending">Asc</option><option value="descending">Desc</option></select></div>
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
			if img_name == 'logo' or img_name == 'icon' or img_name == 'bg':
				img_path = '/'.join([ '/sets', code + '-files', img_name + '.png' ])
			else:
				with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
					set_json = json.load(f)
				for card in set_json['cards']:
					if card['card_name'] == img_name:
						if 'image_name' in set_json and set_json['image_name'] == 'position':
							img_path = '/'.join([ '/sets', code + '-files', 'img', card['position'] + '.png' ])
						else:
							img_path = '/'.join([ '/sets', code + '-files', 'img', str(card['number']) + ('t' if 'token' in card['shape'] else '') + '_' + img_name + '.png' ])
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

	<div class="overlay" id="p1p1">
		<div class="overlay-header">
			<div></div> <!-- empty div for spacing -->
			<div class="overlay-title">Pack 1, Pick 1</div>
			<button class="copy-btn" onclick="copyP1P1()"></button>
			<button class="close-btn" onclick="closeP1P1()"></button>
		</div>
		<div class="canvas-container">
			<canvas id="canvas" class="canvas"></canvas>
		</div>
	</div>

	<script>
		let card_list_arrayified = [];
		let set_list_arrayified = [];
		let specialchars = "";
		let displayStyle = "";
		let p1p1cards = [];

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('scripts', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

			await fetch('/sets/''' + code + '''-files/''' + code + '''-draft.txt')
				.then(response => response.text())
				.then(text => {
					draft_file = text.replace(/},\\n\\t]/g, '}\\n\\t]');
			}).catch(error => console.error('Error:', error));

			draftmancerToP1P1(draft_file);
      
			for (let i = 0; i < card_list_arrayified.length; i++)
			{
				if (card_list_arrayified[i].set == "''' + code + '''")
				{
					set_list_arrayified.push(card_list_arrayified[i]);
				}
			}
			'''

	if os.path.isfile(splashpath):
		html_content += '''		buttons.style.display = 'grid';
				switchView('splash');'''
	else:
		html_content += '''
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
			cardGrid.innerHTML = "";

			if (''' + str(previewing).lower() + ''')
			{
				let text1 = document.createElement("div");
				let text2 = document.createElement("div");
				
				text1.innerText = "Currently Previewing";
				text2.innerText = "check back soon";

				text1.className = "small-caps";

				cardGrid.appendChild(text1);
				cardGrid.appendChild(text2);
				cardGrid.style.gridTemplateColumns = "1fr";
			}
			else
			{
				let set_cards = [];
				let set_basics = [];
				let set_tokens = [];
				let set_mp = [];

				for (const card of set_list_arrayified)
				{
					if (card.rarity.includes("masterpiece"))
					{
						set_mp.push(card);
					}
					else if (card.shape.includes("token"))
					{
						set_tokens.push(card);
					}
					else if (card.type.includes("Basic"))
					{
						set_basics.push(card);
					}
					else
					{
						set_cards.push(card);
					}
				}

				set_cards.sort(compareFunction);
				set_basics.sort(compareFunction);
				set_tokens.sort(compareFunction);
				set_mp.sort(compareFunction);
				if (document.getElementById("sort-order").value == "descending")
				{
					set_cards.reverse();
					set_basics.reverse();
					set_tokens.reverse();
					set_mp.reverse();
				}
				set_list_sorted = set_cards.concat(set_basics).concat(set_tokens).concat(set_mp);
				cardGrid.innerHTML = "";

				for (const card of set_list_sorted)
				{
					cardGrid.append(gridifyCard(card));
				}
			}
		}

		function draftmancerToP1P1(draft_file) { // comments in here by aanginer
			let draft_slots = {};
			let p1p1_object = [];
			let result_json = [];
			let card_map    = {};
			let current_slot_index = 0;
			let slot_indexes = {};
			let card_images = [];
			let mapping = true;

			const draft_headers = draft_file.matchAll(/\\[(.*?)\\]/g); // match text between [ and ]
			for (const result of draft_headers) {
				if (result[1] == "CustomCards")
					continue; // skip the CustomCards header

				if (mapping)
				{
					draft_json = JSON.parse(draft_file.substring(15, draft_file.indexOf(result[1]) - 1));

					for (const card of draft_json)
					{
						card_images.push({
							name: card.name,
							url: card.image_uris.en
						});
					}

					mapping = false;
				}

				const copies = parseInt(result[0].match(/\\((.*?)\\)/g)[0].split("(")[1].split(")")[0]); // match text between ( and ) -- do the split thing bc js regex doesnt let me grab the group for some reason????????
				// -- this is useless but if needed, const name = result.groups[0].match(/\\[(.*)\\(/g); // match text before (
				draft_slots[result[0]] = copies;
				slot_indexes[result[0]] = current_slot_index;
				current_slot_index += copies;
			}

			for (let i = 0; i < current_slot_index; i++) { // the current index should be the total number
				p1p1_object.push([]);
			}

			draft_slots["EOF"] = 0; // add this so when we check for the next slot in the final one we don't get an index error
			for (let i = 0; i < Object.keys(draft_slots).length - 1; i++) {
				const draft_slot = Object.keys(draft_slots)[i];
				const next_slot  = Object.keys(draft_slots)[i + 1];
				const slot_size  = draft_slots[draft_slot];

				let card_lines = draft_file.split(draft_slot)[1].split(next_slot)[0].split("\\n"); // split between the 2 slots -- splitting by EOF shouldnt be a problem as thatll yield a 1 element list

				for (const line of card_lines) {
					const count = parseInt(line.substring(0, line.indexOf(' ')));
					const card_name = line.substring(line.indexOf(' ') + 1).trim();

					if (!card_map[card_name]) {
						card_map[card_name] = {};
					}

					card_map[card_name][draft_slot] = card_map[card_name][draft_slot] ? card_map[card_name][draft_slot] + count : count; // fancy way to do a null check to decide between = and +=
				}
			}

			for (const card of card_images) { // grab the needed card data
				if (Object.keys(card_map).includes(card.name)) {
					const card_slots = card_map[card.name];
					for (const slot in card_slots) {
						const slot_copies = draft_slots[slot];
						for (let i = 0; i < slot_copies; i++) {
							for (let j = 0; j < card_slots[slot]; j++) {
								p1p1_object[slot_indexes[slot] + i].push(card);
							}
						}
					}
				}
			}

			p1p1_cards = p1p1_object;
		}


		function packOnePickOne() {
			img_list = [];
			used_cards = [];
			for (const slot of p1p1_cards)
			{
				if (slot.length == 0) 
					continue;

				do {
					rand_i = Math.floor(Math.random() * (slot.length));
					card = slot[rand_i];
				} while (used_cards.includes(card));

				const img_url = card.url;

				const image = new Image();
				image.src = img_url;

				img_list.push(image);
				used_cards.push(card);
			}

			const canvas = document.getElementById("canvas");
			const ctx = canvas.getContext('2d');

			canvas.width = 1883;
			canvas.height = 1573;

			for (let i = 0; i < img_list.length; i++)
			{
				img_list[i].onload = function() {
					x_offset = 377 * (i % 5);
					y_offset = 525 * Math.floor(i / 5);
					ctx.drawImage(img_list[i], x_offset, y_offset, 375, 523);
				};
			}

			document.getElementById("p1p1").style.display = "block";
		}

		async function copyP1P1() {
			const canvas = document.getElementById("canvas");

			canvas.toBlob(async (blob) => {
				if (!blob) {
					console.error('Failed to create Blob from canvas.');
					return;
				}

				try {
					const item = new ClipboardItem({ [blob.type]: blob });
					await navigator.clipboard.write([item]);
				} catch (err) {
					console.error('Failed to copy canvas image:', err);
				}
			}, 'image/png');
		}

		function closeP1P1() {
			document.getElementById("p1p1").style.display = "none";
		}

		'''

	#F: /resources/snippets/compare-function.txt
	#F: this is where compareFunction is from
	with open(os.path.join('scripts', 'snippets', 'compare-function.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		'''

	#F: /resources/snippets/tokenize-symbolize.txt
	#F: this holds the isDecimal function used in compare-function.txt, as well as something for encoding/decoding symbols
	with open(os.path.join('scripts', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
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
	with open(os.path.join('scripts', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
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

		function randomSetCard() {
			let set_card_list = [];
			for (card of card_list_arrayified)
			{
				if (card.set == "''' + code + '''")
				{
					set_card_list.push(card);
				}
			}
			let i = Math.floor(Math.random() * (set_card_list.length + 1));
			let random_card = set_card_list[i];

			const url = new URL('card', window.location.origin);
			const params = {
				set: random_card.set,
				num: random_card.number,
				name: random_card.card_name
			}
			for (const key in params) {
				url.searchParams.append(key, params[key]);
			}

			window.location.href = url;
		}

		'''

	#F: resources/snippets/random-card.txt
	with open(os.path.join('scripts', 'snippets', 'random-card.txt'), encoding='utf-8-sig') as f:
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
