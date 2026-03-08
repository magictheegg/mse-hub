document.addEventListener("DOMContentLoaded", async () => {
	await fetch('/lists/banlist.json')
		.then(response => response.json())
		.then(json => {
			banlist = json;
		}).catch(error => console.error('Error:', error));
});

function isBannedCard(card_name) {
	return banlist.banned.includes(card_name);
}

function tokenize(text) {
	let tokens = [];

	for (let i = 0; i < text.length; i++) {
		if (i < text.length - 1) {
			if (text[i + 1] == '/') {
				tokens.push(text.substring(i, i + 3));
				i = i + 2;
			}
			else if (isDecimal(text[i]) && isDecimal(text[i + 1])) {
				tokens.push(text.substring(i, i + 2));
				i = i + 1;
			}
			else {
				tokens.push(text[i]);
			}
		}
		else {
			tokens.push(text[i]);
		}
	}

	return tokens;
}

function isDecimal(char) {
	return char >= '0' && char <= '9';
}

function symbolize(text) {
	//This isn't needed now that the { & } are put into the cost & text by the exporter
	//let tokens = tokenize(text);
	//let symText = "";
	//for (const token of tokens)
	//{
	//	symText = symText + "{" + token + "}";
	//}

	return formatTextHTML(text);
}

function formatTextHTML(str) {
	if (!str)
		return "";
	str = str.replace(/[{]([^}]+)[}]/g, function (matched, _1) {
		let letters = _1.toLowerCase()
		return `<span class="mana mana-cost ${isText(letters)} mana-` + letters + '"></span>';
	})
	return str;
}

function isText(l) {
	if (l.includes("v") || l.includes("e")) {
		return "popout";
	}
	return "";
}

function gridifyCard(card_stats, card_text = false, rotate_card = false, designer_notes = false, link = true) {
	const card_name = card_stats.card_name;
	let display_type;

	try {
		display_type = document.getElementById("display");
	} catch {
		display_type = false;
	}

	if (!card_text) return buildImgContainer(card_stats, true, rotate_card, display_type, '', link);

	const grid = document.createElement("div");
	grid.className = "image-grid";

	grid.appendChild(buildImgContainer(card_stats, false, rotate_card, display_type, '', link));

	const text = document.createElement("div");
	text.className = "card-text popout";
	text.id = "card-text";

	const name_cost = document.createElement("div");
	name_cost.className = "name-cost";
	name_cost.innerHTML = card_stats.card_name + (card_stats.cost != "" ? '     ' + symbolize(card_stats.cost) : "");
	text.appendChild(name_cost);

	const type = document.createElement("div");
	type.className = "type";
	type.textContent = card_stats.type;
	text.appendChild(type);

	const effect = document.createElement("div");
	effect.className = "effect";
	let card_effects = "";
	if (card_stats.rules_text != "") {
		card_effects = card_stats.rules_text + "\n" + (card_stats.flavor_text != "[i][/i]" ? "<hr class=\"ft-divider text-bg\"></div>" + card_stats.flavor_text : "");
	} else {
		card_effects = "";
	}

	effect.innerHTML += prettifyEffects(card_effects);
	text.appendChild(effect);

	if (card_stats.pt != "") {
		const pt = document.createElement("div");
		pt.className = "pt";
		pt.textContent = card_stats.pt;
		text.appendChild(pt);
	}
	else if (card_stats.loyalty != "") {
		const loyalty = document.createElement("div");
		loyalty.className = "pt";
		loyalty.textContent = "[" + card_stats.loyalty + "]";
		text.appendChild(loyalty);
	}

	if (designer_notes && card_stats.designer_notes != null) {
		const dnotes = document.createElement("div");
		dnotes.className = "designer-notes";
		dnotes.innerHTML = "<u><b>Designer Notes</b></u>";
		dnotes.innerHTML = dnotes.innerHTML + card_stats.designer_notes;
		text.appendChild(dnotes);
	}

	// 13-name	14-color	15-type	16-ci	17-cost	18-ability	19-pt	20-special-text	21-loyalty
	if (card_stats.shape.includes("adventure") || card_stats.shape.includes("double") || card_stats.shape.includes("spli")) {
		const name_cost_2 = document.createElement("div");
		name_cost_2.className = "name-cost";
		name_cost_2.innerHTML = card_stats.card_name2 + (card_stats.cost2 != "" ? '     ' + symbolize(card_stats.cost2) : "");
		text.appendChild(name_cost_2);

		const type_2 = document.createElement("div");
		type_2.className = "type";
		type_2.textContent = card_stats.type2;
		text.appendChild(type_2);

		const effect_2 = document.createElement("div");
		effect_2.className = "effect";
		let card_effects_2 = "";
		if (card_stats.rules_text2 != "") {
			card_effects_2 = card_stats.rules_text2 + "\n" + (card_stats.flavor_text2 != "[i][/i]" ? "<hr class=\"ft-divider text-bg\"></div>" + card_stats.flavor_text2 : "");
		} else {
			card_effects_2 = "";
		}

		effect_2.innerHTML += prettifyEffects(card_effects_2);
		text.appendChild(effect_2);

		if (card_stats.pt2 != "") {
			const pt_2 = document.createElement("div");
			pt_2.className = "pt";
			pt_2.textContent = card_stats.pt2;
			text.appendChild(pt_2);
		}
		else if (card_stats.loyalty2 != "") {
			const loyalty = document.createElement("div");
			loyalty.className = "pt";
			loyalty.textContent = "[" + card_stats.loyalty2 + "]";
			text.appendChild(loyalty);
		}
	}

	grid.appendChild(text);

	return grid;
}

function buildImgContainer(card_stats, hidden_title = false, rotate_card = false, display_type = false, img_src = "", _link = true) {
	const imgContainer = document.createElement("div");
	imgContainer.className = "img-container";
	const id = card_stats.set + "-" + card_stats.number + (display_type ? "-" + document.getElementById("display").value : "");

	const img = document.createElement("img");
	img.className = "card-image";
	img.id = id;
	img.setAttribute("loading", "lazy");
	// (card_stats[13].includes("_") ? card_stats[13] : card_stats[0]) for posterity
	img.src = img_src + "/sets/" + card_stats.set + "-files/img/" + card_stats.number + (card_stats.shape.includes("token") ? "t_" : "_") + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;

	// let not_in_voyager;

	// if (card_stats.set == "HEL") {
	// 	img.style.filter = "grayscale()";

	// 	not_in_voyager = document.createElement("span");
	// 	not_in_voyager.className = "not-in-voyager";
	// 	not_in_voyager.innerText = "This card is no longer legal in voyager.";
	// }

	let banned_overlay;

	if (isBannedCard(card_stats.card_name)) {
		banned_overlay = document.createElement("div");
		banned_overlay.className = "banned-overlay";
	}

	const link = document.createElement("a");

	if (_link) {
		const url = new URL('card', window.location.origin);
		const params = {
			set: card_stats.set,
			num: card_stats.number,
			name: card_stats.card_name
		}
		for (const key in params) {
			url.searchParams.append(key, params[key]);
		}
		link.href = url;
	}

	link.appendChild(img);

	if ((card_stats.shape.includes("spli") || card_stats.type.includes("Battle")) && rotate_card) {
		const rotated_img = document.createElement("img");
		rotated_img.className = "h-img";
		rotated_img.id = "h-img";
		rotated_img.src = img.src;
		rotated_img.style.display = "block";
		img.style.filter = "blur(2px) brightness(0.7)";

		link.appendChild(rotated_img);
	}

	imgContainer.appendChild(link);

	if (card_stats.shape.includes("double")) {
		const imgFlipBtn = document.createElement("button");
		imgFlipBtn.className = "btn";
		imgFlipBtn.onclick = async function () { imgFlip(id, rotate_card); };
		const imgFlipIcon = document.createElement("img");
		imgFlipIcon.className = "img-flip-icon";
		imgFlipIcon.src = '/img/flip.svg';
		imgFlipBtn.appendChild(imgFlipIcon);
		imgContainer.appendChild(imgFlipBtn);
	}

	if (hidden_title) {
		const title = document.createElement("div");
		title.innerText = card_stats.card_name;
		title.className = "hidden-text text";
		imgContainer.appendChild(title);
	}

	// if (not_in_voyager) {
	// 	imgContainer.appendChild(not_in_voyager);
	// }

	if (banned_overlay) {
		imgContainer.appendChild(banned_overlay);
	}

	return imgContainer;
}

async function imgFlip(id, rotate_card = false) {
	const img = document.getElementById(id);
	const seconds = 0.15;
	const cardName = img.src;

	img.style.transition = seconds.toString() + "s";
	img.style.transform = "rotateY(90deg)";

	const btn = img.parentElement.parentElement.getElementsByTagName("button")[0];
	btn.style.transition = seconds.toString() + "s";
	btn.style.filter = cardName.includes("_front") ? "invert()" : "";

	await setTimeout(function () {
		const rotated_img = document.getElementById("h-img");

		if (cardName.includes("_front")) {
			img.src = cardName.replace("_front", "_back");
			img.parentElement.parentElement.getElementsByTagName("button")[0].style.filter = "invert()";

			if (rotate_card) {
				rotated_img.style.display = "none";
				img.style.filter = "";
			}
		}
		else {
			img.src = cardName.replace("_back", "_front");
			img.parentElement.parentElement.getElementsByTagName("button")[0].style.filter = "";

			if (rotate_card) {
				rotated_img.style.display = "block";
				img.style.filter = "blur(2px) brightness(0.7)";
			}
		}

		img.style.transition = (seconds * 2).toString() + "s";
		img.style.transform = "rotateY(0deg)";
	}, seconds * 1000);

	await setTimeout(function () {
		console.log("done");
	}, seconds * 1000);
}

function prettifyEffects(card_effect) {
	let HTML = "";

	let styled_effect = card_effect.replaceAll("[i]", "<i>").replaceAll("[/i]", "</i>").replaceAll("[b]", "<b>").replaceAll("[/b]", "</b>");
	let card_effects = styled_effect.split("\n");

	for (let i = 0; i < card_effects.length; i++) {
		HTML += card_effects[i];

		if (i != card_effects.length - 1) {
			HTML += "<br>"
		}
	}

	let regexHTML = symbolize(HTML);

	return regexHTML;
}