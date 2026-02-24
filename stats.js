let card_list;

await fetch('https://voyager-mtg.github.io/lists/all-cards.json')
				.then(response => response.json())
				.then(json => {
					card_list = json;
				}).catch(error => console.error('Error:', error));const averages = {};

const card_list_arrayified = card_list.cards;

function isDecimal(char) {
    return char >= '0' && char <= '9';
}


function convertToMV(cost) {
    let mv = 0;

    let costTokens = cost.substring(1, cost.length - 1).replaceAll("}{", " ").split(' ');
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

for (const card of card_list_arrayified) {
    if (!card.type.includes('Creature')) continue;
    const color = card.color.length > 1 ? 'M' : card.color;
    const pow = parseInt(card.pt.split('/')[0]);
    const tou = parseInt(card.pt.split('/')[1]);
    averages[color] ??= {};
    averages[color][convertToMV(card.cost)] ??= [];
    averages[color][convertToMV(card.cost)].push(pow + tou);
}

for (const color_category of Object.values(averages)) {
    for (const mv in color_category) {
        color_category[mv] = color_category[mv].reduce((acc, i) => acc + i, 0) / color_category[mv].length;
    }
}

console.log(averages);