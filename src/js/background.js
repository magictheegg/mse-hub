

function prepareGradients() {
	let defaultGradient = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt = document.createElement("option");
	opt.value = defaultGradient.replace(' ', '-');
	opt.text = defaultGradient;
	try { document.getElementById("color-select").appendChild(opt); } catch {}
	let random_card = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt_rand = document.createElement("option");
	opt_rand.value = "Random-Card";
	opt_rand.text = "Random Card";

	try { document.getElementById("color-select").appendChild(opt_rand); } catch {}
	for (const gradient of gradients) {
		const opt = document.createElement("option");
		opt.value = gradient.name.replace(' ', '-');
		opt.text = gradient.name;
		if (gradient.name != defaultGradient) {
			try { document.getElementById("color-select").appendChild(opt); } catch {}
		}
	}

	for (const gradient in card_backgrounds) {
		const opt = document.createElement("option");
		opt.value = gradient.replace(' ', '-');
		opt.text = gradient;
		if (gradient.name != defaultGradient) {
			try { document.getElementById("color-select").appendChild(opt); } catch {}
		}
	}
}

function setGradient(gradient = false) {
	let artistCredit = "";
	if (!gradient) {
		gradient = document.getElementById("color-select").value;
	}

	gradTop = "#000000";
	gradBottom = "#FFFFFF";
	for (const grad of gradients) {
		if (gradient == grad.name.replace(' ', '-')) {
			gradImage = `linear-gradient(to bottom, ${grad.color1}, ${grad.color2})`
		}
	}

	for (const background in card_backgrounds) {
		if (gradient == background.replace(' ', '-')) {
			gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
			artistCredit = card_backgrounds[background][0];
			setTextColor(card_backgrounds[background][1]);
		}
	}

	if (gradient == "Random-Card") {
		const bgs = Object.keys(card_backgrounds);
		const background = bgs[reallyRand(bgs.length)];
		gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
		artistCredit = card_backgrounds[background][0];
		setTextColor(card_backgrounds[background][1]);
	}


	document.body.style.backgroundImage = gradImage;
	localStorage.setItem("settings.gradient", gradient);
	console.log("CHANGE");
	if (document.getElementsByClassName("artist-credit")[0])
		document.getElementsByClassName("artist-credit")[0].remove();
	const credit_text = document.createElement("span");
	credit_text.className = "artist-credit text";
	credit_text.innerText = `background by ${artistCredit}`;
	if (artistCredit && document.getElementById("color-select"))
		document.getElementById("color-select").parentElement.appendChild(credit_text);
}

function reallyRand(x, seed = false) {
	const date = new Date();
	seed = seed ? seed : date.getUTCFullYear() * 10000 +
		date.getUTCMonth() * 100 +
		date.getUTCDate();

	const a = 1103515245;
	const c = 12345;
	const m = Math.pow(2, 31);

	let randomNumber = (a * seed + c) % m;
	randomNumber = randomNumber / m;

	return Math.floor(randomNumber * x);
}

function setTextColor(c = false) {
	if (c) {
		localStorage.setItem("settings.textcolor", c);
	}
	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));
}

function defaultSetting(name, default_) {
	// if you dont have a value in localstorage, set that value to default_
	if (localStorage.getItem(name) == null) {
		localStorage.setItem(name, default_);
	}
}

function toggleHeader() {
	const header = document.querySelector('.header');
	header.style.transform = header.style.transform === '' ? 'translate(0)' : '';
}

document.addEventListener("DOMContentLoaded", async () => {
	defaultSetting('settings.autosave', 'On');
	defaultSetting('settings.searchalias', 'On');
	defaultSetting('settings.exportcube', 'On');
	defaultSetting('settings.maxcopies', 'On');
	defaultSetting('settings.sanctumbasic', 'On');
	defaultSetting('settings.textcolor', 'Black');
	defaultSetting('settings.gradient', 'Random-Card');
	defaultSetting('settings.format', 'Eternal');
	defaultSetting('settings.deck_privacy', 'Public');
	defaultSetting("settings.compactaccount", "Off");
	defaultSetting("settings.resultgradient", "On");
	defaultSetting("settings.darktheme", "Off");
	defaultSetting("settings.theme", "Light");

	let theme = localStorage.getItem("settings.theme");

	if (!theme && localStorage.getItem("settings.darkthememenu") == "On") {
		theme = "Dark";
	}
	if (!theme && localStorage.getItem("settings.darkthememenu") == "Off") {
		theme = "Light";
	}

	document.body.dataset.theme = theme;

	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));

	try {
		const response = await fetch('/data/gradients.json');
		raw_gradients = await response.json();
	}
	catch (error) {
		console.error('Error:', error);
	}

	gradients = raw_gradients.gradients;
	card_backgrounds = raw_gradients.cards;
	setGradient(localStorage.getItem("settings.gradient"));
	prepareGradients();

	if (window.location.href.includes('#nobg')) {
		document.body.style.background = 'rgba(0,0,0,0)';
		document.querySelector('.header').style.display = 'none';
	}
});

function closeModal() {
	document.getElementById("modal-container").style.display = "none";
}