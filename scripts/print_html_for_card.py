import os
import sys
import json

#F = Fungustober's notes

def generateHTML():
	output_html_file = "card.html"
	
	# Start creating the HTML file content
	html_content = '''<html>
<head>
	<title>Card</title>
	<link rel="icon" type="image/x-icon" href="/img/favicon.png">
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
	.designer-notes {
		padding-top: 10px;
		border-top: 1px solid #171717;
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
		snippet = f.read()
		html_content += snippet

	html_content += '''

	<input type="text" id="display" class="hidden" value="cards-and-text"> <!-- here to make img-container-defs snippet work properly -->
	<div class="banner-container">
		<a class="set-banner" id="set-banner">
			<img class="set-logo" id="set-banner-logo">
			<div class="set-title" id="set-banner-title"></div>
		</a>
	</div>

	<div class="grid-container" id="grid">
	</div>

	<script>
		let card_list_arrayified = [];
		let specialchars = "";

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet
	
	html_content += '''
			await fetch('/lists/all-sets.json')
					.then(response => response.json())
					.then(json => {
						set_list = json;
				}).catch(error => console.error('Error:', error));

			const params = new URLSearchParams(window.location.search);

			const set = params.get('set');
			const num = params.get('num');
			const name = params.get('name');

			for (const c of card_list_arrayified)
			{
				if (c.card_name == name && c.set == set && c.number == num)
				{
					card = c;
					break;
				}
			}

			var link = document.querySelector("link[rel~='icon']");
			link.href = '/sets/' + set + '-files/icon.png';

			document.title = name;

			const banner = document.getElementById("set-banner");
			const banner_logo = document.getElementById("set-banner-logo");
			const banner_title = document.getElementById("set-banner-title");

			banner.href = '/sets/' + set;
			banner_logo.src = '/sets/' + set + '-files/icon.png';

			for (const set_stats of set_list.sets)
			{
				if (set_stats.set_code == set)
				{
					banner_title.innerHTML = set_stats.set_name;
					break;
				}
			}			

			document.getElementById("grid").appendChild(gridifyCard(card, false, true));


			other_printings = [];
			for (const c of card_list_arrayified)
			{
				if (c.card_name == card.card_name && c.type == card.type && !c.shape.includes("Token") && (c.set != card.set || c.number != card.number))
				{
					other_printings.push(c);
				}
			}

			if (other_printings.length > 0)
			{
				const printings = document.createElement("div");
				printings.className = "printings";
				printings.id = "other-printings";
				printings.innerText = "Other Printings: ";

				for (let i = 0; i < other_printings.length; i++)
				{
					const printing = other_printings[i];
					const setlink = document.createElement("a");
					setlink.innerText = printing.set;

					const url = new URL('card', window.location.origin);
					const params = {
						set: printing.set,
						num: printing.number,
						name: printing.card_name
					}
					for (const key in params) {
						url.searchParams.append(key, params[key]);
					}
					setlink.href = url;

					printings.appendChild(setlink);

					if (i != other_printings.length - 1)
					{
						const dot = document.createElement("text");
						dot.innerText = " • ";
						printings.appendChild(dot);
					}
				}

				document.getElementById("card-text").appendChild(printings);
				document.getElementById("other-printings").style.display = "block";
			}
		});

		'''
	
	with open(os.path.join('resources', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function gridifyCard(card_stats, card_text = false, rotate_card = false, designer_notes = true) {
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
