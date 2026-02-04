import { initializeApp } from "firebase/app";
import { setDoc, addDoc, updateDoc, doc, collection, getFirestore, query, where, getDocs, getDoc, deleteDoc } from "firebase/firestore";
import * as fs from "fs"

function isWish(card) {
    const regex = /(reveal|put) (.*?) from your sanctum/gi;

    return regex.test(card.rules_text) && !/^pathbound/gi.test(card.rules_text);
}

function isWipe(card) {
    const regex = /(((destroy|exile) (all|each)( other)? creatures?)|(deals [0-9]+? damage to each [^\n]*? ?creature)|(each ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ gets [+-][0-9]+?\/-[0-9]+?)|((put|return) each ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ (to its owner['’]s hand|on (the)? ?(top|bottom)|(into its owner['’]s sanctum))))/gi;

    return regex.test(card.rules_text);
}

function isCA(card) { // (play|cast) ([^\\n.]+ (from exile|exiled)|(one of )?those cards|them|it this turn|it until)
    const regex = /(Clue token|[Ii]nvestigate)|[Dd]raw|[Dd]raft|(play|cast) ([^\n.]+ (from exile|exiled)|(one of )?those cards|them|it this turn|it until)|(graveyard to|into) your hand|\b(?:return\W+(?:\w+\W+){0,5}?to your hand|to your hand\W+(?:\w+\W+){0,5}?return)\b/gi;

    return regex.test(card.rules_text);
}


function isRemoval(card) {
    const regex = /(destroy)|(deals [0-9]+? damage to (any|target|each) (creature|nonplayer|target|planeswalker))|((target|each) (player|opponent) sacrifices?)|(Exile (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ ?[^c][^a][^r][^d])|(fights)|(return (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ to its owner['’]s hand)|(loses? all abilities)|(can['’]t attack or block)|(doesn['’]t untap during its controllers untap)|((target|each) (((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+) gets [+-][0-9X]+?\/-[1-9X]+?)|(put (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ on the (top|bottom))/gi;
    
    if (isWipe(card)) return false;
    if (card.rules_text.match(/exile/i) && card.rules_text.match(/return it to the/i)) return false;
    if (card.rules_text.match(/(named|copies of) (spark|through violence)/i)) return false;

    return regex.test(card.rules_text);
}

function isRecurrable(card) {
    const re = `((You may cast (this card|${card.card_name}) from your graveyard)|(return (this card|${card.card_name}) from your graveyard)|(put (this card|${card.card_name}) from your graveyard))`;
    const regex = new RegExp(re, "gi");

    return regex.test(card.rules_text);
}

function isUtilityLand(card) {
    const regex = /({.}+?): [^a][^d][^d].*/gi;

    return regex.test(card.rules_text) && card.type.match(/land/i) && !card.card_name.match(/drifting/i);
}

function isDiscard(card) {
    const regex = /(look at (target|each|an?) (player|opponent)('s)? hand)|((target|each|an?) (player|opponent) reveals [^\n]+? hand)|((player|opponent) discards)/gi;
    return regex.test(card.rules_text);
}

function isPermanent(card) {
    return !card.type.match(/instant|sorcery/i);
}

function isTutor(card) {
    const searchRegex = /search your library for a [^\n]+?card/gi;
    const landRegex = /search your library for a [^\n]*?(land|plains|island|swamp|mountain|forest|fault) card/gi;
    return searchRegex.test(card.rules_text) && !landRegex.test(card.rules_text);
}

function isCounterspell(card) {
    return /counter target [\w^\n]*? ?spell/gi.test(card.rules_text);
}

function isThreat(card) {
    return card.type.match(/creature/gi) && !card.rules_text.match(/^pathbound/gi);
}

function isRamp(card) {
    return /Treasure token|[Aa]dd ({|(one|two|three|X) mana|an amount of {|)|additional land|\b(?:((land|Plains|Island|Swamp|Mountain|Forest|Fault))\W+(?:\w+\W+){0,6}?the battlefield)\b|(land|Plains|Island|Swamp|Mountain|Forest|Fault) token /gi.test(card.rules_text) && !/land/gi.test(card.type);
}

const compendium_rules = {
    Interaction: {
        'Small Removal': card => convertToMV(card.cost) < 4 && isRemoval(card) && card.rules_text.match(/(\/-[1-4X])|(deals [1-4])|(mana value [1-3])|((power|toughness) [1-3])/gi),
        'Unconditional Removal': card => isRemoval(card) && card.rules_text.match(/exile target|destroy/gi) && !isInCategory(card, 'Interaction', 'Small Removal') && !card.rules_text.match(/target (artifact|enchantment)/gi),
        'Other Removal': card => isRemoval(card) && !isInCategory(card, 'Interaction', 'Small Removal') && !isInCategory(card, 'Interaction', 'Unconditional Removal'),
        'Countermagic': card => isCounterspell(card),
        'Boardwipes': card => isWipe(card),
        'Discard': card => isDiscard(card)
    },
    Threats: {
        'Early Threats': card => isThreat(card) && !isCA(card) && convertToMV(card.cost) < 3,
        'Midrange Threats': card => isThreat(card) && convertToMV(card.cost) < 5 && convertToMV(card.cost) > 2,
        'Topend Threats': card => isThreat(card) && convertToMV(card.cost) > 4
    },
    Value: {
        'Draw/Selection': card => isCA(card) && !card.type.match(/land/i),
        'Ramp': card => isRamp(card),
        'Tutors': card => isTutor(card),
        'Combo': card => false // Manual categorization
    },
    Manabase: {
        'Spires': card => /spire/i.test(card.card_name) && /spire: search your library for a/i.test(card.rules_text),
        'Ominous Lands': card => /land/i.test(card.type) && /ominous/i.test(card.rules_text),
        'Restored Lands': card => /restored/i.test(card.card_name) && /land/i.test(card.type) && /^pathbound/i.test(card.rules_text),
        'Shockpools': card => /land/i.test(card.type) && /add one mana of any color a land you control/i.test(card.rules_text) && /the/i.test(card.card_name),
        'Driftings': card => /drifting/i.test(card.card_name) && card.set === 'FOE',
        'Castles': card => card.set === 'HOD' && /1 damage to you unless you control three or more/i.test(card.rules_text),
        'Gold Lands': card => false, // Manual categorization
        'Utility Lands': card => false // Manual categorization
    },
    Sanctum: {
        'Pathbound': card => /^pathbound/gi.test(card.rules_text),
        'Erysites': card => /^transcend/gi.test(card.rules_text),
        'Wonders': card => /wonder/gi.test(card.type),
        'Fetchers': card => isWish(card)
    }
};

function isInCategory(card, category, subcategory) {
    return (compendium_rules[category]?.[subcategory]?.(card) || manual_include[category]?.[subcategory]?.includes?.(card.card_name)) && !manual_exclude[category]?.[subcategory]?.includes?.(card.card_name);
}

function generateCompendium() {
    const compendium = {};

    for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
        compendium[headingName] = {};
        for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
            compendium[headingName][subheadingName] = [];
        }
    }
    
    for (const card of card_list_arrayified) {
        if (card.shape.includes("token") || card.card_name.includes('ITD')) continue;
        for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
            for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
                if (isInCategory(card, headingName, subheadingName) && meetsPlayrate(card, headingName))
                    compendium[headingName][subheadingName].push(card.card_name);
            }
        }
    }

    for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
        for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
            compendium[headingName][subheadingName] = [...new Set(compendium[headingName][subheadingName])];
            compendium[headingName][subheadingName].sort(playrateFn);
            const size = sizes?.[headingName]?.[subheadingName] || 15;
            compendium[headingName][subheadingName] = compendium[headingName][subheadingName].slice(0, size);
        }
    }

    return compendium;
}

function isDecimal(char) {
	return char >= '0' && char <= '9';
}

function convertToMV(cost) {
    let mv = 0;

    const costTokens = cost.substring(1, cost.length - 1).replaceAll("}{", " ").split(' ');
    for (const token of costTokens) {
        if (isDecimal(token)) {
            mv += parseInt(token);
        }
        // 2brid
        else if (token.includes('2')) {
            mv += 2;
        }
        else if (token != "x" && token != '') {
            mv += 1;
        }
    }

    return mv;
}

function meetsPlayrate(card, category) {
    const pr = playrates[card.card_name] / numDecks;
    const threshold = pr_override?.[category] ?? 0.01;
    return pr > threshold;
}

function playrateFn(a, b) {
    return playrates[b] - playrates[a];
}

const firebaseConfig = {
    apiKey: "AIzaSyCPurnKVn2caCn3L-gKF2tMFwWur73YAuw",
    authDomain: "voyager-78e30.firebaseapp.com",
    projectId: "voyager-78e30",
    storageBucket: "voyager-78e30.firebasestorage.app",
    messagingSenderId: "411191248476",
    appId: "1:411191248476:web:591349be169d823e5f8899",
    measurementId: "G-TQ1L48F25M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

function sigmoid(x) {
    return 1 / (1 + Math.exp(-x));
}

let totalWeight;

async function getCardStats() {
    const stats = {};

    totalWeight = 0;
    const now = new Date();
    const date = now.getDate();
    const month = now.getMonth();
    const year = now.getYear();

    for (const card of card_list_arrayified) {
        stats[card.card_name] = 0;
    }

    for (const deck of all_decks) {
        const decklist = atob(deck.url.split(';')[1].split('&main')[0]);
        // const { deckDate, deckMonth, deckYear } = (deck.last_modified || '2025-04-01').split('-').map(d => parseInt(d));
        // const difference = (date - deckDate) + (month - deckMonth) * 30 + (year - deckYear) * 365;
        // const weight = sigmoid(difference) * 2 + 0.5;
        // totalWeight += weight;

        for (const line of decklist.split("\n")) {
            const card_name = line.substring(line.indexOf(" ") + 1, line.length).split('(')[0].trim();

            if (stats[card_name] == null) continue;

            stats[card_name]++;
        }
    }

    return stats;
}

const all_decks = [];
let q;

q = query(collection(db, "events"));
const all_events_docs = await getDocs(q);

q = query(collection(db, "users"));
const all_users_docs = await getDocs(q);

all_events_docs.forEach((doc) => {
    const data = doc.data();
    for (const user in data.decks) {
        const deck = data.decks[user];
        all_decks.push({ ...deck, "user": user, "event": true });
    }
});

all_users_docs.forEach((doc) => {
    const data = doc.data();
    for (const deck of data.decks) {
        all_decks.push({ ...deck, "user": data.username, "event": false });
    }
});

const { manual_exclude, manual_include, sizes, pr_override } = JSON.parse(fs.readFileSync('input.json'));
let card_list_arrayified, playrates, numDecks;


fs.readFile('../../lists/all-cards.json', 'utf8', async (err, data) => {
    const all_cards = JSON.parse(data);
    card_list_arrayified = all_cards.cards;

    playrates = await getCardStats();
    numDecks = all_decks.length;

    const compendium = generateCompendium();

    fs.writeFileSync('compendium.json', JSON.stringify(compendium, null, 2));
    console.log("Succesfully generated compendium @ ./compendium.json !")
    process.exit(0);
});