import os
import sys
import json

#F = Fungustober's notes

def generateHTML(codes, username):
	output_html_file = "search.html"

	# Start creating the HTML file content
	html_content = '''<html>
<head>
	<title>Search</title>
	<link rel="icon" type="image/x-icon" href="/img/search.png">
	<link rel="stylesheet" href="resources/mana.css">
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
	.button-grid {
		width: 70%;
		max-width: 1200px;
		height: 40px;
		margin: auto;
		display: grid;
		grid-template-columns: 4fr 1fr;
		gap: 10px;
		padding-top: 20px;
		padding-bottom: 20px;
		justify-items: center;
	}
	.prev-next-btns {
		width: 100%;
		height: 40px;
		margin: auto;
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 5px;
		align-items: center;
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
	button:disabled {
		cursor: auto;
		background-color: #f7fafa;
		font-style: italic;
		box-shadow: none;
		color: #cccccc;
	}
	.button-grid .results-text {
		margin-right: -3px;
	}
	.button-grid .select-text {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: left;
		gap: 8px;
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
	.grid-container {
		display: grid;
		grid-template-columns: auto;
		max-width: 1200px;
		margin: auto;
	}
	.image-grid-container {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		width: 70%;
		max-width: 1200px;
		margin: auto;
		gap: 5px;
		justify-items: center;
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
		background: url('img/flip.png') no-repeat;
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
		background: url('img/flip-hover.png') no-repeat;
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
	}
	.img-container .hidden-text {
		position: absolute;
		font-family: Beleren;
		top: 5%;
		left: 9%;
		font-size: .97vw;
		color: rgba(0, 0, 0, 0);
	}
</style>
<body>
	'''

	with open(os.path.join('resources', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
		snippet = f.read().replace('USERNAME', username)
		html_content += snippet

	html_content += '''
	<div class="button-grid">
		<div class="select-text"><div class="results-text" id="results-text">Loading ...</div>Cards displayed as<select name="display" id="display"><option value="cards-only">Cards Only</option><option value="cards-text">Cards + Text</option></select>sorted by<select name="sort-by" id="sort-by"><option value="name">Name</option><option value="set-code">Set / Number</option><option value="mv">Mana Value</option><option value="color">Color</option><option value="rarity">Rarity</option></select> : <select name="sort-order" id="sort-order"><option value="ascending">Asc</option><option value="descending">Desc</option></select></div>		
		<div class="prev-next-btns">
			<button type="submit" onclick="previousPage()" id="prevBtn" disabled>< Previous</button>
			<button type="submit" onclick="nextPage()" id="nextBtn">Next 30 ></button>
		</div>
	</div>

	<div class="grid-container" id="grid">
	</div>

	<div class="image-grid-container" id="imagesOnlyGrid">
	</div>

	<div class="button-grid" id="footer">
		<div></div>
		<div class="prev-next-btns">
			<button type="submit" onclick="previousPage()" id="prevBtn-footer" disabled>< Previous</button>
			<button type="submit" onclick="nextPage()" id="nextBtn-footer">Next 30 ></button>
		</div>
	</div>

	<script>
		let page = 0;
		let pageCount = 30;
		let search_results = [];
		let card_list_arrayified = [];
		let specialchars = "";

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
			if (sessionStorage.getItem("display") != "cards-only")
			{
				cardGrid = document.getElementById("grid");
			}
			else
			{
				cardGrid = document.getElementById("imagesOnlyGrid");
			}

			card_list_arrayified.sort(compareFunction);

			page = window.location.href.indexOf("page=") == -1 ? 0 : parseInt(window.location.href.substring(window.location.href.indexOf("page=") + 5)) - 1;

			// refresh page values
			let params = decodeURIComponent(window.location.href.indexOf("?search") == -1 ? "" : window.location.href.substring(window.location.href.indexOf("?search") + 8));
			document.getElementById("search").value = (params.indexOf("&page=") == -1 ? params.replaceAll("+", " ") : params.substring(0, params.indexOf("&page=")).replaceAll("+", " "));
			if (sessionStorage.getItem("sortMethod"))
			{
				document.getElementById("sort-by").value = sessionStorage.getItem("sortMethod");				
			}
			if (sessionStorage.getItem("display"))
			{
				document.getElementById("display").value = sessionStorage.getItem("display");				
			}

			displayStyle = document.getElementById("display").value;
			setCardView();

			// initial search on load
			preSearch(false);
		});

		function displayChangeListener() {
			displayStyle = document.getElementById("display").value;
			sessionStorage.setItem("display", displayStyle);
			sessionStorage.setItem("sortMethod", document.getElementById("sort-by").value);

			setCardView();

			preSearch(false);
		}

		document.getElementById("sort-by").onchange = displayChangeListener;
		document.getElementById("display").onchange = displayChangeListener;
		document.getElementById("sort-order").onchange = displayChangeListener;

		window.addEventListener('popstate', function(event) {
			let params = decodeURIComponent(window.location.href.indexOf("?search") == -1 ? "" : window.location.href.substring(window.location.href.indexOf("?search") + 8), (window.location.href.indexOf("page=") == -1 ? window.location.href.length : window.location.href.indexOf("page=")));
			document.getElementById("search").value = (params.indexOf("&page=") == -1 ? params.replaceAll("+", " ") : params.substring(0, params.indexOf("&page=")).replaceAll("+", " "));
			page = window.location.href.indexOf("page=") == -1 ? 0 : parseInt(window.location.href.substring(window.location.href.indexOf("page=") + 5)) - 1;

			preSearch(false);
		});

		function setCardView() {
			imagesOnlyGrid.style.display = displayStyle == "cards-only" ? '' : 'none';
			grid.style.display = displayStyle == "cards-only" ? 'none' : '';
		}

		'''

	with open(os.path.join('resources', 'snippets', 'compare-function.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	#F: I've added in a bunch of additional variables to allow people to search DFCs by info on their back faces
	#F: For example, let's say I want to find Delver of Secrets by searching for a 3/2 (which is the p/t of Insectile Aberration)
	#F: Alas, I don't know how to incorporate this into the search, so I will leave that up to other people.
	html_content += '''

		function preSearch(setNewState) {
			card_list_arrayified.sort(compareFunction);
			if (document.getElementById("sort-order").value == "descending")
			{
				card_list_arrayified.reverse();
			}
			search_results = [];
			page = setNewState ? 0 : page;

			search(setNewState);
		}

		function search(setNewState) {
			searchTerms = document.getElementById("search").value.toLowerCase();

			if (searchTerms != "")
			{
				if (setNewState)
				{
					let url = (window.location.href.indexOf("?") == -1 ? new URL(window.location.href) : new URL(window.location.href.substring(0, window.location.href.indexOf("?"))));
					let params = new URLSearchParams(url.search);
					params.append("search", searchTerms);
					history.pushState({}, '', url.pathname + '?' + params.toString());
				}
			}
			else
			{
				if (setNewState)
				{
					let url = (window.location.href.indexOf("?") == -1 ? new URL(window.location.href) : new URL(window.location.href.substring(0, window.location.href.indexOf("?"))));
					let params = new URLSearchParams(url.search);
					params.delete("search");
					history.pushState({}, '', url.pathname + '' + params.toString());
				}
			}

			if (displayStyle == "cards-only")
			{
				cardGrid = document.getElementById("imagesOnlyGrid");
			}
			else
			{
				cardGrid = document.getElementById("grid");
			}
			cardGrid.innerHTML = "";

			for (const card of card_list_arrayified) {
				if (card.shape.includes("token") && !searchTerms.includes("*t:token") && !searchTerms.includes("t:token"))
				{
					continue;
				}

				if (card.type.includes("Basic") && !searchTerms.includes("*t:basic") && !searchTerms.includes("t:basic"))
				{
					continue;
				}

				searched = searchAllTokens(card, tokenizeTerms(searchTerms));

				if (searched && !containsCard(search_results, card))
				{
					search_results.push(card);
				}
			}

			if (searchTerms != "")
			{
				document.getElementById("results-text").innerText = search_results.length + (search_results.length == 1 ? " result found." : " results found.");
			}
			else
			{
				document.getElementById("results-text").innerText = "";
			}

			if (page != 0)
			{
				document.getElementById("prevBtn").disabled = false;
				document.getElementById("prevBtn-footer").disabled = false;
			}
			else
			{
				document.getElementById("prevBtn").disabled = true;
				document.getElementById("prevBtn-footer").disabled = true;
			}

			// set text of Next to match number of displayed images
			displayStyle = document.getElementById("display").value;
				pageCount = displayStyle == "cards-only" ? 60 : 30;
				document.getElementById("nextBtn").innerText = "Next " + pageCount + " >";
				document.getElementById("nextBtn-footer").innerText = "Next " + pageCount + " >";

				// really awesome code block to fix the URL when switching from Cards + Text view to Cards Only view
				while ((pageCount * page) > search_results.length)
				{
					page = page - 1;

					let url = (window.location.href.indexOf("page=") == -1 ? new URL(window.location.href) : new URL(window.location.href.substring(0, window.location.href.indexOf("page="))));
				let params = new URLSearchParams(url.search);
				params.append("page", page+1);
				history.replaceState({}, '', url.pathname + '?' + params.toString());
				}

			for (let i = (pageCount * page); i < Math.min((pageCount * (page + 1)), search_results.length); i++)
			{
				cardGrid.appendChild(gridifyCard(search_results[i]));
			}

			if (search_results.length <= (pageCount * (page + 1)))
			{
				document.getElementById("nextBtn").disabled = true;
				document.getElementById("nextBtn-footer").disabled = true;
			}
			else
			{
				document.getElementById("nextBtn").disabled = false;
				document.getElementById("nextBtn-footer").disabled = false;
			}
		}

		function containsCard(list, card)
		{
			for (const li of list)
			{
				if (li[0] == card.card_name && li[3] == card.type)
				{
					return true;
				}
			}

			return false;
		}

		function tokenizeTerms(searchTerms)
		{
			let searchTokens = [];
			let key = 0;
			let inParens = false;
			let inQuotes = false;
			for (let i = 0; i < searchTerms.length; i++)
			{
				if (searchTerms.charAt(i) == '(')
				{
					inParens = true;
				}
				if (searchTerms.charAt(i) == ')')
				{
					inParens = false;
				}
				if (!inParens && !inQuotes && (searchTerms.charAt(i) == '"' || searchTerms.charAt(i) == '“' || searchTerms.charAt(i) == '/'))
				{
					inQuotes = true;
				}
				else if (!inParens && inQuotes && (searchTerms.charAt(i) == '"' || searchTerms.charAt(i) == '”' || searchTerms.charAt(i) == '/'))
				{
					inQuotes = false;
				}
				if (searchTerms.charAt(i) == ' ' && !inParens && !inQuotes)
				{
					searchTokens.push(searchTerms.substring(key, i));
					key = i + 1;
				}
				if (i == searchTerms.length - 1)
				{
					searchTokens.push(searchTerms.substring(key));
				}
			}

			return searchTokens;
		}

		function searchAllTokens(card, tokens)
		{
			if (tokens.length < 1)
			{
				return true;
			}
			for (let i = 0; i < tokens.length; i++)
			{
				if (tokens[i].charAt(0) == '*')
				{
					return searchAllTokens(card, tokens.slice(0, i)) && searchAllTokens(card, tokens.slice(i + 1));
				}
				if (tokens[i] == "or")
				{
					return searchAllTokens(card, tokens.slice(0, i)) || searchAllTokens(card, tokens.slice(i + 1));
				}
			}

			for (let token of tokens)
			{
				if (token.charAt(0) == '-')
				{
					return !searchToken(card, token.substring(1)) && (tokens.length == 1 ? true : searchAllTokens(card, tokens.slice(1)));
				}
				if (token.charAt(0) == '(')
				{
					return searchAllTokens(card, tokenizeTerms(token.substring(1, token.length - 1))) && (tokens.length == 1 ? true : searchAllTokens(card, tokens.slice(1)));
				}
				else
				{
					return searchToken(card, token) && (tokens.length == 1 ? true : searchAllTokens(card, tokens.slice(1)));
				}
			}
		}

		function searchToken(card, token)
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

			let card_name = card_stats.card_name;
			let card_color = card_stats.color != "" ? card_stats.color : "c";
			let card_rarity = card_stats.rarity;
			let card_type = card_stats.type;
			// 4: collector number
			let card_ci = card_stats.color_identity;
			let card_cost = card_stats.cost;
			let card_mv = (isDecimal(card_cost.charAt(0)) ? parseInt(card_cost) + card_cost.replaceAll('x','').length - 1 : card_cost.replaceAll('x','').length) - ((card_cost.split('/').length - 1) * 2);
			//Strip out the lingering [i][/i] and [b][/b] tags while we're searching just in case someone decided to bold something in the
			//middle of their rules text for some reason
			let card_oracle_text = card_stats.rules_text != "" ? card_stats.rules_text.replace(/\[(\/)?([ib])\]/g, "") : card_stats.special_text.replace(/\[(\/)?([ib])\]/g, "");
			let card_power = card_stats.pt.substring(0,card_stats.pt.indexOf('/'));
			let card_toughness = card_stats.pt.substring(card_stats.pt.indexOf('/')+1);
			let card_shape = card_stats.shape;
			let card_set = card_stats.set;
			let card_loyalty = card_stats.loyalty;
			let card_notes = card_stats.notes;
			let card_color_2 = "";
			let card_cost_2 = "";
			let card_power_2 = "";
			let card_toughness_2 = "";
			let card_loyalty_2 = ""

			// two cards in one
			if (card_shape.includes("adventure") || card_shape.includes("double") || card_shape.includes("spli"))
			{
				card_name = card_name + "	" + card_stats.card_name2;
				card_type = card_type + "	" + card_stats.type2;
				card_oracle_text = card_oracle_text + "	" + (card_stats.rules_text2 != "" ? card_stats.rules_text2.replace(/\[(\/)?([ib])\]/g, "") : card_stats.special_text2.replace(/\[(\/)?([ib])\]/g, ""));
				card_color_2 = card_stats.color2 != "" ? card_stats.color2 : "c";
				card_cost_2 = card_stats.cost2;
				card_power_2 = card_stats.pt2.substring(0,card_stats.pt2.indexOf('/'));
				card_toughness_2 = card_stats.pt.substring(card_stats.pt.indexOf('/')+1);
				card_loyalty_2 = card_stats.loyalty2;
			}

			token = token.replaceAll("~", card_name).replaceAll("cardname", card_name).replaceAll('"','').replaceAll('/','').replaceAll('“','').replaceAll('”','');

			const modifierRegex = /[!:<>=]/;
			const match = token.search(modifierRegex);

			if (match > -1)
			{
				const term = token.substring(0, match);
				const modifier = token.charAt(match);
				let check = token.substring(match + 1);

				// availableTokens = ["mv", "c", "ci", "t", "o", "pow", "tou", "r", "is"]

				/* template
				if (term == "mv")
				{
					if (modifier == "!" || modifier == "=")
					{

					}
					else if (modifier == ":")
					{

					}
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					}
				} */
				if (term == "mv")
				{
					if (modifier == "!" || modifier == "=")
					{
						return (card_mv == check);
					}
					else if (modifier == ":")
					{
						return (card_mv == check);
					}
					else if (modifier == "<")
					{
						return (card_mv < check);
					}
					else if (modifier == ">")
					{
						return (card_mv > check);
					}
				}
				if (term == "c" || term == "color")
				{
					if (modifier == "!" || modifier == "=")
					{
						if (!isNaN(check))
						{
							return card_color.length == parseInt(check);
						}
						return (card_color.split("").sort().join("") == check.split("").sort().join(""));
					}
					else if (modifier == ":")
					{
						if (!isNaN(check))
						{
							return card_color.length == parseInt(check);
						}
						return hasAllChars(card_color, check);
					}
					else if (modifier == "<")
					{
						if (!isNaN(check))
						{
							return card_color.length < parseInt(check);
						}
						return hasNoChars(card_color, check);
					}
					else if (modifier == ">")
					{
						if (!isNaN(check))
						{
							return card_color.length > parseInt(check);
						}
						return hasAllAndMoreChars(card_color, check);
					}
				}
				if (term == "ci")
				{
					if (modifier == "!" || modifier == "=")
					{
						// why is this the best way to do this?
						if (!isNaN(check))
						{
							return card_ci.length == parseInt(check);
						}
						return (card_ci.split("").sort().join("") == check.split("").sort().join(""));
					}
					else if (modifier == ":")
					{
						if (!isNaN(check))
						{
							return card_ci.length == parseInt(check);
						}
						return hasAllChars(card_ci, check);
					}
					else if (modifier == "<")
					{
						if (!isNaN(check))
						{
							return card_ci.length < parseInt(check);
						}
						return hasNoChars(card_ci, check);
					}
					else if (modifier == ">")
					{

						if (!isNaN(check))
						{
							return card_ci.length > parseInt(check);
						}
						return hasAllAndMoreChars(card_ci, check);
					}
				}
				if (term == "t" || term == "type")
				{
					if (modifier == ":")
					{
						return card_type.includes(check);
					}
					/* unsupported flows
					if (modifier == "!" || modifier == "=")
					{

					}
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					} */
				}
				if (term == "o")
				{
					if (modifier == ":")
					{
						regex = new RegExp(check);
						return regex.test(card_oracle_text);
					}
					/* unsupported flows
					if (modifier == "!" || modifier == "=")
					{

					}
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					} */
				}
				if (term == "pow")
				{
					if (modifier == "!" || modifier == "=")
					{
						return (card_power == check);
					}
					else if (modifier == ":")
					{
						return (card_power == check);
					}
					else if (modifier == "<")
					{
						return (card_power < check);
					}
					else if (modifier == ">")
					{
						return (card_power > check);
					}
				}
				if (term == "tou")
				{
					if (modifier == "!" || modifier == "=")
					{
						return (card_toughness == check);
					}
					else if (modifier == ":")
					{
						return (card_toughness == check);
					}
					else if (modifier == "<")
					{
						return (card_toughness < check);
					}
					else if (modifier == ">")
					{
						return (card_toughness > check);
					}
				}
				if (term == "r" || term == "rarity")
				{
					rarities = [ "common", "uncommon", "rare", "mythic" ];
					for (const rarity of rarities)
					{
						if (rarity.startsWith(check))
						{
							check = rarity;
						}
					}
					if (modifier == ":" || modifier == "!" || modifier == "=")
					{
						return (card_rarity == check);
					}
					else if (modifier == "<")
					{
						return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) < rarities.indexOf(check);
					}
					else if (modifier == ">")
					{
						return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) > rarities.indexOf(check);
					}
				}
				if (term == "e" || term == "set")
				{
					if (modifier == ":" || modifier == "!" || modifier == "=")
					{
						return (card_set == check);
					}
					/* unsupported flows
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					} */
				}
				if (term == "keyword" || term=="kw" || term == "has")
				{
					if (modifier == ":" || modifier == "!" || modifier == "=")
					{
						regex_kw1 = new RegExp(`(^|newline|, )${check}[^.]*($|newline|\\\\()`, "g");
						regex_kw2 = new RegExp(`(^|newline)${check} `, "g");
						return regex_kw1.test(card_oracle_text) || regex_kw2.test(card_oracle_text);
					}
					/* unsupported flows
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					} */
				}
				if (term == "is")
				{
					if (modifier == ":" || modifier == "!" || modifier == "=")
					{
						// all of these are implemented individually
						if (check == "permanent")
						{
							return !card_type.includes("instant") && !card_type.includes("sorcery");
						}
						if (check == "spell")
						{
							return !card_type.includes("land");
						}
						if (check == "commander")
						{
							return (card_type.includes("legendary") && card_type.includes("creature")) || card_oracle_text.includes("can be your commander");
						}
						if (check == "hybrid")
						{
							return (card_cost.includes("/"));
						}
					}
					/* unsupported flows
					else if (modifier == "<")
					{

					}
					else if (modifier == ">")
					{

					} */
				}
				if (term == "tag")
				{
					if (modifier == ":" || modifier == "=" || modifier == "!")
					{
						return card_notes.includes("!tag " + check);
					}
				}
			}

			return card_name.includes(token);
		}

		'''

	with open(os.path.join('resources', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function gridifyCard(card_stats) {
			const card_name = card_stats.card_name;

			if (displayStyle == "cards-only")
			{
				return buildImgContainer(card_stats, true);
			}

		'''

	with open(os.path.join('resources', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

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

		document.getElementById("search").addEventListener("keypress", function(event) {
			if (event.key === "Enter") {
			event.preventDefault();
			preSearch(true);
			}
		});

		function previousPage() {
			page = page - 1;
			cardGrid.innerHTML = "";

			let url = (window.location.href.indexOf("page=") == -1 ? new URL(window.location.href) : new URL(window.location.href.substring(0, window.location.href.indexOf("page="))));
			let params = new URLSearchParams(url.search);
			if (page != 0)
			{
				params.append("page", page+1);
			}
			history.pushState({}, '', url.pathname + '?' + params.toString());

			for (let i = (pageCount * page); i < Math.min((pageCount * (page + 1)), search_results.length); i++)
			{
				cardGrid.appendChild(gridifyCard(search_results[i]));
			}

			document.getElementById("nextBtn").disabled = false;
			document.getElementById("nextBtn-footer").disabled = false;
			if (page == 0)
			{
				document.getElementById("prevBtn").disabled = true;
				document.getElementById("prevBtn-footer").disabled = true;
			}

			document.body.scrollTop = 0; // For Safari
				document.documentElement.scrollTop = 0; // For real browsers
		}

		function nextPage() {
			page = page + 1;
			
			let url = (window.location.href.indexOf("page=") == -1 ? new URL(window.location.href) : new URL(window.location.href.substring(0, window.location.href.indexOf("page="))));
			let params = new URLSearchParams(url.search);
			params.append("page", page+1);
			history.pushState({}, '', url.pathname + '?' + params.toString());

			cardGrid.innerHTML = "";

			for (let i = (pageCount * page); i < Math.min((pageCount * (page + 1)), search_results.length); i++)
			{
				cardGrid.appendChild(gridifyCard(search_results[i]));
			}

			document.getElementById("prevBtn").disabled = false;
			document.getElementById("prevBtn-footer").disabled = false;
			if (search_results.length <= (pageCount * (page + 1)))
			{
				document.getElementById("nextBtn").disabled = true;
				document.getElementById("nextBtn-footer").disabled = true;
			}

			document.body.scrollTop = 0; // For Safari
				document.documentElement.scrollTop = 0; // For real browsers
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