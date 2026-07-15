import os
import sys
import json

def generateHTML(codes):
	output_html_file = "deck.html"

	with open(os.path.join('resources', 'site-config.json'), encoding='utf-8-sig') as f:
		config = json.load(f)
		base_url = config.get('base_url', '')
		hub_name = base_url.split('https://')[1].split('.github.io')[0].lower() if 'https://' in base_url else 'unknown'

	# Start creating the HTML file content
	html_content = '''<html>
<head>
	<title>Deck</title>
	<link rel="icon" type="image/x-icon" href="./img/deck.png">
	<link rel="stylesheet" href="./resources/mana.css">
	<link rel="stylesheet" href="./resources/header.css">
	<link rel="stylesheet" href="./resources/card-text.css">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<script title="root">
	const rootPath = ".";
	const SUPABASE_URL = 'https://mtjkkvtcmejzcpjmropd.supabase.co';
	const SUPABASE_KEY = 'sb_publishable_Hgyr2JJRsJRa1pYwoz-ijQ_ozfwnp9t';
	const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
	const hubName = "''' + hub_name + '''";
</script>
<style>
	@font-face {
		font-family: Beleren;
		src: url('./resources/beleren.ttf');
	}
	body {
		font-family: 'Helvetica', 'Arial', sans-serif;
		overscroll-behavior: none;
		margin: 0px;
		background-color: #bbbbbb;
		display: block;
	}
	.page-container {
		width: 100%;
		height: 91vh;
		padding: 20px;
		display: block;
		margin: auto;
		box-sizing: border-box;
	}
	.deck-display-container {
		height: 100%;
		width: 100%;
		max-width: 1300px;
		margin: auto;
		border: 1px solid #d5d9d9;
		border-top: 4px solid #171717;
		border-bottom: 4px solid #171717;
		background-color: #f3f3f3;
		border-radius: 6px;
		display: grid;
		grid-template-columns: 1fr 500px;
		overflow-y: hidden;
		overflow-x: hidden;
		position: relative;
	}
	.deck-main-area {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow-y: hidden;
		border-right: 1px solid #d5d9d9;
	}
	.deck-header {
		width: 95%;
		min-height: 50px;
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 5px 2.5%;
		border-bottom: 1px solid #898989;
	}
	#deck-title {
		font-family: Beleren;
		font-size: 24px;
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
	.deck-cards-scroll-container {
		flex-grow: 1;
		overflow-y: auto;
		overflow-x: hidden;
		scrollbar-width: none;
		padding: 20px;
	}
	.deck-cards-scroll-container::-webkit-scrollbar {
		display: none;
	}
	
	.deck-columns-container {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr;
		gap: 0px;
	}
	@media (max-width: 1200px) {
		.deck-columns-container {
			grid-template-columns: 1fr 1fr;
		}
	}
	.deck-col {
		padding: 0 12px;
	}
	.deck-section {
		margin-bottom: 20px;
	}
	.deck-section-title {
		font-size: 15px;
		font-weight: bold;
		padding-top: 10px;
		padding-bottom: 10px;
		padding-left: 5px;
		display: block;
	}
	.deck-line {
		border-top: 1px solid #d5d9d9;
		display: flex;
		gap: 8px;
		padding: 4px 5px;
		cursor: pointer;
		align-items: center;
		font-size: 15px;
	}
	.deck-line:hover {
		background-color: #e8e8e8;
	}
	.card-count-text {
		font-weight: bold;
		min-width: 20px;
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

	/* Card Grid Container - EXACT CSS from Deckbuilder */
	.card-grid-container {
		border-left: 1px solid #d5d9d9;
		width: 100%;
		height: 100%;
		overflow-y: hidden;
	}
	.card-grid-container .img-container {
		width: 100%;
		height: 55%;
		padding: 10px 0;
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
	.img-container .btn {
		background: url('./img/flip.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 15%;
		height: 11%;
		cursor: pointer;
		border: none;
		position: absolute;
		border-radius: 0px;
		box-shadow: none;
	}
	.img-container .btn:hover {
		background: url('./img/flip-hover.png') no-repeat;
		background-size: contain;
		background-position: center;
	}
	.img-container .h-img {
		transform: rotateY(0deg) rotate(90deg);
		width: 85%;
		border-radius: 3.733% / 2.677%;
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
	.card-text div { font-size: 13px; }
	.card-text .name-cost { font-size: 16px; }
	.card-text .type { font-size: 14px; }
	.card-text br { content: ""; display: block; margin-bottom: 5px; }
	
	.hidden { display: none; }

	/* images view grid */
	.spoiler-container {
		display: flex;
		flex-direction: row;
		flex-wrap: wrap;
		gap: 20px;
		margin-right: -70px;
	}
	.spoiler-section {
		width: fit-content;
		margin-bottom: 20px;
	}
	.spoiler-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, 140px);
		gap: 10px;
	}
	.spoiler-grid:last-child {
		margin-right: 70px;
	}
	.spoiler-card {
		position: relative;
		cursor: pointer;
	}
	.spoiler-card img {
		width: 100%;
		border-radius: 4.75% / 3.5%;
		display: block;
	}
	.spoiler-count {
		position: absolute;
		top: 5px;
		right: 5px;
		background: rgba(0,0,0,0.8);
		color: white;
		padding: 2px 6px;
		border-radius: 4px;
		font-size: 12px;
		font-weight: bold;
		z-index: 2;
	}
	.dropdown-container {
		display: flex;
		gap: 5px;
		align-items: center;
		font-size: 14px;
	}
	#view-select {
		margin-right: 20px;
	}
</style>
<body>
'''

	with open(os.path.join('scripts', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		html_content += f.read()

	html_content += '''
	<input type="text" id="display" class="hidden" value="cards-and-text"> <!-- for snippet compat -->
	<div class="page-container">
		<div class="deck-display-container">
			<div class="deck-main-area">
				<div class="deck-header">
					<div style="display: flex; flex-direction: column; gap: 2px;">
						<div style="display: flex; align-items: baseline; gap: 15px;">
							<div id="deck-title">Loading Deck...</div>
							<div id="deck-format" style="font-size: 16px; color: #666; font-style: italic;"></div>
						</div>
						<div id="deck-hub" style="font-size: 12px; color: #888;"></div>
					</div>
					<div class="dropdown-container">
						View cards as<select id="view-select" onchange="setView(this.value)">
							<option value="text">Text</option>
							<option value="stacks">Stacks</option>
							<option value="images">Images</option>
						</select>
						<select id="export-menu" onchange="if(this.value != 'default') exportFile(this.value)">
							<option value="default">Export ...</option>
							<option value="clipboard">Copy text</option>
							<option value="deck-image">Deck Image</option>
							<option value="export-dek">Export .dek</option>
							<option value="export-txt">Export .txt</option>
							<option value="export-cod">Export .cod</option>
						</select>
					</div>
				</div>
				<div class="deck-cards-scroll-container" id="deck-scroll-container">
				</div>
			</div>
			<div class="card-grid-container" id="card-grid-container">
			</div>
		</div>
	</div>

	<script>
		let card_list_arrayified = [];
		let currentDeck = { name: "", main: [], side: [] };
		let currentView = 'text';
		let specialchars = "";

		document.addEventListener("DOMContentLoaded", async function () {
'''

	with open(os.path.join('scripts', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		html_content += f.read()

	html_content += '''
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
			const urlParams = new URLSearchParams(window.location.search);
			const deckId = urlParams.get('id');
			
			if (deckId) {
				const { data, error } = await _supabase
					.from('decks')
					.select('*')
					.eq('id', deckId)
					.eq('hub', hubName)
					.single();

				if (error) {
					console.error('Error fetching deck:', error);
					loadDeckFromHash();
				} else {
					currentDeck = {
						name: data.name,
						format: data.format,
						main: data.mainboard,
						side: data.sideboard
					};
					document.getElementById("deck-title").innerText = currentDeck.name || "Untitled Deck";
					document.getElementById("deck-format").innerText = (currentDeck.format && currentDeck.format !== "None") ? currentDeck.format : "";
					document.title = (currentDeck.name || "Deck") + " - Magic the Egg";
					render();
					
					// Autopopulate first card
					const allCards = lookupCards(currentDeck.main.concat(currentDeck.side));
					if (allCards.length > 0) {
						showCardInGrid(allCards[0].stats);
					}
				}
			} else {
				loadDeckFromHash();
			}
		});

		function loadDeckFromHash() {
			const hash = window.location.hash.substring(1);
			if (!hash) return;
			try {
				const decoded = decodeURIComponent(escape(atob(hash)));
				if (decoded.startsWith('{')) {
					// Old JSON format
					currentDeck = JSON.parse(decoded);
				} else {
					// New compact format: Name|Format|MainCards|SideCards
					const parts = decoded.split('|');
					const name = parts[0];
					const format = parts.length > 3 ? parts[1] : "None";
					const mainStr = parts.length > 3 ? parts[2] : (parts[1] || "");
					const sideStr = parts.length > 3 ? parts[3] : (parts[2] || "");

					const parsePart = (str) => {
						if (!str) return [];
						// Try semicolon first (new format), fallback to comma (old format)
						const items = str.includes(';') ? str.split(';') : str.split(',');
						return items.map(item => {
							// Try colon first (new format), fallback to period (old format)
							const bits = item.includes(':') ? item.split(':') : item.split('.');
							return { set: bits[0], num: bits[1], count: parseInt(bits[2]), name: bits[3] };
						});
					};

					currentDeck = {
						name: name,
						format: format,
						main: parsePart(mainStr),
						side: parsePart(sideStr)
					};
				}
				document.getElementById("deck-title").innerText = currentDeck.name || "Untitled Deck";
				document.getElementById("deck-format").innerText = (currentDeck.format && currentDeck.format !== "None") ? currentDeck.format : "";
				document.title = (currentDeck.name || "Deck") + " - Magic the Egg";
				render();
				
				// Autopopulate first card
				const allCards = lookupCards(currentDeck.main.concat(currentDeck.side));
				if (allCards.length > 0) {
					showCardInGrid(allCards[0].stats);
				}
			} catch (e) {
				console.error("Failed to decode deck hash", e);
			}
		}

		function setView(view) {
			currentView = view;
			render();
		}

		function render() {
			const container = document.getElementById("deck-scroll-container");
			container.innerHTML = "";

			const mainCards = lookupCards(currentDeck.main);
			const sideCards = lookupCards(currentDeck.side);

			const categoryOrder = ["creature", "planeswalker", "sorcery", "instant", "artifact", "enchantment", "battle", "land"];
			const categoryNames = {
				"creature": "Creatures", "planeswalker": "Planeswalkers", "sorcery": "Sorceries",
				"instant": "Instants", "artifact": "Artifacts", "enchantment": "Enchantments",
				"battle": "Battles", "land": "Lands"
			};

			const categorizedMain = categoryOrder.map(key => ({
				key: key, name: categoryNames[key], cards: []
			}));

			mainCards.forEach(card => {
				const type = card.stats.type.toLowerCase();
				for (const key of categoryOrder) {
					if (type.includes(key)) {
						categorizedMain.find(cat => cat.key === key).cards.push(card);
						return;
					}
				}
			});

			const activeCategories = categorizedMain.filter(cat => cat.cards.length > 0);
			activeCategories.forEach(cat => cat.cards.sort((a,b) => a.stats.card_name.localeCompare(b.stats.card_name)));
			const sideSection = { name: "Sideboard", cards: sideCards.sort((a,b) => a.stats.card_name.localeCompare(b.stats.card_name)), key: "sideboard" };

			if (currentView === 'images') {
				const spoilerCont = document.createElement("div");
				spoilerCont.className = "spoiler-container";
				activeCategories.forEach(cat => {
					spoilerCont.appendChild(createSpoilerSection(cat));
				});
				if (sideSection.cards.length > 0) {
					spoilerCont.appendChild(createSpoilerSection(sideSection));
				}
				container.appendChild(spoilerCont);
			} else {
				const colsCont = document.createElement("div");
				colsCont.className = "deck-columns-container";
				const colEles = [document.createElement("div"), document.createElement("div"), document.createElement("div")];
				colEles.forEach(c => { c.className = "deck-col"; colsCont.appendChild(c); });

				activeCategories.forEach(cat => {
					let colIdx = 1; // Default Col 2
					if (cat.key === "creature" || cat.key === "planeswalker") colIdx = 0;
					if (cat.key === "land") colIdx = 2;
					colEles[colIdx].appendChild(createSection(cat, currentView === 'stacks'));
				});

				if (sideSection.cards.length > 0) {
					colEles[2].appendChild(createSection(sideSection, currentView === 'stacks'));
				}
				container.appendChild(colsCont);
			}
		}

		function lookupCards(codes) {
			if (!codes) return [];
			return codes.map(item => {
				const name = (item.name || item.card_name || "").trim();
				const num = item.num || item.number;
				const set = item.set;

				let stats = null;
				const notToken = (c) => !c.shape || !c.shape.includes("token");
				
				// 1. Try Set + Name + Number
				if (name && num) {
					stats = card_list_arrayified.find(c => c.set === set && c.card_name.trim() === name && c.number == num && notToken(c));
				}
				
				// 2. Try Set + Name
				if (!stats && name) {
					stats = card_list_arrayified.find(c => c.set === set && c.card_name.trim() === name && notToken(c));
				}
				
				// 3. Try Set + Number
				if (!stats && num) {
					stats = card_list_arrayified.find(c => c.set === set && c.number == num && notToken(c));
				}

				return stats ? { count: item.count, stats: stats } : null;
			}).filter(c => c !== null);
		}

		async function exportFile(export_as) {
			let deck_text = "";
			let deck_name = currentDeck.name || "Untitled Deck";

			if (export_as == "deck-image") {
				const container = document.getElementById("deck-scroll-container");
				const oldView = currentView;
				
				// Force images view if not already there
				if (currentView !== 'images') {
					setView('images');
					document.getElementById("view-select").value = "images";
				}

				// Wait for images to potentially load and layout to stabilize
				await new Promise(resolve => setTimeout(resolve, 1000));

				const spoilerCont = container.querySelector(".spoiler-container");
				if (spoilerCont) {
					const currentWidth = spoilerCont.offsetWidth;

					html2canvas(spoilerCont, {
						useCORS: true,
						allowTaint: true,
						backgroundColor: "#f3f3f3",
						scale: 2,
						logging: false,
						onclone: (clonedDoc) => {
							const cloned = clonedDoc.querySelector(".spoiler-container");
							if (cloned) {
								cloned.style.marginRight = "0";
								cloned.style.padding = "20px";
								cloned.style.background = "#f3f3f3";
								cloned.style.width = currentWidth + "px";

								// Add Title to the image
								const header = clonedDoc.createElement("div");
								header.style.marginBottom = "20px";
								header.style.width = "100%";
								header.style.borderBottom = "1px solid #898989";
								header.style.paddingBottom = "10px";
								header.style.display = "flex";
								header.style.alignItems = "baseline";
								header.style.gap = "15px";

								const title = clonedDoc.createElement("div");
								title.innerText = currentDeck.name || "Untitled Deck";
								title.style.fontFamily = "Beleren";
								title.style.fontSize = "32px";
								header.appendChild(title);

								if (currentDeck.format && currentDeck.format !== "None") {
									const format = clonedDoc.createElement("div");
									format.innerText = currentDeck.format;
									format.style.fontSize = "20px";
									format.style.color = "#666";
									format.style.fontStyle = "italic";
									header.appendChild(format);
								}

								cloned.prepend(header);
							}
						}
					}).then(canvas => {
						const link = document.createElement('a');
						link.download = deck_name + ".png";
						link.href = canvas.toDataURL("image/png");
						link.click();
					});
				}

				document.getElementById("export-menu").value = "default";
				return;
			}

			let export_cod = (export_as == "export-cod");

			if (export_cod) {
				deck_text += `<?xml version="1.0" encoding="UTF-8"?>\\n<cockatrice_deck version="1">\\n\\t<deckname>${deck_name}</deckname>\\n\\t<zone name="main">\\n`;
			}

			const mainCards = lookupCards(currentDeck.main);
			for (const card of mainCards) {
				if (export_cod) {
					deck_text += `\\t\\t<card number="${card.count}" name="${card.stats.card_name}"/>\\n`;
				} else {
					deck_text += `${card.count} ${export_as == "export-dek" ? JSON.stringify(card.stats) : card.stats.card_name}\\n`;
				}
			}

			const sideCards = lookupCards(currentDeck.side);
			if (sideCards.length > 0) {
				if (export_cod) {
					deck_text += `\\t</zone>\\n\\t<zone name="side">\\n`;
				} else {
					deck_text += "sideboard\\n";
				}
				for (const card of sideCards) {
					if (export_cod) {
						deck_text += `\\t\\t<card number="${card.count}" name="${card.stats.card_name}"/>\\n`;
					} else {
						deck_text += `${card.count} ${export_as == "export-dek" ? JSON.stringify(card.stats) : card.stats.card_name}\\n`;
					}
				}
			}

			if (export_cod) {
				deck_text += "\\t</zone>\\n</cockatrice_deck>";
			}

			if (export_as != "clipboard") {
				let downloadableLink = document.createElement('a');
				downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(deck_text));
				downloadableLink.download = deck_name + ("." + export_as.split("-")[1]);
				document.body.appendChild(downloadableLink);
				downloadableLink.click();
				document.body.removeChild(downloadableLink);
			} else {
				navigator.clipboard.writeText(deck_text);
			}

			document.getElementById("export-menu").value = "default";
		}

		function createSection(cat, isStacks) {
			const section = document.createElement("div");
			section.className = "deck-section";
			const title = document.createElement("span");
			title.className = "deck-section-title";
			const total = cat.cards.reduce((acc, curr) => acc + curr.count, 0);
			title.innerText = `${cat.name} (${total})`;
			section.appendChild(title);

			const cards_list = cat.cards;
			for (let i = 0; i < cards_list.length; i++) {
				const card = cards_list[i];
				const card_stats = card.stats;
				let card_row;

				if (!isStacks) {
					card_row = document.createElement("div");
					card_row.className = "deck-line";
					card_row.innerHTML = `<span class="card-count-text">${card.count}</span> <span>${card_stats.card_name}</span>`;
				} else {
					card_row = document.createElement("div");
					card_row.className = "card-img-container";
					if (i === cards_list.length - 1) {
						card_row.style.height = "auto";
						card_row.style.maxHeight = "100%";
					}
					const card_img = document.createElement("img");
					card_img.src = getCardImgSrc(card_stats);
					
					const fx1 = document.createElement("div"); fx1.className = "card-fx";
					const fx2 = document.createElement("div"); fx2.className = "card-fx";
					const card_count = document.createElement("div");
					card_count.className = "card-fx";
					card_count.innerText = card.count + "x";

					card_row.appendChild(fx1);
					card_row.appendChild(fx2);
					card_row.appendChild(card_count);
					card_row.appendChild(card_img);
				}

				card_row.onmouseover = function() {
					showCardInGrid(card_stats);
				};
				card_row.onclick = () => window.open(getCardUrl(card_stats), '_blank');
				section.appendChild(card_row);
			}
			return section;
		}

		function createSpoilerSection(cat) {
			const section = document.createElement("div");
			section.className = "spoiler-section";
			const title = document.createElement("span");
			title.className = "deck-section-title";
			const total = cat.cards.reduce((acc, curr) => acc + curr.count, 0);
			title.innerText = `${cat.name} (${total})`;
			section.appendChild(title);

			const grid = document.createElement("div");
			grid.className = "spoiler-grid";
			grid.style.display = "flex";
			grid.style.flexWrap = "wrap";
			grid.style.gap = "10px";

			cat.cards.forEach(card => {
				const div = document.createElement("div");
				div.className = "spoiler-card";
				div.style.width = "140px";
				div.innerHTML = `<div class="spoiler-count">${card.count}</div><img src="${getCardImgSrc(card.stats)}">`;
				div.onmouseover = () => showCardInGrid(card.stats);
				div.onclick = () => window.open(getCardUrl(card.stats), '_blank');
				grid.appendChild(div);
			});
			section.appendChild(grid);
			return section;
		}

		function showCardInGrid(card_stats) {
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

		function getCardImgSrc(card_stats) {
			const prefix = card_stats.hubURL ? card_stats.hubURL : rootPath;
			if ("position" in card_stats) {
				return prefix + "/sets/" + card_stats.set + "-files/img/" + card_stats.position + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
			}
			return prefix + "/sets/" + card_stats.set + "-files/img/" + card_stats.number + (card_stats.shape.includes("token") ? "t_" : "_") + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
		}

		function getCardUrl(card) {
			const prefix = card.hubURL ? card.hubURL : window.location.origin;
			const url = new URL(prefix + '/card', prefix);
			url.searchParams.append('set', card.set);
			url.searchParams.append('num', card.number);
			url.searchParams.append('name', card.card_name);
			return url.href;
		}

		function gridifyCard(card_stats, card_text = false, small = false, designer_notes = false) {
			const card_name = card_stats.card_name;
			rotate_card = !small && card_stats.rotated;

			if (!card_text) {
				return buildImgContainer(card_stats, true, rotate_card);			
			}
'''

	with open(os.path.join('scripts', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
		html_content += f.read()

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
'''

	with open(os.path.join('scripts', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		html_content += f.read()

	html_content += '''
		function goToSearch() {
			window.location = (rootPath + "/search?search=" + document.getElementById("search").value);
		}

		document.getElementById("search").addEventListener("keypress", function(event) {
			if (event.key === "Enter") {
				event.preventDefault();
				goToSearch();
			}
		});
'''

	with open(os.path.join('scripts', 'snippets', 'random-card.txt'), encoding='utf-8-sig') as f:
		html_content += f.read()

	html_content += '''
	</script>
</body>
</html>'''

	# Write the HTML content to the output HTML file
	with open(output_html_file, 'w', encoding='utf-8-sig') as file:
		file.write(html_content)

	print(f"HTML file saved as {output_html_file}")
