import os
import sys
import json

def generateHTML(codes):
	output_html_file = "deckbuilder.html"

	with open(os.path.join('resources', 'site-config.json'), encoding='utf-8-sig') as f:
		config = json.load(f)
		base_url = config.get('base_url', '')
		hub_name = base_url.split('https://')[1].split('.github.io')[0].lower() if 'https://' in base_url else 'unknown'

	# Start creating the HTML file content
	html_content = '''<html>
<head>
	<title>Deckbuilder</title>
	<link rel="icon" type="image/x-icon" href="./img/deckbuilder.png">
	<link rel="stylesheet" href="./resources/mana.css">
	<link rel="stylesheet" href="./resources/header.css">
	<link rel="stylesheet" href="./resources/card-text.css">
	<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<script title="root">
	const rootPath = ".";
	const SUPABASE_URL = 'https://mtjkkvtcmejzcpjmropd.supabase.co';
	const SUPABASE_KEY = 'sb_publishable_Hgyr2JJRsJRa1pYwoz-ijQ_ozfwnp9t';
	const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
	const hubName = "''' + hub_name + '''";

	function generateShortId(length = 10) {
		const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
		let result = '';
		for (let i = 0; i < length; i++) {
			result += chars.charAt(Math.floor(Math.random() * chars.length));
		}
		return result;
	}
</script>
<style>
	@font-face {
		font-family: Beleren;
		src: url('./resources/beleren.ttf');
	}
	@font-face {
		font-family: 'Gotham Narrow Medium';
		src: url('./resources/gotham-narrow-medium.otf');
	}
	body {
		font-family: 'Helvetica', 'Arial', sans-serif;
		overscroll-behavior: none;
		margin: 0px;
		background-color: #bbbbbb;
		display: block;
	}
	.page-container {
		width: 2000px;
		max-width: 98%;
		height: 89%;
		padding-top: 10px;
		display: grid;
		grid-template-columns: 3fr 2fr;
		margin: auto;
		gap: 5px;
	}
	.admin-only.hidden {
		display: none;
	}
	
	/* Admin Password Modal */
	#admin-modal-overlay {
		position: fixed;
		top: 0; left: 0; width: 100%; height: 100%;
		background: rgba(0,0,0,0.7);
		display: none;
		justify-content: center;
		align-items: center;
		z-index: 10000;
	}
	.admin-modal {
		background: white;
		padding: 30px;
		border-radius: 8px;
		width: 350px;
		box-shadow: 0 4px 15px rgba(0,0,0,0.3);
		text-align: center;
		position: relative;
	}
	.admin-modal-close {
		position: absolute;
		top: 10px;
		right: 15px;
		font-size: 24px;
		cursor: pointer;
		color: #888;
		line-height: 1;
	}
	.admin-modal-close:hover {
		color: #171717;
	}
	
	/* General Notification Modal */
	#notification-modal-overlay {
		position: fixed;
		top: 0; left: 0; width: 100%; height: 100%;
		background: rgba(0,0,0,0.5);
		display: none;
		justify-content: center;
		align-items: center;
		z-index: 11000;
	}
	.notification-modal {
		background: white;
		padding: 25px;
		border-radius: 8px;
		width: 320px;
		box-shadow: 0 4px 15px rgba(0,0,0,0.3);
		text-align: center;
	}
	.notification-modal p {
		margin-top: 5px;
		margin-bottom: 20px;
		font-size: 16px;
	}
	
	/* Selection Modal */
	#selection-modal-overlay {
		position: fixed;
		top: 0; left: 0; width: 100%; height: 100%;
		background: rgba(0,0,0,0.5);
		display: none;
		justify-content: center;
		align-items: center;
		z-index: 10500;
	}
	.selection-modal {
		background: white;
		padding: 25px;
		border-radius: 8px;
		width: 650px;
		height: 85vh;
		box-shadow: 0 4px 15px rgba(0,0,0,0.3);
		display: flex;
		flex-direction: column;
		position: relative;
	}
	.selection-chips {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
		gap: 15px;
		justify-content: center;
		margin: 20px 0;
		overflow-y: auto;
		padding: 5px;
	}
	.selection-chip {
		background: white;
		border: 1px solid #d5d9d9;
		border-radius: 8px;
		cursor: pointer;
		overflow: hidden;
		transition: transform 0.2s, box-shadow 0.2s;
		display: flex;
		flex-direction: column;
		height: 140px;
	}
	.selection-chip:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 10px rgba(0,0,0,0.1);
	}
	.selection-chip-image {
		height: 100px;
		width: 100%;
		background-size: 150%;
		background-position: center 20%;
		background-color: #eee;
	}
	.selection-chip-info {
		padding: 8px;
		text-align: left;
		display: flex;
		flex-direction: column;
		justify-content: center;
		flex-grow: 1;
		background: white;
	}
	.selection-chip-name {
		font-family: Beleren;
		font-size: 13px;
		margin: 0;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
		color: #171717;
	}
	.selection-chip-format {
		font-size: 11px;
		color: #666;
		font-style: italic;
		margin: 2px 0 0 0;
	}
	#selection-search {
		width: 100%;
		padding: 10px;
		margin-bottom: 10px;
		border: 1px solid #d5d9d9;
		border-radius: 4px;
		box-sizing: border-box;
		font-size: 16px;
	}
	#selection-title {
		margin-top: 0;
		font-family: Beleren;
		text-align: center;
	}
	
	.admin-modal p {
		margin-top: 0;
		margin-bottom: 15px;
		font-size: 18px;
	}
	#admin-verify-msg {
		font-size: 12px;
		margin-top: 20px;
		margin-bottom: 0px;
		color: #666;
		display: none;
	}
	.admin-modal input {
		width: 90%;
		padding: 10px;
		margin: 10px 0 20px 0;
		border: 1px solid #d5d9d9;
		border-radius: 4px;
		font-size: 16px;
	}
	.admin-modal-buttons {
		justify-self: center;
		width: 70%;
		display: flex;
		gap: 40px;
		justify-content: space-around;
	}
	.admin-btn {
		padding: 8px 20px;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		font-weight: bold;
		max-width: 86px;
	}
	.admin-btn.save { background: #171717; color: white; }
	.admin-btn.cancel { background: #e0e0e0; color: #333; }

	.deckbuilder-container {
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
		gap: 5px;
	}
	.search-results-container {
		display: grid;
		grid-template-columns: 3fr 2fr;
		overflow-y: hidden;
		overflow-x: hidden;
		height: 100%;
	}
	.gallery-column {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}
	.search-container {
		height: 100%;
		border: 1px solid #d5d9d9;
		border-top: 4px solid #171717;
		border-bottom: 4px solid #171717;
		background-color: #f3f3f3;
		border-radius: 6px;
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
	}
	.filter-bar {
		background-color: white;
		border-top: 1px solid #d5d9d9;
		padding: 5px 15px;
		display: flex;
		align-items: center;
		gap: 8px;
		font-size: 13px;
		min-height: 20px;
	}
	.filter-bar input[type="checkbox"] {
		width: auto;
		height: auto;
		margin: 0;
		cursor: pointer;
	}
	.deckbuilder-search-grid {
		width: 95%;
		max-width: 1200px;
		min-height: 36px;
		display: grid;
		grid-template-columns: 5fr 2fr 1fr;
		gap: 8px;
		padding: 5px 2.5%;
		border-bottom: 1px solid #898989;
		justify-items: center;
		align-items: center;
	}
	.search-row {
		display: grid;
		grid-template-columns: 3fr 1.5fr 1.5fr 1fr 3fr;
		gap: 5px;
		padding: 5px 10px;
		border-bottom: 1px solid #d5d9d9;
		cursor: pointer;
		font-size: 12px;
		align-items: center;
		width: 100%;
		box-sizing: border-box;
	}
	.search-row:hover {
		background-color: #e9e9e9;
	}
	.search-row div {
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}
	.search-row-header {
		font-weight: bold;
		background-color: #e0e0e0;
		position: sticky;
		top: 0;
		z-index: 1;
	}
	input {
		width: 100%;
		height: 35px;
		font-size: 16px;
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 2px;
		padding-left: 10px;
		padding-right: 10px;
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
	}
	input:focus {
		outline-color: #4f4f4f;
	}
	button {
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 8px;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		color: #171717;
		cursor: pointer;
		font-size: 13px;
		width: 100%;
		height: 35px;
		min-width: 85px;
	}
	button:hover {
		background-color: #ffffff;
	}
	button:focus {
		border-color: #171717;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		outline: 0;
	}
	button:disabled, select:disabled {
		cursor: auto;
		background-color: #f7fafa;
		font-style: italic;
		box-shadow: none;
		color: #cccccc;
	}
	.deckbuilder-search-grid .select-text {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: left;
		gap: 4px;
		font-size: 14.5px;
		text-align: center;
	}
	select {
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 8px;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		text-align: center;
		color: #171717;
		font-size: 13px;
		height: 30px;
	}
	select:focus {
		outline-color: #4f4f4f;
	}
	.search-image-grid-container {
		overflow-y: scroll;
		flex: 1;
	}
	.search-image-grid {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		width: 98%;
		gap: 3px;
		justify-items: center;
		padding: 1%;
	}
	.search-image-grid .img-container {
		width: 100%;
		min-height: 150px;
		aspect-ratio: 2.5 / 3.5;
	}
	@media ( max-width: 750px ) {
		.image-grid {
			grid-template-columns: 1fr 1fr;	
		}
	}
	.image-grid {
		display: flex;
		flex-direction: column;
		height: 100%;
	}
	.card-text {
		border-top: 3px solid #171717;
		overflow-y: scroll;
		scrollbar-width: none;
		height: 50%;
		padding: 10px 0;
	}
	.card-text div {
		font-size: 13px;
	}
	.card-text .name-cost {
		font-size: 16px;
	}
	.card-text .type {
		font-size: 14px;
	}
	.card-text br {
		content: "";
		display: block;
		margin-bottom: 5px;
	}
	.img-container {
		position: relative;
		align-self: center;
		text-align: center;
	}
	.img-container img {
		width: 100%;
		height: auto;
		border-radius: 3.733% / 2.677%;
	}
	.img-container .btn {
		background: url('./img/flip.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 15%;
		height: 11%;
		cursor: pointer;
		border: none;
		position: absolute;
		top: 6.5%;
		left: 8.5%;
		transform: translate(-50%, -85%);
		border-radius: 0px;
		box-shadow: none;
	}
	.img-container .btn:hover {
		background: url('./img/flip-hover.png') no-repeat;
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
	.card-grid-container {
		border-left: 1px solid #d5d9d9;
		width: 100%;
		height: 100%;
		overflow-y: hidden;
	}
	.card-grid-container .img-container {
		width: 100%;
		height: 50%;
		padding: 10px 0;
	}
	.img-container a {
		height: 100%;
		max-width: 80%;
		display: grid;
		justify-self: center;
	}
	.img-container a > * {
		grid-row: 1;
		grid-column: 1;
	}
	.card-grid-container img {
		width: auto;
		min-width: 0;
		max-width: 100%;
		height: auto;
		min-height: 0;
		max-height: 100%;
		display: block;
		margin: auto;
		border-radius: 3.733% / 2.677%;
	}
	.card-grid-container .btn {
		left: 50%;
		top: 48%;
		transform: translate(-50%, -50%);
		opacity: 0.5;
	}
	.hidden {
		display: none;
	}
	.no-cards-text {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 100%;
		text-align: center;
		font-style: italic;
		color: #494949;
	}
	.deck-container {
		height: 100%;
		border: 1px solid #d5d9d9;
		border-top: 4px solid #171717;
		border-bottom: 4px solid #171717;
		background-color: #f3f3f3;
		border-radius: 6px;
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
		position: relative;
	}
	.deck-info-grid {
		width: 95%;
		max-width: 1200px;
		min-height: 36px;
		display: grid;
		grid-template-columns: 1.5fr 1fr .65fr .75fr .75fr;
		gap: 6px;
		padding: 5px 2.5%;
		border-bottom: 1px solid #898989;
		justify-items: center;
		align-items: center;
	}
	.deck-info-grid select {
		width: 100%;
	}
	#search-display {
		width: 100%;
	}
	.deck-count {
		font-weight: bold;
	}
	.static-deck-container {
		height: 100%;
		overflow-y: hidden;
	}
	.deck-cards-container {
		display: grid;
		grid-template-columns: 1fr 1fr;
		overflow-y: scroll;
		scrollbar-width: none;
		font-size: 14px;
		height: 100%;
	}
	.deck-container span {
		font-size: 15px;
		font-weight: bold;
		padding-top: 10px;
		padding-bottom: 5px;
		padding-left: 22px;
	}
	.deck-container .icon {
		width: 60%;
	}
	.deck-section {
		display: none;
	}
	.deck-inner-section {
		padding-bottom: 10px;
		line-height: 1.5;
	}
	.deck-line {
		border-top: 1px solid #d5d9d9;
		display: grid;
		grid-template-columns: 1fr 1fr 13fr;
		gap: 5px;
		align-items: center;
	}
	.deck-col {
		padding: 0 15px;
		height: 100%;
	}
	.card-img-container {
		height: 2.1vw;
		max-height: 45px;
		display: grid;
		grid-template-columns: 1fr 1fr 2fr 12fr;
		gap: 2px;
		font-weight: bold;
		line-height: 1;
	}
	.card-img-container img {
		width: 100%;
		border-radius: 3.733% / 2.677%;
	}
	.card-fx {
		display: grid;
		align-items: center;
		justify-items: center;
		text-align: center;
	}
	.card-img-container .card-fx {
		height: 2.7vw;
		max-height: 63px;
	}
	.img-container .h-img {
		transform: rotateY(0deg) rotate(90deg);
		width: 85%;
		border-radius: 3.733% / 2.677%;
	}
	.rc-menu {
		display: none;
		position: absolute;
		background-color: #f3f3f3;
		border-top: 1px solid #d5d9d9;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		z-index: 2;
		font-size: 12px;
	}
	.rc-menu ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.rc-menu li {
		padding: 8px 12px;
		border: 1px solid #d5d9d9;
		border-top: none;
		cursor: pointer;
	}
	.rc-menu li:hover {
		background-color: #ffffff;
	}
	.search-grid {
		justify-content: center;
	}
	.sg-icon {
		cursor: pointer;
	}
</style>
<body>
	<div class="header">
		<div class="search-grid">
			<a onclick="window.location.href = rootPath + '/'"><img class="sg-logo" id="header-banner"></a>
			<img class="sg-icon" id="header-search" onclick="goToSearch()">
			<a onclick="window.location.href = rootPath + '/all-sets'"><img id="header-sets" class="sg-icon">Sets</a>
			<a id="header-articles-link" onclick="window.location.href = rootPath + '/all-articles'" style="display: none;"><img id="header-articles" class="sg-icon">Articles</a>
			<a id="header-decks-link" onclick="window.location.href = rootPath + '/decks'" style="display: none;"><img id="header-decks" class="sg-icon">Decks</a>
			<a onclick="window.location.href = rootPath + '/deckbuilder'"><img id="header-deckbuilder" class="sg-icon">Deckbuilder</a>
			<a onclick="randomCard()"><img id="header-random" class="sg-icon">Random</a>
		</div>
	</div>
	<script>
		document.addEventListener("DOMContentLoaded", function () {
			document.getElementById("header-banner").src = rootPath + "/img/banner.png";
			document.getElementById("header-search").src = rootPath + "/img/search.png";
			document.getElementById("header-sets").src = rootPath + "/img/sets.png";
			document.getElementById("header-articles").src = rootPath + "/img/articles.png";
			document.getElementById("header-decks").src = rootPath + "/img/deck.png";
			document.getElementById("header-deckbuilder").src = rootPath + "/img/deckbuilder.png";
			document.getElementById("header-random").src = rootPath + "/img/random.png";

			// Hide Articles if none exist
			fetch(rootPath + '/all-articles.html', { method: 'HEAD' })
				.then(response => {
					if (response.ok) document.getElementById('header-articles-link').style.display = 'flex';
				}).catch(() => {});

			// Hide Decks if none exist
			fetch(rootPath + '/decks.html', { method: 'HEAD' })
				.then(response => {
					if (response.ok) document.getElementById('header-decks-link').style.display = 'flex';
				}).catch(() => {});
		});
	</script>
	<div id="myContextMenu" class="rc-menu">
		<ul>
			<li id="add-to-deck">Add to Deck</li>
			<li id="add-to-sideboard">Add to Sideboard</li>
		</ul>
	</div>
	<input type="text" id="display" class="hidden" value="cards-and-text"> <!-- here to make img-container-defs snippet work properly -->
	<div class="page-container">
		<div class="search-container">
			<div class="deckbuilder-search-grid">
				<input type="text" inputmode="search" placeholder="Search ..." name="search" id="search" spellcheck="false" autocomplete="off" autocorrect="off" spellcheck="false">
				<div class="select-text">
					<select name="sort-by" id="sort-by">
						<option value="name">Name</option>
						<option value="set-code">Set / Number</option>
						<option value="mv">Mana Value</option>
						<option value="color">Color</option>
						<option value="rarity">Rarity</option>
					</select>:<select name="sort-order" id="sort-order">
						<option value="ascending">Asc</option>
						<option value="descending">Desc</option>
					</select>
				</div>
				<select name="search-display" id="search-display">
					<option value="cards">Cards</option>
					<option value="text">Text</option>
				</select>
			</div>
			<div class="search-results-container">
				<div class="gallery-column">
					<div class="search-image-grid-container">
						<div class="search-image-grid" id="imagesOnlyGrid">
						</div>
					</div>
					<div class="filter-bar">
						<input type="checkbox" id="filter-duplicates" checked onchange="displayChangeListener()">
						<label for="filter-duplicates">Filter duplicates</label>
					</div>
				</div>
				<div class="card-grid-container" id="card-grid-container">
				</div>
			</div>
		</div>
		<div class="deck-container">
			<div class="no-cards-text" id="no-cards-text">
				Click on a card to add it to the deck
			</div>
			<div class="deck-info-grid">
				<input type="text" value="Untitled Deck" id="deck-name" spellcheck="false" autocomplete="off" autocorrect="off" spellcheck="false">
				<select name="format-select" class="format-select" id="format-select">
					<option value="None">Format ...</option>
				</select>
				<div id="deck-count" class="deck-count">
					(0 / 0)
				</div>
				<select name="display-select" class="display-select" id="display-select">
					<option value="text">Text</option>
					<option value="images">Images</option>
				</select>
				<select name="file-menu" class="file-menu" id="file-menu">
					<option value="default">Actions ...</option>
					<option disabled>─── EDIT ───</option>
					<option value="new">New deck</option>
					<option value="import">Import deck</option>
					<option value="import-clipboard">Load from clipboard</option>
					<option value="clipboard">Copy to clipboard</option>
					<option value="save">Save deck</option>
					<option value="save-hash">Open deck page</option>
					<option disabled>─── EXPORT ───</option>
					<option value="export-dek">Export .dek</option>
					<option value="export-txt">Export .txt</option>
					<option value="export-cod">Export .cod</option>
					<option disabled>─── ADMIN ───</option>
					<option value="admin" id="admin-toggle-option">Admin mode</option>
					<option value="load-db" class="admin-only hidden">Load from database</option>
					<option value="update-db" class="admin-only hidden">Update saved deck</option>
					<option value="delete-db" class="admin-only hidden">Delete saved deck</option>
				</select>
				<input type="file" class="hidden" id="import-file" onclick="this.value=null;">
			</div>
			<div class="static-deck-container">
				<div class="deck-cards-container">
					<div class="deck-col" id="col1">
						<div class="deck-section" id="deck-creature">
							<span id="deck-creature-title">Creatures (0)</span>
							<div class="deck-inner-section" id="deck-creature-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-planeswalker">
							<span id="deck-planeswalker-title">Planeswalkers (0)</span>
							<div class="deck-inner-section" id="deck-planeswalker-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-artifact">
							<span id="deck-artifact-title">Artifacts (0)</span>
							<div class="deck-inner-section" id="deck-artifact-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-enchantment">
							<span id="deck-enchantment-title">Enchantments (0)</span>
							<div class="deck-inner-section" id="deck-enchantment-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-battle">
							<span id="deck-battle-title">Battles (0)</span>
							<div class="deck-inner-section" id="deck-battle-cards">
							</div>
						</div>
					</div>
					<div class="deck-col" id="col2">
						<div class="deck-section" id="deck-instant">
							<span id="deck-instant-title">Instants (0)</span>
							<div class="deck-inner-section" id="deck-instant-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-sorcery">
							<span id="deck-sorcery-title">Sorceries (0)</span>
							<div class="deck-inner-section" id="deck-sorcery-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-land">
							<span id="deck-land-title">Lands (0)</span>
							<div class="deck-inner-section" id="deck-land-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-sideboard">
							<span id="deck-sideboard-title">Sideboard (0)</span>
							<div class="deck-inner-section" id="deck-sideboard-cards">
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>

	<!-- Admin Password Modal -->
	<div id="admin-modal-overlay">
		<div class="admin-modal">
			<span class="admin-modal-close" onclick="closeAdminModal()">&times;</span>
			<p>Enter Hub Password:</p>
			<input type="password" id="admin-password-input" placeholder="Password...">
			<div class="admin-modal-buttons">
				<button class="admin-btn cancel" onclick="closeAdminModal()">Cancel</button>
				<button class="admin-btn save" id="admin-submit-btn" onclick="submitAdminPassword()">Submit</button>
			</div>
			<p id="admin-verify-msg">Verifying...</p>
		</div>
	</div>

	<!-- Notification Modal -->
	<div id="notification-modal-overlay">
		<div class="notification-modal">
			<p id="notification-msg"></p>
			<div class="admin-modal-buttons" id="notification-buttons-single">
				<button class="admin-btn save" onclick="closeNotification()">OK</button>
			</div>
			<div class="admin-modal-buttons" id="notification-buttons-confirm" style="display: none;">
				<button class="admin-btn cancel" onclick="closeNotification()">Cancel</button>
				<button class="admin-btn save" id="confirm-yes-btn">Confirm</button>
			</div>
		</div>
	</div>

	<!-- Selection Modal -->
	<div id="selection-modal-overlay">
		<div class="selection-modal">
			<span class="admin-modal-close" onclick="closeSelectionModal()">&times;</span>
			<h3 id="selection-title">Select Deck</h3>
			<input type="text" id="selection-search" placeholder="Search decks...">
			<div class="selection-chips" id="selection-list"></div>
		</div>
	</div>

	<script>
		let search_results = [];
		let card_list_arrayified = [];
		let cardLookupIndex = new Map();
		let specialchars = "";
		let deck = [];
		let sideboard = [];
		let active_card = [];
		let sets_json = {};
		let currentDeckId = null;
		let isAdmin = false;
		let contextMenu;

		function buildCardIndex() {
			cardLookupIndex.clear();
			card_list_arrayified.forEach(c => {
				const name = (c.card_name || "").trim().toLowerCase();
				// Index by Set+Num
				cardLookupIndex.set(`${c.set}:${c.number}`, c);
				// Index by Set+Name (for fallback)
				cardLookupIndex.set(`${c.set}:${name}`, c);
			});
		}

		function getCardImgSrc(card_stats) {
			const prefix = card_stats.hubURL ? card_stats.hubURL : rootPath;
			if ("position" in card_stats) {
				return prefix + "/sets/" + card_stats.set + "-files/img/" + card_stats.position + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
			}
			return prefix + "/sets/" + card_stats.set + "-files/img/" + card_stats.number + (card_stats.shape.includes("token") ? "t_" : "_") + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
		}

		function getCardStats(item) {
			if (!item) return null;
			const name = (item.name || item.card_name || "").trim();
			const num = item.num || item.number;
			const set = item.set;

			const notToken = (c) => !c.shape || !c.shape.includes("token");

			// 1. Try Set + Name + Number
			let stats = card_list_arrayified.find(c => c.set === set && (c.card_name || "").trim() === name && c.number == num && notToken(c));
			
			// 2. Try Set + Name
			if (!stats) {
				stats = card_list_arrayified.find(c => c.set === set && (c.card_name || "").trim() === name && notToken(c));
			}
			
			// 3. Try Set + Number
			if (!stats) {
				stats = card_list_arrayified.find(c => c.set === set && c.number == num && notToken(c));
			}
			
			return stats;
		}

		function getCardUrl(card) {
			const prefix = card.hubURL ? card.hubURL : window.location.origin;
			const url = new URL(prefix + '/card', prefix);
			url.searchParams.append('set', card.set);
			url.searchParams.append('num', card.number);
			url.searchParams.append('name', card.card_name);
			return url.href;
		}

		function convertToMV(cost) {
			if (!cost) return 0;
			let mv = 0;
			const tokens = cost.substring(1, cost.length - 1).split('}{');
			tokens.forEach(token => {
				if (!isNaN(token)) {
					mv += parseInt(token);
				} else if (token.includes('2')) {
					mv += 2;
				} else if (token !== 'x' && token !== '') {
					mv += 1;
				}
			});
			return mv;
		}

		function getMostExpensiveCard(deckData) {
			const board = (deckData.mainboard || []);
			if (board.length === 0) return null;
			
			let bestCard = null;
			let maxScore = -1;

			board.forEach(item => {
				const card = getCardStats(item);
				if (card) {
					const mv = convertToMV(card.cost);
					const rarities = { 'mythic': 4, 'rare': 3, 'uncommon': 2, 'common': 1, 'cube': 0 };
					const rarityScore = rarities[card.rarity] || 0;
					const score = (mv * 10) + rarityScore;
					
					if (score > maxScore) {
						maxScore = score;
						bestCard = card;
					}
				}
			});

			return bestCard;
		}

		document.addEventListener("DOMContentLoaded", async function () {
			contextMenu = document.getElementById("myContextMenu");
			'''

	with open(os.path.join('scripts', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

			await fetch(rootPath + '/lists/all-sets.json')
					.then(response => response.json())
					.then(data => {
						sets_json = data; 
				}).catch(error => console.error('Error:', error));
'''

	if os.path.exists(os.path.join('lists', 'external-hubs.txt')):
		html_content += '''
			try {
				const hubResp = await fetch(rootPath + '/lists/external-hubs.txt');
				if (hubResp.ok) {
					const hubsText = await hubResp.text();
					const hubURLs = hubsText.split(/\\r?\\n/).map(url => url.trim()).filter(url => url.length > 0);
					for (let url of hubURLs) {
						if (!url.startsWith('http')) {
							url = 'https://' + url;
						}
						try {
							const externalCardsResp = await fetch(url + '/lists/all-cards.json');
							if (externalCardsResp.ok) {
								const externalCardsJson = await externalCardsResp.json();
								externalCardsJson.cards.forEach(c => {
									c.hubURL = url;
									card_list_arrayified.push(c);
								});
							}
							const externalSetsResp = await fetch(url + '/lists/all-sets.json');
							if (externalSetsResp.ok) {
								const externalSetsJson = await externalSetsResp.json();
								externalSetsJson.sets.forEach(s => {
									if (!sets_json.sets.some(existing => existing.set_code === s.set_code)) {
										sets_json.sets.push(s);
									}
								});
							}
						} catch (e) {
							console.error('Error fetching external hub:', url, e);
						}
					}
				}
			} catch (e) {
				// No external hubs file or other error
			}
'''

	html_content += '''
			await fetch(rootPath + '/lists/formats.json')
					.then(response => response.json())
					.then(data => {
						const select = document.getElementById("format-select");
						data.formats.forEach(f => {
							const option = document.createElement("option");
							option.value = f;
							option.innerText = f;
							select.appendChild(option);
						});
				}).catch(error => console.error('Error:', error));

			cardGrid = document.getElementById("imagesOnlyGrid");
			card_list_arrayified.sort(compareFunction);
			buildCardIndex();

			gridified_card = gridifyCard(card_list_arrayified[0], true);
			gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
			gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
			document.getElementById("card-grid-container").appendChild(gridified_card);

			// initial search on load
			preSearch();

			if (localStorage.getItem("hubPassword")) {
				isAdmin = true;
				updateAdminUI();
			}

			document.getElementById("admin-password-input").addEventListener("keydown", (e) => {
				if (e.key === "Enter") submitAdminPassword();
			});
		});

		function toggleAdminMode() {
			if (!isAdmin) {
				document.getElementById("admin-modal-overlay").style.display = "flex";
				document.getElementById("admin-password-input").focus();
			} else {
				showConfirm("Disable Admin Mode?", () => {
					localStorage.removeItem("hubPassword");
					isAdmin = false;
					updateAdminUI();
				});
			}
		}

		function closeAdminModal() {
			document.getElementById("admin-modal-overlay").style.display = "none";
			document.getElementById("admin-password-input").value = "";
			document.getElementById("admin-verify-msg").style.display = "none";
		}

		async function submitAdminPassword() {
			const pass = document.getElementById("admin-password-input").value;
			if (!pass) return;

			document.getElementById("admin-verify-msg").style.display = "block";
			document.getElementById("admin-verify-msg").innerText = "Verifying...";
			
			// Try to fetch from hub_secrets using this password
			const resp = await fetch(`${SUPABASE_URL}/rest/v1/hub_secrets?hub_name=ilike.${hubName}`, {
				headers: {
					'apikey': SUPABASE_KEY,
					'Authorization': `Bearer ${SUPABASE_KEY}`,
					'x-hub-password': pass
				}
			});

			const data = await resp.json();
			if (resp.ok && data.length > 0) {
				localStorage.setItem("hubPassword", pass);
				isAdmin = true;
				updateAdminUI();
				closeAdminModal();
			} else {
				document.getElementById("admin-verify-msg").innerText = "Invalid password.";
				document.getElementById("admin-verify-msg").style.color = "red";
			}
		}

		function showAlert(msg) {
			document.getElementById("notification-msg").innerText = msg;
			document.getElementById("notification-buttons-single").style.display = "flex";
			document.getElementById("notification-buttons-confirm").style.display = "none";
			document.getElementById("notification-modal-overlay").style.display = "flex";
		}

		function showConfirm(msg, onConfirm) {
			document.getElementById("notification-msg").innerText = msg;
			document.getElementById("notification-buttons-single").style.display = "none";
			document.getElementById("notification-buttons-confirm").style.display = "flex";
			document.getElementById("notification-modal-overlay").style.display = "flex";
			
			const confirmBtn = document.getElementById("confirm-yes-btn");
			// Clone button to remove old listeners
			const newConfirmBtn = confirmBtn.cloneNode(true);
			confirmBtn.parentNode.replaceChild(newConfirmBtn, confirmBtn);
			
			newConfirmBtn.onclick = () => {
				closeNotification();
				onConfirm();
			};
		}

		function closeNotification() {
			document.getElementById("notification-modal-overlay").style.display = "none";
		}

		function showSelectionModal(title, items, onSelect) {
			document.getElementById("selection-title").innerText = title;
			const list = document.getElementById("selection-list");
			const searchInput = document.getElementById("selection-search");
			
			searchInput.value = "";
			
			const renderChips = (filterText = "") => {
				list.innerHTML = "";
				const filtered = items.filter(item => 
					item.name.toLowerCase().includes(filterText.toLowerCase())
				);
				
				filtered.forEach(item => {
					const chip = document.createElement("div");
					chip.className = "selection-chip";
					
					// Get preview image from the most "expensive" card (like decks.html)
					let imgSrc = "";
					const bestCard = getMostExpensiveCard(item);
					if (bestCard) {
						imgSrc = getCardImgSrc(bestCard);
					}

					chip.innerHTML = `
						<div class="selection-chip-image" style="${imgSrc ? `background-image: url('${imgSrc}')` : ''}"></div>
						<div class="selection-chip-info">
							<p class="selection-chip-name">${item.name}</p>
							<p class="selection-chip-format">${item.format || 'No format'}</p>
						</div>
					`;

					chip.onclick = () => {
						closeSelectionModal();
						onSelect(item);
					};
					list.appendChild(chip);
				});
			};

			searchInput.oninput = (e) => renderChips(e.target.value);
			renderChips();
			
			document.getElementById("selection-modal-overlay").style.display = "flex";
			searchInput.focus();
		}

		function closeSelectionModal() {
			document.getElementById("selection-modal-overlay").style.display = "none";
		}

		function updateAdminUI() {
			const adminToggle = document.getElementById("admin-toggle-option");
			
			if (isAdmin) {
				adminToggle.innerText = "Exit Admin Mode";
			} else {
				adminToggle.innerText = "Admin Mode";
			}

			// Load from database only needs isAdmin
			const loadOpt = document.querySelector('option[value="load-db"]');
			if (isAdmin) loadOpt.classList.remove("hidden");
			else loadOpt.classList.add("hidden");

			// Update and Delete need isAdmin AND currentDeckId
			const updateOpt = document.querySelector('option[value="update-db"]');
			const deleteOpt = document.querySelector('option[value="delete-db"]');
			
			if (isAdmin && currentDeckId) {
				updateOpt.classList.remove("hidden");
				deleteOpt.classList.remove("hidden");
			} else {
				updateOpt.classList.add("hidden");
				deleteOpt.classList.add("hidden");
			}
		}

		async function loadFromDatabase() {
			const { data, error } = await _supabase
				.from('decks')
				.select('id, name, format, mainboard, sideboard')
				.eq('hub', hubName)
				.order('created_at', { ascending: false });

			if (error) {
				console.error('Error fetching decks:', error);
				showAlert('Failed to fetch decks from database.');
				return;
			}

			if (data.length === 0) {
				showAlert("No decks found in the database for this hub.");
				return;
			}

			showSelectionModal("Select a deck to load:", data, async (selectedDeck) => {
				// Fetch full deck details
				const { data: fullDeck, error: fetchError } = await _supabase
					.from('decks')
					.select('*')
					.eq('id', selectedDeck.id)
					.single();

				if (fetchError) {
					console.error('Error fetching deck details:', fetchError);
					return;
				}

				// Load into builder
				currentDeckId = fullDeck.id;
				document.getElementById("deck-name").value = fullDeck.name;
				document.getElementById("format-select").value = fullDeck.format || "None";
				
				deck = [];
				sideboard = [];

				fullDeck.mainboard.forEach(item => {
					const stats = getCardStats(item);
					if (stats) {
						for (let i = 0; i < item.count; i++) deck.push(JSON.stringify(stats));
					}
				});

				fullDeck.sideboard.forEach(item => {
					const stats = getCardStats(item);
					if (stats) {
						for (let i = 0; i < item.count; i++) sideboard.push(JSON.stringify(stats));
					}
				});

				processDeck();
				updateAdminUI();
			});
		}

		async function updateSavedDeck() {
			if (!currentDeckId) return;
			const password = localStorage.getItem("hubPassword");
			if (!password) {
				showAlert("Admin Password missing. Re-enable Admin Mode.");
				return;
			}

			const deckName = document.getElementById("deck-name").value;
			const deckFormat = document.getElementById("format-select").value;

			const mainboardData = [];
			const mainMap = new Map();
			deck.forEach(cardStr => {
				mainMap.set(cardStr, (mainMap.get(cardStr) || 0) + 1);
			});
			mainMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				mainboardData.push({ set: card.set, num: card.number, count: count, name: card.card_name });
			});

			const sideboardData = [];
			const sideMap = new Map();
			sideboard.forEach(cardStr => {
				sideMap.set(cardStr, (sideMap.get(cardStr) || 0) + 1);
			});
			sideMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				sideboardData.push({ set: card.set, num: card.number, count: count, name: card.card_name });
			});

			// We use a custom fetch here because Supabase JS client doesn't support custom headers for specific requests easily
			// and we need to pass the hub password for RLS.
			const resp = await fetch(`${SUPABASE_URL}/rest/v1/decks?id=eq.${currentDeckId}`, {
				method: 'PATCH',
				headers: {
					'apikey': SUPABASE_KEY,
					'Authorization': `Bearer ${SUPABASE_KEY}`,
					'Content-Type': 'application/json',
					'Prefer': 'return=representation',
					'x-hub-password': password
				},
				body: JSON.stringify({
					name: deckName,
					format: deckFormat,
					mainboard: mainboardData,
					sideboard: sideboardData
				})
			});

			if (!resp.ok) {
				const err = await resp.json();
				console.error('Error updating deck:', err);
				showAlert('Failed to update deck. Check password?');
			} else {
				const shareUrl = window.location.origin + window.location.pathname.replace('deckbuilder', 'deck') + '?id=' + currentDeckId;
				window.open(shareUrl, "_blank");
			}
			document.getElementById("file-menu").value = "default";
		}

		async function deleteSavedDeck() {
			if (!currentDeckId) return;
			showConfirm("Are you sure you want to PERMANENTLY delete this deck from the database?", async () => {
				const password = localStorage.getItem("hubPassword");
				
				const resp = await fetch(`${SUPABASE_URL}/rest/v1/decks?id=eq.${currentDeckId}`, {
					method: 'DELETE',
					headers: {
						'apikey': SUPABASE_KEY,
						'Authorization': `Bearer ${SUPABASE_KEY}`,
						'x-hub-password': password
					}
				});

				if (!resp.ok) {
					showAlert('Failed to delete deck. Check password?');
				} else {
					deck = [];
					sideboard = [];
					currentDeckId = null;
					document.getElementById("deck-name").value = "Untitled Deck";
					processDeck();
					updateAdminUI();
				}
			});
		}

		function displayChangeListener() {
			preSearch();
		}

		document.getElementById("sort-by").onchange = displayChangeListener;
		document.getElementById("sort-order").onchange = displayChangeListener;
		document.getElementById("search-display").onchange = displayChangeListener;

		document.getElementById("file-menu").addEventListener("change", function(event) {
			let option = document.getElementById("file-menu").value;

			if (option == "new")
			{
				deck = [];
				sideboard = [];
				processDeck();
				document.getElementById("file-menu").value = "default";
			}
			else if (option == "import")
			{
				document.getElementById("import-file").click();
			}
			else if (option == "import-clipboard")
			{
				importFromClipboard();
			}
			else if (option == "load-db")
			{
				loadFromDatabase();
			}
			else if (option == "save")
			{
				saveToCloud();
			}
			else if (option == "update-db")
			{
				updateSavedDeck();
			}
			else if (option == "delete-db")
			{
				deleteSavedDeck();
			}
			else if (option == "save-hash")
			{
				openHashedDeck();
			}
			else if (option == "admin")
			{
				toggleAdminMode();
			}
			else if (option == "clipboard" || option.startsWith("export"))
			{
				exportFile(option);
			}
			document.getElementById("file-menu").value = "default";
		});

		document.addEventListener("click", (event) => {
			if (!contextMenu.contains(event.target)) {
				contextMenu.style.display = "none";
			}
		});

		document.getElementById("add-to-deck").addEventListener("click", () => {
			addCardToDeck(active_card);
			contextMenu.style.display = "none";
		});

		document.getElementById("add-to-sideboard").addEventListener("click", () => {
			addCardToSideboard(active_card);
			contextMenu.style.display = "none";
		});

		document.getElementById("display-select").addEventListener("change", function(event) {
			processDeck();
		});

		document.getElementById("import-file").addEventListener("change", function(event) {
			const files = event.target.files;

			if (files.length > 0) {
				const file = files[0];
				const name = file.name.replace(/\\.[^/.]+$/, "");
				const import_type = file.name.replace(/^[^/.]+\\./, "");

				document.getElementById("deck-name").value = name;

				deck = [];
				sideboard = [];
				sb_cards = false;

				const reader = new FileReader();
				reader.onload = function(e) {
					const fileContent = e.target.result;

					const lines = fileContent.split('\\n');
					if (import_type == 'dek')
					{
						for (const line of lines)
						{
							if (line == 'sideboard' || line == '') // '' for Draftmancer files
							{
								sb_cards = true;
							}
							else
							{
								const count = line.substring(0, line.indexOf(' '));
								const card = line.substring(line.indexOf(' ') + 1);

								for (let i = 0; i < count; i++)
								{
									if (sb_cards)
									{
										addCardToSideboard(card);
									}
									else
									{
										addCardToDeck(card);
									}
								}						
							}
						}
					}
					else if (import_type == 'txt')
					{
						let deck_map = new Map();
						let sb_map = new Map();

						for (const line of lines)
						{
							if (line == 'sideboard' || line == '') // '' for Draftmancer files
							{
								sb_cards = true;
							}
							else if (!sb_cards)
							{
								count = parseInt(line.substring(0, line.indexOf(' ')));
								card_name = line.substring(line.indexOf(' ') + 1);

								if (deck_map.has(card_name))
								{
									deck_map.set(card_name, deck_map.get(card_name) + count);
								}
								else
								{
									deck_map.set(card_name, count);
								}
							}
							else
							{
								count = parseInt(line.substring(0, line.indexOf(' ')));
								card_name = line.substring(line.indexOf(' ') + 1);

								if (sb_map.has(card_name))
								{
									sb_map.set(card_name, sb_map.get(card_name) + count);
								}
								else
								{
									sb_map.set(card_name, count);
								}
							}
						}
						for (const card of card_list_arrayified)
						{
							if (card.shape && card.shape.includes("token")) continue;

							if (deck_map.has(card.card_name))
							{
								for (let i = 0; i < deck_map.get(card.card_name); i++)
								{
									addCardToDeck(JSON.stringify(card));
								}
								deck_map.delete(card.card_name);
							}

							if (sb_map.has(card.card_name))
							{
								for (let i = 0; i < sb_map.get(card.card_name); i++)
								{
									addCardToSideboard(JSON.stringify(card));
								}
								sb_map.delete(card.card_name);
							}
						}
					}
				};
				reader.readAsText(file);
			}

			document.getElementById("file-menu").value = "default";
		});

		'''

	with open(os.path.join('scripts', 'snippets', 'compare-function.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function preSearch() {
			const searchTerms = document.getElementById("search").value.toLowerCase();
			const tokens = tokenizeTerms(searchTerms) || [];
			const sortBySelect = document.getElementById("sort-by");
			const sortOrderSelect = document.getElementById("sort-order");

			sortBySelect.disabled = false;
			sortOrderSelect.disabled = false;

			tokens.forEach(token => {
				if (token.startsWith("sort:")) {
					const val = token.substring(5);
					const map = {
						"name": "name",
						"set": "set-code",
						"mv": "mv",
						"color": "color",
						"rarity": "rarity",
						"cube": "cube"
					};
					if (map[val]) {
						const option = Array.from(sortBySelect.options).find(opt => opt.value === map[val]);
						if (option) {
							sortBySelect.value = map[val];
							sortBySelect.disabled = true;
						}
					}
				}
				if (token.startsWith("direction:")) {
					const val = token.substring(10);
					const map = {
						"asc": "ascending",
						"desc": "descending"
					};
					if (map[val]) {
						const option = Array.from(sortOrderSelect.options).find(opt => opt.value === map[val]);
						if (option) {
							sortOrderSelect.value = map[val];
							sortOrderSelect.disabled = true;
						}
					}
				}
			});

			card_list_arrayified.sort(compareFunction);
			if (document.getElementById("sort-order").value == "descending")
			{
				card_list_arrayified.reverse();
			}
			search_results = [];

			search();
		}

		let currentRenderIndex = 0;
		const CHUNK_SIZE = 100;
		let searchObserver = null;
		let currentProcessedResults = [];

		function search() {
			searchTerms = document.getElementById("search").value.toLowerCase();
			const displayMode = document.getElementById("search-display").value;
			const filterDuplicates = document.getElementById("filter-duplicates").checked;

			const resultsContainer = document.querySelector(".search-image-grid-container");
			if (resultsContainer) resultsContainer.scrollTop = 0;

			cardGrid = document.getElementById("imagesOnlyGrid");
			cardGrid.innerHTML = "";
			search_results = [];
			currentRenderIndex = 0;

			if (searchObserver) {
				searchObserver.disconnect();
			}

			if (displayMode === "text") {
				cardGrid.style.display = "block";
				const header = document.createElement("div");
				header.className = "search-row search-row-header";
				header.innerHTML = "<div>Name</div><div>Sets</div><div>Cost</div><div>P/T</div><div>Type</div>";
				cardGrid.appendChild(header);
			} else {
				cardGrid.style.display = "grid";
			}

			for (const card of card_list_arrayified) {
				if (card.shape.includes("token") && !searchTerms.includes("*t:token") && !searchTerms.includes("t:token"))
				{
					continue;
				}

				searched = searchAllTokens(card, tokenizeTerms(searchTerms));

				if (searched && (!filterDuplicates || !containsCard(search_results, card)))
				{
					search_results.push(card);
				}
			}

			// Pre-process results for the current display mode
			if (displayMode === "text") {
				const groupedResults = [];
				const seenCards = new Set();
				
				// Create a quick lookup for sets to avoid O(n^2) later
				const setLookup = {};
				card_list_arrayified.forEach(c => {
					if (!setLookup[c.card_name]) setLookup[c.card_name] = new Set();
					setLookup[c.card_name].add(c.set);
				});

				search_results.forEach(card => {
					// Unique identifier depends on whether we are filtering duplicates
					const id = filterDuplicates ? card.card_name : `${card.set}-${card.number}`;
					
					if (!seenCards.has(id)) {
						seenCards.add(id);
						const cardSets = filterDuplicates ? Array.from(setLookup[card.card_name]).join(", ") : card.set;
						groupedResults.push({ ...card, allSets: cardSets });
					}
				});
				currentProcessedResults = groupedResults;
			} else {
				currentProcessedResults = search_results;
			}

			renderNextChunk();
		}

		function renderNextChunk() {
			const displayMode = document.getElementById("search-display").value;
			const cardGrid = document.getElementById("imagesOnlyGrid");
			
			const oldSentinel = document.getElementById("search-sentinel");
			if (oldSentinel) oldSentinel.remove();

			const nextChunk = currentProcessedResults.slice(currentRenderIndex, currentRenderIndex + CHUNK_SIZE);
			
			nextChunk.forEach(card_stats => {
				if (displayMode === "text") {
					const row = document.createElement("div");
					row.className = "search-row";
					const pt = (card_stats.pt || "").replace(/\\//g, "/");
					const cleanCost = card_stats.cost.replace(/{(.*?)}/g, (match, p1) => {
						return p1.length > 1 ? p1.split('').join('/') : p1;
					});
					row.innerHTML = `<div>${card_stats.card_name}</div>
									 <div>${card_stats.allSets}</div>
									 <div>${cleanCost}</div>
									 <div>${pt}</div>
									 <div>${card_stats.type}</div>`;
					row.onmouseover = () => renderPreview(card_stats);
					row.onclick = () => addCardToDeck(JSON.stringify(card_stats));
					row.addEventListener("contextmenu", (event) => {
						event.preventDefault();
						showContextMenu(event, card_stats);
					});
					cardGrid.appendChild(row);
				} else {
					const imgContainer = document.createElement("div");
					imgContainer.className = "img-container";
					const card_sr_grid = gridifyCard(card_stats, true, true);
					const card_sr = card_sr_grid.getElementsByTagName("img")[0];
					card_sr.onmouseover = () => renderPreview(card_stats);
					card_sr.onclick = () => addCardToDeck(JSON.stringify(card_stats));
					card_sr.style.cursor = "pointer";
					card_sr.addEventListener("contextmenu", (event) => {
						event.preventDefault();
						showContextMenu(event, card_stats);
					});
					imgContainer.appendChild(card_sr);
					cardGrid.appendChild(imgContainer);
				}
			});

			currentRenderIndex += CHUNK_SIZE;

			if (currentRenderIndex < currentProcessedResults.length) {
				const sentinel = document.createElement("div");
				sentinel.id = "search-sentinel";
				sentinel.style.height = "20px";
				cardGrid.appendChild(sentinel);

				if (!searchObserver) {
					searchObserver = new IntersectionObserver((entries) => {
						if (entries[0].isIntersecting) {
							renderNextChunk();
						}
					}, { root: document.querySelector(".search-image-grid-container"), threshold: 0.1 });
				}
				searchObserver.observe(sentinel);
			}
		}

		function renderPreview(card_stats) {
			const cgc = document.getElementById("card-grid-container");
			cgc.innerHTML = "";
			const gridified_card = gridifyCard(card_stats, true);
			gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
			gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
			if (card_stats.shape.includes("double")) {
				gridified_card.getElementsByTagName("button")[0].onclick = function() {
					imgFlip("image-grid-card", card_stats.rotated);
				}
			}
			cgc.appendChild(gridified_card);
		}

		function showContextMenu(event, card_stats) {
			const contextMenu = document.getElementById("myContextMenu");
			contextMenu.style.display = "block";
			contextMenu.style.left = event.pageX + "px";
			contextMenu.style.top = event.pageY + "px";
			active_card = JSON.stringify(card_stats);
		}

		function containsCard(list, card)
		{
			for (const li of list)
			{
				if (li.card_name == card.card_name && li.cost == card.cost)
				{
					return true;
				}
			}

			return false;
		}

		'''

	with open(os.path.join('scripts', 'snippets', 'search-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	with open(os.path.join('scripts', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function gridifyCard(card_stats, card_text = false, small = false, designer_notes = false) {
			const card_name = card_stats.card_name;
			rotate_card = !small && card_stats.rotated;

			if (!card_text)
			{
				return buildImgContainer(card_stats, true, rotate_card);			
			}

		'''

	with open(os.path.join('scripts', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
		const originalBuildImgContainer = buildImgContainer;
		buildImgContainer = function(card_stats, hidden_title = false, rotate_card = false) {
			const container = originalBuildImgContainer(card_stats, hidden_title, rotate_card);
			if (card_stats.hubURL) {
				const img = container.querySelector(".card-image");
				if (img) {
					img.src = img.src.replace(/^.*\/sets\//, card_stats.hubURL + "/sets/");
				}
				const hImg = container.querySelector(".h-img");
				if (hImg) {
					hImg.src = hImg.src.replace(/^.*\/sets\//, card_stats.hubURL + "/sets/");
				}
				const link = container.querySelector("a");
				if (link) {
					const url = new URL(card_stats.hubURL + '/card', card_stats.hubURL);
					const params = {
						set: card_stats.set,
						num: card_stats.number,
						name: card_stats.card_name
					}
					for (const key in params) {
						url.searchParams.append(key, params[key]);
					}
					link.href = url.toString();
				}
			}
			return container;
		};

		function hasAllChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (!strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal;
		}

		function hasNoChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal;
		}

		function hasAllAndMoreChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (!strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal && (strOut.length > strIn.length);
		}

		function addCardToDeck(card) {
			deck.push(card);
			processDeck();
		}

		function addCardToSideboard(card) {
			sideboard.push(card);
			processDeck();
		}

		function processDeck() {
			const nct = document.getElementById("no-cards-text");
			nct.style.display = (deck.length == 0 && sideboard.length == 0) ? "block" : "none";

			const dc = document.getElementById("deck-count");
			dc.innerText = "(" + deck.length + " / " + sideboard.length + ")";

			let deck_cards = new Map([
				['land', new Map([])],
				['creature', new Map([])],
				['instant', new Map([])],
				['planeswalker', new Map([])],
				['artifact', new Map([])],
				['enchantment', new Map([])],
				['sorcery', new Map([])],
				['battle', new Map([])],
				['sideboard', new Map([])]
			]);

			for (const card of deck)
			{
				card_type = JSON.parse(card).type.toLowerCase();

				for (const [key, map] of deck_cards)
				{
					if (card_type.includes(key))
					{
						if (map.has(card))
						{
							map.set(card, map.get(card) + 1);
						}
						else
						{
							map.set(card, 1);
						}

						break;
					}
				}
			}
			for (const card of sideboard)
			{
				let map = deck_cards.get("sideboard");
				if (map.has(card))
				{
					map.set(card, map.get(card) + 1);
				}
				else
				{
					map.set(card, 1);
				}
			}

			for (const [key, map] of deck_cards)
			{
				dsec_id = "deck-" + key;
				outer_ele = document.getElementById(dsec_id);

				if (map.size == 0)
				{
					outer_ele.style.display = "none";
				}
				else
				{
					outer_ele.style.display = "grid";
					dsec_c_id = dsec_id + "-cards";
					
					dsec_t_id = dsec_id + "-title";
					title_ele = document.getElementById(dsec_t_id);
					let count = 0;
					for (const val of Array.from(map.values()))
					{
						count += val;
					}
					const numregex = /[0-9]+/;
					title_ele.innerText = title_ele.innerText.replace(numregex, count);

					cards_ele = document.getElementById(dsec_c_id);
					cards_ele.innerHTML = "";
					const cards_list = Array.from(map.keys()).sort();				
					for (const card of cards_list)
					{
						const display_style = document.getElementById("display-select").value;
						const card_stats = JSON.parse(card);
						const card_name = card_stats.card_name;

						if (display_style == "text")
						{
							card_row = document.createElement("div");
							card_row.className = "deck-line";
							
							card_in_deck = document.createElement("div");
							card_in_deck.innerText += map.get(card) + " " + card_name + "\\n";
							card_in_deck.style.cursor = "pointer";
							card_in_deck.onmouseover = function() {
								cgc = document.getElementById("card-grid-container");
								cgc.innerHTML = "";
								const gridified_card = gridifyCard(card_stats, true);
								gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
								gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
								if (card_stats.shape.includes("double"))
								{
									gridified_card.getElementsByTagName("button")[0].onclick = function() {
										imgFlip("image-grid-card", card_stats.rotated);
									}
								}
								cgc.appendChild(gridified_card);
							};

							del_btn = document.createElement("img");
							del_btn.className = "icon";
							del_btn.style.cursor = "pointer";

							add_btn = document.createElement("img");
							add_btn.className = "icon";
							add_btn.style.cursor = "pointer";

							if (key == "sideboard")
							{
								del_btn.src = rootPath + "/img/sb-delete.png";
								del_btn.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									processDeck();
								}

								add_btn.src = rootPath + "/img/sb-add.png";
								add_btn.onclick = function() {
									sideboard.push(card);
									processDeck();
								}

								card_in_deck.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									addCardToDeck(card);
								}
							}
							else
							{
								del_btn.src = rootPath + "/img/delete.png";
								del_btn.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									processDeck();
								}

								add_btn.src = rootPath + "/img/add.png";
								add_btn.onclick = function() {
									deck.push(card);
									processDeck();
								}

								card_in_deck.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									addCardToSideboard(card);
								}
							}

							db_container = document.createElement("div");
							db_container.className = "card-fx";
							db_container.appendChild(del_btn);

							ab_container = document.createElement("div");
							ab_container.className = "card-fx";
							ab_container.appendChild(add_btn);

							card_row.appendChild(db_container);
							card_row.appendChild(ab_container);
							card_row.appendChild(card_in_deck);
							cards_ele.appendChild(card_row);
						}
						else
						{
							card_img_container = document.createElement("div");
							card_img_container.className = "card-img-container";
							if (card == cards_list[cards_list.length - 1])
							{
								card_img_container.style.height = "auto";
								card_img_container.style.maxHeight = "100%";
							}

							card_img = document.createElement("img");
							card_img.loading = "lazy";
							card_img.src = getCardImgSrc(card_stats);
							card_img.style.cursor = "pointer";
							card_img.onmouseover = function() {
								cgc = document.getElementById("card-grid-container");
								cgc.innerHTML = "";
								const gridified_card = gridifyCard(card_stats, true);
								gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
								gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
								if (card_stats.shape.includes("double"))
								{
									gridified_card.getElementsByTagName("button")[0].onclick = function() {
										imgFlip("image-grid-card", card_stats.rotated);
									}
								}
								cgc.appendChild(gridified_card);
							};

							card_count = document.createElement("div");
							card_count.innerText = map.get(card) + "x";

							del_btn = document.createElement("img");
							del_btn.className = "icon";
							del_btn.style.cursor = "pointer";

							add_btn = document.createElement("img");
							add_btn.className = "icon";
							add_btn.style.cursor = "pointer";

							if (key == "sideboard")
							{
								del_btn.src = rootPath + "/img/sb-delete.png";
								del_btn.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									processDeck();
								}

								add_btn.src = rootPath + "/img/sb-add.png";
								add_btn.onclick = function() {
									sideboard.push(card);
									processDeck();
								}

								card_img.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									addCardToDeck(card);
								}
							}
							else
							{
								del_btn.src = rootPath + "/img/delete.png";
								del_btn.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									processDeck();
								}

								add_btn.src = rootPath + "/img/add.png";
								add_btn.onclick = function() {
									deck.push(card);
									processDeck();
								}

								card_img.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									addCardToSideboard(card);
								}
							}

							db_container = document.createElement("div");
							db_container.className = "card-fx";
							db_container.appendChild(del_btn);

							ab_container = document.createElement("div");
							ab_container.className = "card-fx";
							ab_container.appendChild(add_btn);
							card_count.className = "card-fx";

							card_img_container.appendChild(db_container);
							card_img_container.appendChild(ab_container);
							card_img_container.appendChild(card_count);
							card_img_container.appendChild(card_img);
							cards_ele.appendChild(card_img_container);
						}
					}
				}
			}
		}

		function openHashedDeck() {
			const deckName = document.getElementById("deck-name").value;
			let mainParts = [];
			let sideParts = [];

			const mainMap = new Map();
			deck.forEach(cardStr => {
				mainMap.set(cardStr, (mainMap.get(cardStr) || 0) + 1);
			});
			mainMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				mainParts.push(`${card.set}:${card.number}:${count}:${card.card_name}`);
			});

			const sideMap = new Map();
			sideboard.forEach(cardStr => {
				sideMap.set(cardStr, (sideMap.get(cardStr) || 0) + 1);
			});
			sideMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				sideParts.push(`${card.set}:${card.number}:${count}:${card.card_name}`);
			});

			const compactString = `${deckName}|${document.getElementById("format-select").value}|${mainParts.join(';')}|${sideParts.join(';')}`;
			const hash = btoa(unescape(encodeURIComponent(compactString)));
			window.open(rootPath + "/deck#" + hash, "_blank");
			document.getElementById("file-menu").value = "default";
		}

		async function saveToCloud() {
			const deckName = document.getElementById("deck-name").value;
			const deckFormat = document.getElementById("format-select").value;
			const deckId = generateShortId();
			
			const mainboardData = [];
			const mainMap = new Map();
			deck.forEach(cardStr => {
				mainMap.set(cardStr, (mainMap.get(cardStr) || 0) + 1);
			});
			mainMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				mainboardData.push({ set: card.set, num: card.number, count: count, name: card.card_name });
			});

			const sideboardData = [];
			const sideMap = new Map();
			sideboard.forEach(cardStr => {
				sideMap.set(cardStr, (sideMap.get(cardStr) || 0) + 1);
			});
			sideMap.forEach((count, cardStr) => {
				const card = JSON.parse(cardStr);
				sideboardData.push({ set: card.set, num: card.number, count: count, name: card.card_name });
			});

			const { data, error } = await _supabase
				.from('decks')
				.insert([
					{ id: deckId, name: deckName, format: deckFormat, mainboard: mainboardData, sideboard: sideboardData, hub: hubName }
				])
				.select();

			if (error) {
				console.error('Error saving deck:', error);
				showAlert('Failed to save deck to cloud.');
			} else {
				const shareUrl = window.location.origin + window.location.pathname.replace('deckbuilder', 'deck') + '?id=' + deckId;
				window.open(shareUrl, "_blank");
			}
			document.getElementById("file-menu").value = "default";
		}

		async function exportFile(export_as) {
			let deck_text = "";
			let deck_name = document.getElementById("deck-name").value;
			let export_cod = (export_as == "export-cod");

			if (export_cod) {
				deck_text += `<?xml version="1.0" encoding="UTF-8"?>\\n<cockatrice_deck version="1">\\n\\t<deckname>${deck_name}</deckname>\\n\\t<zone name="main">\\n`;
			}

			let map = new Map([]);
			for (const card of deck)
			{
				if (map.has(card))
				{
					map.set(card, map.get(card) + 1);
				}
				else
				{
					map.set(card, 1);
				}
			}
			for (const card_map of Array.from(map.keys()))
			{
				let card_number = map.get(card_map);
				if (export_cod) {
					deck_text += `\\t\\t<card number="${card_number}" name="${JSON.parse(card_map).card_name}"/>\\n`;
					continue; // continue instead of writing else
				}
				deck_text += card_number + " " + (export_as == "export-dek" ? card_map : JSON.parse(card_map).card_name + "\\n");
			}
			if (sideboard.length != 0)
			{
				deck_text += export_cod ? '\\t</zone>\\n\\t<zone name="side">\\n' : "sideboard\\n";
				map = new Map([]);
				for (const card of sideboard)
				{
					if (map.has(card))
					{
						map.set(card, map.get(card) + 1);
					}
					else
					{
						map.set(card, 1);
					}
				}
				for (const card_map of Array.from(map.keys()))
				{
					let card_number = map.get(card_map);
					if (export_cod) {
						deck_text += `\\t\\t<card number="${card_number}" name="${JSON.parse(card_map).card_name}"/>\\n`;
						continue; // continue instead of writing else
					}
					deck_text += card_number + " " + (export_as == "export-dek" ? card_map : JSON.parse(card_map).card_name + "\\n");
				}
			}

			if (export_cod) {
				deck_text += "\\t</zone>\\n</cockatrice_deck>";
			}

			if (export_as != "clipboard")
			{
				let downloadableLink = document.createElement('a');
				downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(deck_text));
				downloadableLink.download = deck_name + ("." + export_as.split("-")[1]);
				document.body.appendChild(downloadableLink);
				downloadableLink.click();
				document.body.removeChild(downloadableLink);
			}
			else
			{
				navigator.clipboard.writeText(deck_text);
			}

			document.getElementById("file-menu").value = "default";
		}

		async function importFromClipboard() {
			try {
				const deckText = await navigator.clipboard.readText();

				deck = [];
				sideboard = [];

				let deck_map = new Map();
				let sb_map = new Map();
				let sb_cards = false;

				for (let line of deckText.split('\\n'))
				{
					line = line.trim();

					if (line == 'sideboard' || line == '') // '' for Draftmancer files
					{
						sb_cards = true;
					}
					else if (!sb_cards)
					{
						count = parseInt(line.substring(0, line.indexOf(' ')));
						card_name = line.substring(line.indexOf(' ') + 1);

						if (deck_map.has(card_name))
						{
							deck_map.set(card_name, deck_map.get(card_name) + count);
						}
						else
						{
							deck_map.set(card_name, count);
						}
					}
					else
					{
						count = parseInt(line.substring(0, line.indexOf(' ')));
						card_name = line.substring(line.indexOf(' ') + 1);

						if (sb_map.has(card_name))
						{
							sb_map.set(card_name, sb_map.get(card_name) + count);
						}
						else
						{
							sb_map.set(card_name, count);
						}
					}
				}
				for (const card of card_list_arrayified)
				{
					if (card.shape && card.shape.includes("token")) continue;

					if (deck_map.has(card.card_name))
					{
						for (let i = 0; i < deck_map.get(card.card_name); i++)
						{
							addCardToDeck(JSON.stringify(card));
						}
						deck_map.delete(card.card_name);
					}

					if (sb_map.has(card.card_name))
					{
						for (let i = 0; i < sb_map.get(card.card_name); i++)
						{
							addCardToSideboard(JSON.stringify(card));
						}
						sb_map.delete(card.card_name);
					}
				}
			} catch (err) {
				console.error('Failed to read clipboard:', err);
			}
			document.getElementById("file-menu").value = "default";
		}

		function goToSearch() {
			window.location = (rootPath + "/search");
		}

		document.getElementById("search").addEventListener("keypress", function(event) {
			if (event.key === "Enter") {
				event.preventDefault();
				preSearch();
			}
		});

		'''

	with open(os.path.join('scripts', 'snippets', 'random-card.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	# ඞ sus
	html_content += '''
	</script>
</body>
</html>'''

	# Write the HTML content to the output HTML file
	with open(output_html_file, 'w', encoding='utf-8-sig') as file:
		file.write(html_content)

	print(f"HTML file saved as {output_html_file}")