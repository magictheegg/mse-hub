function compareFunction(a, b) {
    const sortMode = document.getElementById("sort-by").value;

    // if (a.rarity.includes("masterpiece") && !b.rarity.includes("masterpiece")) {
    // 	return 1;
    // }

    // if (!a.rarity.includes("masterpiece") && b.rarity.includes("masterpiece")) {
    // 	return -1;
    // }

    if (a.shape.includes("token") && !b.shape.includes("token")) {
        return 1;
    }

    if (!a.shape.includes("token") && b.shape.includes("token")) {
        return -1;
    }

    if (sortMode == 'set-code') {
        if (a.set === b.set) {
            if (a.number === b.number) {
                return 0;
            }
            else {
                return (a.number < b.number) ? -1 : 1;
            }
        }
        else {
            return (a.set < b.set) ? -1 : 1;
        }
    }
    else if (sortMode == 'name') {
        if (a.card_name === b.card_name) {
            return 0;
        }
        else {
            return (a.card_name < b.card_name) ? -1 : 1;
        }
    }
    else if (sortMode == 'mv') {
        //since cost is now formatted like {1}{U} instead of 1U, we need to remove the brackets from the string first
        //CE: undoing this because we're counting { chars for MV
        a_mv = isDecimal(a.cost.charAt(1)) ? parseInt(a.cost.substring(1, a.cost.indexOf('}'))) + a.cost.replaceAll('x', '').split('{').length - 2 : a.cost.replaceAll('x', '').split('{').length - 1;
        b_mv = isDecimal(b.cost.charAt(1)) ? parseInt(b.cost.substring(1, b.cost.indexOf('}'))) + b.cost.replaceAll('x', '').split('{').length - 2 : b.cost.replaceAll('x', '').split('{').length - 1;
        if (a_mv === b_mv) {
            if (a.card_name === b.card_name) {
                return 0;
            }
            else {
                return (a.card_name < b.card_name) ? -1 : 1;
            }
        }
        else {
            return (a_mv < b_mv) ? -1 : 1;
        }
    }
    else if (sortMode == 'color') {
        color_sort_order = ["W", "U", "B", "R", "G", "I", "WU", "UB", "BR", "RG", "GW", "WB", "UR", "BG", "RW", 'IW', 'IU', 'IB', 'IR', 'IG', "GU", "WUB", "UBR", "BRG", "RGW", "GWU", "RWB", "GUR", "WBG", "URW", "BGU", 'IWU', 'IUB', 'IBR', 'IRG', 'IGW', 'IWB', 'IBG', 'IGU', 'IUR', 'IRW', "WUBR", "UBRG", "BRGW", "RGWU", "GWUB", "IWUB", "IUBR", "IBRG", "IRGW", "IGWU", "IRWB", "IGUR", "IWBG", "IURW", "IBGU", "WUBRG", "IWUBR", "IUBRG", "IBRGW", "IRGWU", "IGWUB", ""];

        a_color_index = -1;
        b_color_index = -1;

        for (let i = 0; i < color_sort_order.length; i++) {
            if (a.color.toLowerCase().split('').sort().join('') == color_sort_order[i].toLowerCase().split('').sort().join('')) {
                a_color_index = i;
            }
            if (b.color.toLowerCase().split('').sort().join('') == color_sort_order[i].toLowerCase().split('').sort().join('')) {
                b_color_index = i;
            }
        }

        if (a_color_index === b_color_index) {
            if (a.card_name === b.card_name) {
                return 0;
            }
            else {
                return (a.card_name < b.card_name) ? -1 : 1;
            }
        }
        else {
            return (a_color_index < b_color_index) ? -1 : 1;
        }
    }
    else if (sortMode == 'rarity') {
        rarity_sort_order = ["mythic", "rare", "uncommon", "common"];
        a_rarity_index = 100;
        b_rarity_index = 100;

        for (let i = 0; i < rarity_sort_order.length; i++) {
            if (a.rarity.toLowerCase() == rarity_sort_order[i]) {
                a_rarity_index = i;
            }
            if (b.rarity.toLowerCase() == rarity_sort_order[i]) {
                b_rarity_index = i;
            }
        }

        if (a_rarity_index === b_rarity_index) {
            color_sort_order = ["W", "U", "B", "R", "G", "I", "WU", "UB", "BR", "RG", "GW", "WB", "UR", "BG", "RW", 'IW', 'IU', 'IB', 'IR', 'IG', "GU", "WUB", "UBR", "BRG", "RGW", "GWU", "RWB", "GUR", "WBG", "URW", "BGU", 'IWU', 'IUB', 'IBR', 'IRG', 'IGW', 'IWB', 'IBG', 'IGU', 'IUR', 'IRW', "WUBR", "UBRG", "BRGW", "RGWU", "GWUB", "IWUB", "IUBR", "IBRG", "IRGW", "IGWU", "IRWB", "IGUR", "IWBG", "IURW", "IBGU", "WUBRG", "IWUBR", "IUBRG", "IBRGW", "IRGWU", "IGWUB", ""];

            a_color_index = -1;
            b_color_index = -1;

            for (let i = 0; i < color_sort_order.length; i++) {
                if (a.color.toLowerCase().split('').sort().join('') == color_sort_order[i].toLowerCase().split('').sort().join('')) {
                    a_color_index = i;
                }
                if (b.color.toLowerCase().split('').sort().join('') == color_sort_order[i].toLowerCase().split('').sort().join('')) {
                    b_color_index = i;
                }
            }

            if (a_color_index === b_color_index) {
                if (a.card_name === b.card_name) {
                    return 0;
                }
                else {
                    return (a.card_name < b.card_name) ? -1 : 1;
                }
            }
            else {
                return (a_color_index < b_color_index) ? -1 : 1;
            }
        }
        else {
            return (a_rarity_index < b_rarity_index) ? -1 : 1;
        }
    }

    else if (sortMode == "copies") {
        if (on_cl_page) {
            const a_copies = collection_copies.get(`${a.card_name} (${a.set}) ${a.number}`);
            const b_copies = collection_copies.get(`${b.card_name} (${b.set}) ${b.number}`);
            return b_copies - a_copies;
        } else {
            const a_copies = collection_copies[`${a.set}-${a.number}`];
            const b_copies = collection_copies[`${b.set}-${b.number}`];
            return b_copies - a_copies;
        }
    }

    else if (sortMode == 'playrate') {
        return all_cards_stats[b.card_name].playrate_overall - all_cards_stats[a.card_name].playrate_overall;
    }
}

async function searchToken(card, token) {
    let card_stats = [];

    for (var key in card) {
        if (isNaN(card[key])) {
            card_stats[key] = card[key].toLowerCase();
        }
        else {
            card_stats[key] = card[key];
        }
    }

    let card_name = card_stats.card_name;
    let card_color = card_stats.color;
    let card_rarity = card_stats.rarity;
    let card_type = card_stats.type;
    // 4: collector number
    let card_ci = removeDuplicateChars(card_stats.color_identity);
    let card_cost = card_stats.cost;
    let card_mv = convertToMV(card_cost);
    //Strip out the lingering [i][/i] and [b][/b] tags while we're searching just in case someone decided to bold something in the
    //middle of their rules text for some reason
    let card_oracle_text = card_stats.rules_text != "" ? card_stats.rules_text.replace(/\[(\/)?([ib])\]/g, "") : card_stats.special_text.replace(/\[(\/)?([ib])\]/g, "");
    let card_power = card_stats.pt.substring(0, card_stats.pt.indexOf('/'));
    let card_toughness = card_stats.pt.substring(card_stats.pt.indexOf('/') + 1);
    let card_shape = card_stats.shape;
    let card_set = card_stats.set;
    let card_loyalty = card_stats.loyalty;
    let card_notes = card_stats.notes;
    let card_artist = card_stats.artist;
    let card_color_2 = "";
    let card_cost_2 = "";
    let card_power_2 = "";
    let card_toughness_2 = "";
    let card_loyalty_2 = ""

    let color_map = new Map([
        ["white", "w"],
        ["blue", "u"],
        ["black", "b"],
        ["red", "r"],
        ["green", "g"],
        ["silver", "i"],
        ["azorius", "wu"],
        ["dimir", "ub"],
        ["rakdos", "br"],
        ["gruul", "rg"],
        ["selesnya", "gw"],
        ["orzhov", "wb"],
        ["golgari", "bg"],
        ["simic", "gu"],
        ["izzet", "ur"],
        ["boros", "rw"],
        ["esper", "wub"],
        ["grixis", "ubr"],
        ["jund", "brg"],
        ["naya", "rgw"],
        ["bant", "gwu"],
        ["abzan", "wbg"],
        ["sultai", "bgu"],
        ["temur", "gur"],
        ["jeskai", "urw"],
        ["mardu", "rwb"],
    ]);

    // two cards in one
    if (card_shape.includes("adventure") || card_shape.includes("double") || card_shape.includes("spli")) {
        card_name = card_name + "	" + card_stats.card_name2;
        card_type = card_type + "	" + card_stats.type2;
        card_oracle_text = card_oracle_text + "	" + (card_stats.rules_text2 != "" ? card_stats.rules_text2.replace(/\[(\/)?([ib])\]/g, "") : card_stats.special_text2.replace(/\[(\/)?([ib])\]/g, ""));
        card_color_2 = card_stats.color2;
        card_cost_2 = card_stats.cost2;
        card_power_2 = card_stats.pt2.substring(0, card_stats.pt2.indexOf('/'));
        card_toughness_2 = card_stats.pt.substring(card_stats.pt.indexOf('/') + 1);
        card_loyalty_2 = card_stats.loyalty2;
    }

    token = token.replaceAll("~", card_name).replaceAll("cardname", card_name).replaceAll('"', '').replaceAll('“', '').replaceAll('”', '');

    const modifierRegex = /[!:<>=]+/g;
    const match = token.match(modifierRegex);

    if (match) {
        const modifier = match[0];
        const term = token.substring(0, token.indexOf(modifier));
        let check = token.substring(token.indexOf(modifier) + modifier.length);

        if (check.charAt(0) == '/') {
            check = check.substring(1);
        }
        if (check.charAt(check.length - 1) == '/') {
            check = check.substring(0, check.length - 1);
        }

        if (color_map.has(check)) {
            check = color_map.get(check);
        }

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
        if (term == "mv" || term == "cmc") {
            if (modifier == "!" || modifier == "=") {
                return (card_mv == check);
            }
            else if (modifier == ":") {
                return (card_mv == check);
            }
            else if (modifier == "<") {
                return (card_mv < check);
            }
            else if (modifier == ">") {
                return (card_mv > check);
            }
            else if (modifier == "<=") {
                return (card_mv <= check);
            }
            else if (modifier == ">=") {
                return (card_mv >= check);
            }
        }
        if (term == "c" || term == "color" || term == "colour") {
            if (!isNaN(check)) {
                if (modifier == "!" || modifier == "=") {
                    return card_color.length == parseInt(check);
                }
                else if (modifier == ":") {
                    return card_color.length == parseInt(check);
                }
                else if (modifier == "<") {
                    return card_color.length < parseInt(check);
                }
                else if (modifier == ">") {
                    return card_color.length > parseInt(check);
                }
                else if (modifier == "<=") {
                    return card_color.length <= parseInt(check);
                }
                else if (modifier == ">=") {
                    return card_color.length >= parseInt(check);
                }
            }
            else {
                card_color = card_color == "" ? "c" : card_color;
                if (check == "m") {
                    if (modifier == "<") {
                        return card_color.length < 2;
                    }
                    else {
                        return card_color.length > 1;
                    }
                }
                else if (modifier == "!" || modifier == "=") {
                    return (card_color.split("").sort().join("") == check.split("").sort().join(""));
                }
                else if (modifier == ":") {
                    return hasAllChars(card_color, check);
                }
                else if (modifier == "<") {
                    return card_color == "c" || (check.length > card_color.length && hasAllChars(check, card_color));
                }
                else if (modifier == ">") {
                    return card_color.length > check.length && hasAllChars(card_color, check);
                }
                else if (modifier == "<=") {
                    return card_color == "c" || hasAllChars(check, card_color);
                }
                else if (modifier == ">=") {
                    return hasAllChars(card_color, check);
                }
            }
        }
        if (term == "cost" || term == "mana") {
            if (modifier == "!" || modifier == "=" || modifier == ":") {
                card_cost_cleaned = card_cost.replaceAll('{', '').replaceAll('}', '');
                return check == card_cost || check == card_cost_cleaned;
            }
        }
        if (term == "ci" || term == "id") {
            if (!isNaN(check)) {
                card_ci = card_ci == "c" ? "" : card_ci;
                if (modifier == "!" || modifier == "=") {
                    return card_ci.length == parseInt(check);
                }
                else if (modifier == ":") {
                    return card_ci.length <= parseInt(check);
                }
                else if (modifier == "<") {
                    return card_ci.length < parseInt(check);
                }
                else if (modifier == ">") {
                    return card_ci.length > parseInt(check);
                }
                else if (modifier == "<=") {
                    return card_ci.length <= parseInt(check);
                }
                else if (modifier == ">=") {
                    return card_ci.length >= parseInt(check);
                }
            }
            else {
                if (modifier == "!" || modifier == "=") {
                    return (card_ci.split("").sort().join("") == check.split("").sort().join(""));
                }
                else if (modifier == ":") {
                    return card_ci == "c" || hasAllChars(check, card_ci);
                }
                else if (modifier == "<") {
                    return card_ci == "c" || (check.length > card_ci.length && hasAllChars(check, card_ci));
                }
                else if (modifier == ">") {
                    return card_ci.length > check.length && hasAllChars(card_ci, check);
                }
                else if (modifier == "<=") {
                    return card_ci == "c" || hasAllChars(check, card_ci);
                }
                else if (modifier == ">=") {
                    return hasAllChars(card_ci, check);
                }
            }
        }
        if (term == "t" || term == "type") {
            if (modifier == ":") {
                let regex = new RegExp("\\b" + check + "\\b");
                return regex.test(card_type);
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
        if (term == "o" || term == "oracle" || term == "text") {
            if (modifier == ":") {
                let regex = new RegExp(check.replaceAll("+", "\\+"));
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
        if (term == "pow" || term == "power") {
            if (modifier == "!" || modifier == "=") {
                return (card_power == check);
            }
            else if (modifier == ":") {
                return (card_power == check);
            }
            else if (modifier == "<") {
                return (card_power < check);
            }
            else if (modifier == ">") {
                return (card_power > check);
            }
            else if (modifier == "<=") {
                return (card_power <= check);
            }
            else if (modifier == ">=") {
                return (card_power >= check);
            }
        }
        if (term == "tou" || term == "toughness") {
            if (modifier == "!" || modifier == "=") {
                return (card_toughness == check);
            }
            else if (modifier == ":") {
                return (card_toughness == check);
            }
            else if (modifier == "<") {
                return (card_toughness < check);
            }
            else if (modifier == ">") {
                return (card_toughness > check);
            }
            else if (modifier == "<=") {
                return (card_toughness <= check);
            }
            else if (modifier == ">=") {
                return (card_toughness >= check);
            }
        }
        if (term == "r" || term == "rarity") {
            rarities = ["common", "uncommon", "rare", "mythic"];
            for (const rarity of rarities) {
                if (rarity.startsWith(check)) {
                    check = rarity;
                }
            }
            if (modifier == ":" || modifier == "!" || modifier == "=") {
                return (card_rarity == check);
            }
            else if (modifier == "<") {
                return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) < rarities.indexOf(check);
            }
            else if (modifier == ">") {
                return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) > rarities.indexOf(check);
            }
            else if (modifier == "<=") {
                return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) <= rarities.indexOf(check);
            }
            else if (modifier == ">=") {
                return rarities.includes(card_rarity) && rarities.indexOf(card_rarity) >= rarities.indexOf(check);
            }
        }
        if (term == "e" || term == "set") {
            let set_longname = "";
            for (const set of set_list.sets) {
                if (set.set_code.toLowerCase() == card_set) {
                    set_longname = set.set_name.toLowerCase();
                    set_designer = set.designer.toLowerCase();
                    break;
                }
            }
            if (modifier == ":" || modifier == "!" || modifier == "=") {
                return (card_set == check || set_longname.includes(check) || set_designer.includes(check));
            }
            /* unsupported flows
            else if (modifier == "<")
            {

            }
            else if (modifier == ">")
            {

            } */
        }
        if (term == "keyword" || term == "kw" || term == "has") {
            if (modifier == ":" || modifier == "!" || modifier == "=") {
                regex_kw1 = new RegExp(`(^|\n|, )${check}[^.]*($|\n|\\()`, "g");
                regex_kw2 = new RegExp(`(^|\n)${check} `, "g");
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
        if (term == "alias") {
            let regex = new RegExp(check.replaceAll("+", "\\+"));
            return regex.test(card_stats.special_text);
        }
        if (term == "f" || term == "format") {
            if (modifier == ":" || modifier == "!" || modifier == "=") {
                for (const set of sets_json.sets) {
                    if (set.set_code.toLowerCase() == card_set) {
                        formats = ["standard", "modern", "legacy"];
                        set_formats = set.formats.toLowerCase().replace(' ', '').split(',');

                        for (const format of set_formats) {
                            if (formats.includes(format) && formats.includes(check)) {
                                if (formats.indexOf(format) < formats.indexOf(check)) {
                                    return true;
                                }
                            }
                        }

                        return set_formats.includes(check);
                    }
                }
            }
            return false;
        }
        if (term == "is") {
            if (modifier == ":" || modifier == "!" || modifier == "=") {
                // all of these are implemented individually
                if (check == "permanent") {
                    return !card_type.includes("instant") && !card_type.includes("sorcery");
                }
                if (check == "spell") {
                    return !card_type.includes("land");
                }
                if (check == "commander") {
                    return (card_type.includes("legendary") && card_type.includes("creature")) || card_oracle_text.includes("can be your commander");
                }
                if (check == "hybrid") {
                    for (let i = 0; i < card_cost.length - 2; i++) {
                        if (card_cost[i] != '{' && card_cost[i] != '}' && card_cost[i + 1] != '{' && card_cost[i + 1] != '}' && !isDecimal(card_cost[i + 1])) {
                            return true;
                        }
                    }
                    return false;
                }
                if (check == "sanctum") {
                    let regex = new RegExp("((P|p)athbound|(H|h)eir–)");
                    if (regex.test(card_oracle_text)) {
                        return true;
                    } else {
                        if (card_type.includes("wonder") || card_type.includes("erysite") || card_type.includes("realm") || card_type.includes("frontier")) {
                            return true;
                        } else {
                            if (card.special_text.includes("sanctum")) {
                                return true;
                            } else {
                                return false;
                            }
                        }
                    }
                }
                if (check == "dfc") {
                    return card_shape.includes("double");
                }
                if (check == "mdfc") {
                    return card_shape.includes("modal") && card_shape.includes("double");
                } if (check == "tdfc") {
                    return (card_shape.includes("transform") || card.rules_text.includes("transform")) && card_shape.includes("double");
                }
                if (check == "played") {
                    return all_cards_stats[card.card_name].is_played;
                }
                if (check == "staple") {
                    return all_cards_stats[card.card_name].is_staple;
                }
                if (check == 'nerfed' || check == 'changed') {
                    const card_match = new RegExp(`\\*\\*${RegExp.escape(card_name)}(\\'s)?\\*\\* (.*?)\\n`, "gi");
                    return changelogs.match(card_match);
                }
                for (const [ regex, fn ] of Object.entries(is_rules)) {
                    if (!check.match(regex)) continue;
                    return fn(card);
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
        if (term == "tag") {
            if (modifier == ":" || modifier == "=" || modifier == "!") {
                if (check == "removal") {
                    return isRemoval(card_stats);
                }
                if (check == "ca" || check == "cardadvantage" || check == "draw") {
                    return isCA(card_stats);
                }
                if (check == "wipe" || check == "wrath" || check == "boardwipe") {
                    return isWipe(card_stats);
                }
                if (check == "wish" || check == "fetch") {
                    return isWish(card_stats);
                }
                let regex = new RegExp("!tag " + check + "\\b");
                return regex.test(card_notes);
            }
        }
        if (term == "a" || term == "art" || term == "artist") {
            if (modifier == ":" || modifier == "=" || modifier == "!") {
                return card_artist.includes(check);
            }
        }
        if (term == "ft" || term == "flavor" || term == "flavour" || term == "flavortext" || term == "flavourtext") {
            if (modifier == "!" || modifier == "=") {
                return card_stats.flavor_text == check;
            }
            else if (modifier == ":") {
                return card_stats.flavor_text.includes(check);
            }
            else if (modifier == "<") {
                return card_stats.flavor_text < check;
            }
            else if (modifier == ">") {
                return card_stats.flavor_text > check;
            }
        }
        if (term == "lore") {
            if (modifier == "!" || modifier == "=" || modifier == ":") {
                return card_stats.flavor_text.toLowerCase().includes(check) || card_name.includes(check) || card.notes.toLowerCase().includes(check);
            }
        }
        if (term == "designer" || term == "design") {
            if (modifier == "!" || modifier == "=" || modifier == ":") {
                return card_stats.designer.includes(check);
            }
        }
        if (term == "sort" || term == "include") {
            return true;
        }
        if (term == "size" || term == "pt") {
            let searched_power = parseInt(check.split("/")[0]);
            let searched_toughness = parseInt(check.split("/")[1]);
            function search_tou(check, modifier, card_toughness) {
                if (modifier == "!" || modifier == "=") {
                    return (card_toughness == check);
                }
                else if (modifier == ":") {
                    return (card_toughness == check);
                }
                else if (modifier == "<") {
                    return (card_toughness < check);
                }
                else if (modifier == ">") {
                    return (card_toughness > check);
                }
                else if (modifier == "<=") {
                    return (card_toughness <= check);
                }
                else if (modifier == ">=") {
                    return (card_toughness >= check);
                }
            }

            function search_pow(check, modifier, card_power) {
                if (modifier == "!" || modifier == "=") {
                    return (card_power == check);
                }
                else if (modifier == ":") {
                    return (card_power == check);
                }
                else if (modifier == "<") {
                    return (card_power < check);
                }
                else if (modifier == ">") {
                    return (card_power > check);
                }
                else if (modifier == "<=") {
                    return (card_power <= check);
                }
                else if (modifier == ">=") {
                    return (card_power >= check);
                }
            }
            return search_pow(searched_power, modifier, card_power) && search_tou(searched_toughness, modifier, card_toughness);
        }
        if (modifier == ":" || modifier == "=" || modifier == "!") {
            let regex = new RegExp(`!tag<${term}> ${check}\\b`);
            return regex.test(card_notes);
        }
    }
    let regex = new RegExp(token.replaceAll("+", "\\+"));
    return (regex.test(card_stats.special_text) && (localStorage.getItem('settings.searchalias') == "On")) || card_name.includes(token);
} function isDecimal(char) {
    return char >= '0' && char <= '9';
}

const is_rules = {
    // regex: fn
    'wish': isWish,
    'wipe|boardwipe': isWipe,
    'ca|draw': isCA,
    'removal': isRemoval,
    'recurrable|recursion': isRecurrable,
    'discard': isDiscard,
    'tutor|searche?r?': isTutor,
    'ramp': isRamp,
    'utilityl?a?n?d?': isUtilityLand,
    'smallremove?a?l?': card => convertToMV(card.cost) < 4 && isRemoval(card) && card.rules_text.match(/(\/-[1-4X])|(deals [1-4])|(mana value [1-3])|((power|toughness) [1-3])/gi),
    'uncond(itional)?remove?a?l?': card => isRemoval(card) && card.rules_text.match(/exile target|destroy/gi) && !isInCategory(card, 'Interaction', 'Small Removal') && !card.rules_text.match(/target (artifact|enchantment)/gi),
    'counter(spell|magic)?': isCounterspell,
    'threat': isThreat
};

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

function isUtilityLand(card) {
    const regex = /({.}+?): [^a][^d][^d].*/gi;

    return regex.test(card.rules_text) && card.type.includes("land") && !card.card_name.includes("drifting");
}

function hasAllChars(strOut, strIn) {
    let retVal = true;

    for (let i = 0; i < strIn.length; i++) {
        if (!strOut.includes(strIn.charAt(i))) {
            retVal = false;
        }
    }

    return retVal;
}

function hasNoChars(strOut, strIn) {
    let retVal = true;

    for (let i = 0; i < strIn.length; i++) {
        if (strOut.includes(strIn.charAt(i))) {
            retVal = false;
        }
    }

    return retVal;
}

function hasAllAndMoreChars(strOut, strIn) {
    let retVal = true;

    for (let i = 0; i < strIn.length; i++) {
        if (!strOut.includes(strIn.charAt(i))) {
            retVal = false;
        }
    }

    return retVal && (strOut.length > strIn.length);
}

function tokenizeTerms(searchTerms) {
    let tokenRegex = /-?\w*[!:<>=]?(([^ "\(\)“”]+)|(\".+?\")|(\(.+?\))|(\/.+?\/)|(\“.+?\”))/g;
    let searchTokens = searchTerms.match(tokenRegex);

    return searchTokens;
}

async function searchAllTokens(card, tokens) {
    if (tokens == null || tokens == '') {
        return true;
    }

    tokens = tokens.filter(t => !t.startsWith("sort:") && !t.startsWith("direction:"));
    if (tokens.length == 0)
    {
        return true;
    }

    for (let i = 0; i < tokens.length; i++) {
        if (tokens[i].charAt(0) == '+') {
            return await searchAllTokens(card, tokens.slice(0, i)) && await searchAllTokens(card, tokens.slice(i + 1));
        }
        if (tokens[i] == "or") {
            return await searchAllTokens(card, tokens.slice(0, i)) || await searchAllTokens(card, tokens.slice(i + 1));
        }
    }

    for (let token of tokens) {
        if (token.charAt(0) == '-') {
            return !(await searchToken(card, token.substring(1))) && (tokens.length == 1 ? true : await searchAllTokens(card, tokens.slice(1)));
        }
        if (token.charAt(0) == '(') {
            return await searchAllTokens(card, tokenizeTerms(token.substring(1, token.length - 1))) && (tokens.length == 1 ? true : await searchAllTokens(card, tokens.slice(1)));
        }
        else {
            return await searchToken(card, token) && (tokens.length == 1 ? true : await searchAllTokens(card, tokens.slice(1)));
        }
    }
}

function removeDuplicateChars(str) {
    let ret_str = '';

    for (const c of str) {
        if (!ret_str.includes(c)) {
            ret_str += c;
        }
    }

    return ret_str;
}

function convertToMV(cost) {
    let mv = 0;

    costTokens = cost.substring(1, cost.length - 1).replaceAll("}{", " ").split(' ');
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