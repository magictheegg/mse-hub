import os
import sys
import json

def generateHTML():
	output_html_file = "index.html"

	# Start creating the HTML file content
	html_content = '''<html>
	<head>
		<title>MSE Set Hub</title>
		<link rel="icon" type="image/x-icon" href="/img/favicon.png">
		<meta name="viewport" content="width=device-width, initial-scale=1.0">
	</head>
	<style>
	@font-face {
	  font-family: 'Beleren Small Caps';
	  src: url('/resources/beleren-caps.ttf');
	}
	body {
		background-image: linear-gradient(to top, #ffdde1, #ee9ca7);
		background-attachment: fixed;
		overscroll-behavior: none;
		font-family: 'Helvetica', 'Arial', sans-serif;
		display: grid;
	}
	.selects {
		position: absolute;
	}
	.item-container {
		height: auto;
		display: grid;
		justify-self: center;
		align-self: center;
	}
	.item-container .banner {
		max-width: 500px;
		max-height: 200px;
		display: block;
		margin: auto;
		padding-bottom: 20px;
	}
	select {
		position: absolute;
		text-align: center;
		font-family: -apple-system, system-ui, "Segoe UI", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
		font-weight: 500;
		cursor: pointer;
		background-color: #F3F3F3;
	}
	input {
		width: 100%;
		max-width: 700px;
		margin: auto;
		height: 50px;
		font-size: 24px;
		color: #171717;
		background-color: #f3f3f3;
		border: 1px solid #d9d9d9;
		border-radius: 2px;
		padding-left: 10px;
		padding-right: 10px;
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
	}
	input:focus {
		outline-color: #171717;
	}
	.two-part-grid {
		width: 100%;
		max-width: 700px;
		margin: auto;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 20px;
		justify-items: center;
	}
	.two-part-grid p {
		width: 100%;
		text-align: center;
		padding-bottom: 8px;
		font-size: 24px;
		font-weight: bolder;
		font-family: 'Georgia';
		margin: 0;
	}
	.container p {
		padding: 11px 0px;
	}
	.preview-container {
		display: grid;
		grid-template-columns: repeat(3, 1fr);
		gap: 2px;
		justify-items: center;
		align-items: center;
		padding-bottom: 10px;
	}
	.set-group {
		font-family: Beleren Small Caps;
		font-size: 18px;
		width: 100%;
		margin-bottom: 10px;
		border-bottom: 2px solid #171717;
	}
	.button-grid {
		display: grid;
		margin: auto;
		grid-template-columns: repeat(4, 1fr);
		gap: 20px;
		padding-top: 10px;
		padding-bottom: 20px;
	}
	.button-grid button {
		background-color: #171717;
		border: none;
		color: #f3f3f3;
		border-radius: 5px;
		cursor: pointer;
		font-size: 15px;
		width: 150px;
		height: 35px;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 5px;
	}
	button:hover {
		background-color: #000000;
		border: 1px solid #f3f3f3;
	}
	.btn-img {
		width: 24px;
	}
	.container {
		height: fit-content;
		align-self: center;
	}
	.card-container {
		background: #f3f3f3;
		width: 90%;
		border: 1px solid #d5d9d9;
		border-top: 3px solid #171717;
		border-bottom: 3px solid #171717;
		border-radius: 6px;
		display: grid;
		justify-items: center;
		gap: 8px;
		padding-top: 8px;
		padding-bottom: 8px;
		height: fit-content;
	}
	.card-container p {
		border-bottom: 1px solid #898989;
	}
	.card-container a {
		width: 70%;
	}
	.card-container img {
		width: 100%;
		display: block;
		margin: auto;
	}
	.set-icon-container {
		font-family: 'Beleren Small Caps';
		font-size: 12px;
		text-align: center;
		display: grid;
		justify-items: center;
		align-items: center;
		gap: 2px;
		width: 100%;
		height: 100%;
	}
	.set-icon-container a {
		text-decoration: none;
		color: #171717;
		height: 100%;
	}
	.set-icon {
		height: 60px;
		display: grid;
		align-items: center;
		justify-items: center;
	}
	.set-icon img {
		width: 60px;
	}
	.set-icon-name {
		min-height: 30px;
		height: 100%;
	}
	@media ( max-width: 750px ) {
		.item-container {
			width: 95%;	
		}
		.search-grid {
			width: 95%;
		}
		.two-part-grid p {
			font-size: 18px;
		}
	}
	</style>
	<body>
		<div class="selects" id="selects">
			<select id="color-select" onchange="setGradient()">
			</select>
		</div>
		<div class="item-container">
			<img class="banner" src="img/banner.png"></img>
			<input type="text" inputmode="search" placeholder="Search ..." autofocus="autofocus" name="search" id="search" spellcheck="false" autocomplete="off" autocorrext="off" spellcheck="false">
			<div class="button-grid">
				<button onclick="goToSets()"><img src="/img/sets.png" class="btn-img">All Sets</button>
				<button onclick="goToDeckbuilder()"><img src="/img/deck.png" class="btn-img">Deckbuilder</button>
				<button onclick="randomCard()"><img src="/img/random.png" class="btn-img">Random Card</button>
				<button onclick="playOnCgs()"><img src="/img/cgs.png" class="btn-img">Play on CGS</button>
			</div>
			<div class="two-part-grid">
				<div class="container" id="preview-container">
					<p>Preview Galleries</p>
					'''

	with open(os.path.join('lists', 'set-order.json'), encoding='utf-8-sig') as j:
		so_json = json.load(j)

	for key in so_json:
		html_content += '''					<div class="set-group">''' + key + '''</div>
		'''
		html_content += '''					<div class="preview-container">
		'''
		set_codes = so_json[key]
		for code in set_codes:
			set_name = 'MISSING'
			if not os.path.exists(os.path.join('sets', code + '-files', 'ignore.txt')):
				with open(os.path.join('lists', 'all-sets.json'), encoding='utf-8-sig') as f:
					data = json.load(f)
					for s in data['sets']:
						if s['set_code'] == code:
							set_name = s['set_name']
							break

				html_content += '''<div class="set-icon-container">
									<a href="previews/''' + code + '''"><div class="set-icon"><img src="sets/''' + code + '''-files/icon.png" title="''' + set_name + '''"></img></div>
									<div class="set-icon-name">''' + set_name + '''</div></a>
								</div>
				'''
		html_content += '''					</div>
		'''
	
	html_content += '''
				</div>
				<div class="card-container" id="cotd-image">
					<p>Card of the Day</p>
				</div>
			</div>
		</div>
		<script>
			const delay = ms => new Promise(res => setTimeout(res, ms));
			let gradients = [];
			let card_list_arrayified = [];
			let specialchars = "";

			document.addEventListener("DOMContentLoaded", async function () {
				try {
					const response = await fetch('./resources/gradients.json');
					raw_gradients = await response.json();
				}
				catch(error) {
					console.error('Error:', error);
				}

				gradients = raw_gradients.gradients;
				prepareGradients();

				'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet
	
	html_content += '''
				card_list_cleaned = [];

				for (const card of card_list_arrayified)
				{
					let card_stats = [];

					for (var key in card)
					{
						if (isNaN(card[key]))
						{
							card_stats[key] = card[key].toLowerCase();
						}
						else
						{
							card_stats[key] = card[key];
						}
					}

					if (!card_stats.shape.includes("token") && !card_stats.type.includes("basic"))
					{
						card_list_cleaned.push(card);
					}
				}

				const cotd = reallyRand(card_list_cleaned.length);
				const card_stats = card_list_cleaned[cotd];

				const a = document.createElement("a");

				const url = new URL('card', window.location.origin);
				const params = {
					set: card_stats.set,
					num: card_stats.number,
					name: card_stats.card_name
				}
				for (const key in params) {
					url.searchParams.append(key, params[key]);
				}
				a.href = url;

				const img = document.createElement("img");
				img.id = "cotd";


				img.src = '/sets/' + card_stats.set + '-files/img/' + card_stats.number + '_' + card_stats.card_name + (card_stats.shape.includes('double') ? '_front' : '') + '.' + card_stats.image_type;

				a.append(img);
				document.getElementById("cotd-image").append(a);

				do {
					await delay(100);
				}
				while (!isImageOk(document.getElementById("cotd")));
				document.getElementById("preview-container").style.height = document.getElementById("cotd-image").offsetHeight;
			});

			document.getElementById("search").addEventListener("keypress", function(event) {
				if (event.key === "Enter") {
					event.preventDefault();
					search();
				}
			});

			window.addEventListener('resize', function(event) {
				document.getElementById("preview-container").style.height = document.getElementById("cotd-image").offsetHeight;
			}, true);

			function isImageOk(img) {
				if (!img.complete || img.naturalWidth == 0) {
					return false;
				}

				return true;
			}

			// if this doesn't work, blame Gemini
			function reallyRand(x) {
				const date = new Date();
				const seed = date.getFullYear() * 10000 + 
							 date.getMonth() * 100 + 
							 date.getDate();

				const a = 1103515245;
				const c = 12345;
				const m = Math.pow(2, 31);

				let randomNumber = (a * seed + c) % m;
				randomNumber = randomNumber / m;

				return Math.floor(randomNumber * x);
			}

			function prepareGradients() {
				for (const gradient of gradients)
				{
					const opt = document.createElement("option");
					opt.value = gradient.name.replace(' ', '-');
					opt.text = gradient.name;
					document.getElementById("color-select").appendChild(opt);
				}

				setGradient();
			}

			function setGradient() {
				gradient = document.getElementById("color-select").value;

				gradTop = "#000000";
				gradBottom = "#FFFFFF";
				for (const grad of gradients)
				{
					if (gradient == grad.name.replace(' ', '-'))
					{
						gradTop = grad.color1;
						gradBottom = grad.color2;
					}
				}

				document.body.style.backgroundImage = `linear-gradient(to bottom, ${gradTop}, ${gradBottom})`;
			}

			function goToSets() {
				window.location = ("/all-sets");
			}

			function goToDeckbuilder() {
				window.location = ("/deckbuilder");
			}

			function playOnCgs() {
				window.location = ("/play");
			}

			function search() {
				const url = new URL('search', window.location.origin);
				url.searchParams.append('search', document.getElementById("search").value);
				window.location.href = url;
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

	print(f"HTML file saved as {output_html_file}")
