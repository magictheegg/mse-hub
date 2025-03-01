import os
import sys
import json

def generateHTML():
	output_html_file = "all-sets.html"

	# Start creating the HTML file content
	html_content = '''<html>
	<head>
	  <title>All Sets</title>
	  <link rel="icon" type="image/x-icon" href="/img/sets.png">
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
			font-size: 20px;
			padding-bottom: 30px;
		}
		a {
			text-decoration: none;
			color: #171717;
		}
		.set-table {
			width: 60%;
			max-width: 1000px;
			display: grid;
			grid-template-columns: 1fr;
			padding-top: 20px;
			margin: auto;
		}
		.set-header-row {
			width: 100%;
			display: grid;
			grid-template-columns: 0.5fr 2.5fr 0.5fr 0.5fr;
			gap: 5px;
			font-weight: bold;
			padding-bottom: 10px;
		}
		.set-row {
			height: 6em;
			width: 100%;
			display: grid;
			grid-template-columns: 0.5fr 2.5fr 0.5fr 0.5fr;
			gap: 5px;
			align-items: center;
			border-top: 1px solid #171717;
		}
		.set-row:hover {
			background-color: #fafafa;
		}
		.set-row:nth-child(2n) {
		  background-color: #dedede;
		}
		.set-row:nth-child(2n):hover {
			background-color: #e6e6e6;
		}
		.set-row img {
			width: 70%;
			justify-self: center;
		}
		.set-title {
			font-family: Beleren;
			letter-spacing: .02em;
			font-size: 22px;
		}
		.set-group {
			font-family: Beleren Small Caps;
			text-align: center;
			font-size: 40px;
			padding-top: 20px;
		}
	</style>
	<body>
		'''

	with open(os.path.join('resources', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	with open(os.path.join('lists', 'set-order.json'), encoding='utf-8-sig') as j:
		so_json = json.load(j)

	for key in so_json:
		html_content += '''			<div class="set-group">''' + key + '''</div>
		'''

		html_content += '''
			<div class="set-table">
			<div class="set-header-row">
				<div></div> <!-- empty div for spacing -->
				<div>NAME</div>
				<div>CODE</div>
				<div>CARDS</div>
			</div>
		'''

		set_codes = so_json[key]
		for code in set_codes:
			set_name = 'MISSING'
			with open(os.path.join('lists', 'all-sets.json'), encoding='utf-8-sig') as f:
				data = json.load(f)
				for s in data['sets']:
					if s['set_code'] == code:
						set_name = s['set_name']
						break
					set_name = 'MISSING'

			with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as f:
				data = json.load(f)
				set_count = 0
				for entry in data['cards']:
					if 'token' not in entry['shape'] and 'Basic' not in entry['type']:
						set_count += 1

			html_content += '''
			<a href="/sets/''' + code + '''" class="set-row"> 
				<img src="/sets/''' + code + '''-files/icon.png">
				<div class="set-title">''' + set_name + '''</div>
				<div>''' + code + '''</div>
				<div>''' + str(set_count) + '''</div>
			</a>
			'''

		html_content += '''</div>
		'''

	html_content += '''
	<script>
		let card_list_arrayified = [];
		let specialchars = "";
		let displayStyle = "";

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
		});

		function isDecimal(char) {
			return char >= '0' && char <= '9';
		}

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

	print(f"HTML file saved as {output_html_file}")