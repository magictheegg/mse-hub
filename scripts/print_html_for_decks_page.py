import os
import json

def generateHTML():
    output_html_file = "decks.html"

    with open(os.path.join('resources', 'site-config.json'), encoding='utf-8-sig') as f:
        config = json.load(f)
        base_url = config.get('base_url', '')
        hub_name = base_url.split('https://')[1].split('.github.io')[0].lower() if 'https://' in base_url else 'unknown'

    # Start creating the HTML file content
    html_content = f'''<html>
<head>
    <title>Browse Decks</title>
    <link rel="icon" type="image/x-icon" href="./img/deck.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..800;1,300..800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="./resources/mana.css">
    <link rel="stylesheet" href="./resources/header.css">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
</head>
<script title="root">
    const rootPath = ".";
    const SUPABASE_URL = 'https://mtjkkvtcmejzcpjmropd.supabase.co';
    const SUPABASE_KEY = 'sb_publishable_Hgyr2JJRsJRa1pYwoz-ijQ_ozfwnp9t';
    const _supabase = supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
    const hubName = "{hub_name}";
</script>
<style>
    @font-face {{
        font-family: 'Beleren Small Caps';
        src: url('./resources/beleren-caps.ttf');
    }}
    @font-face {{
        font-family: Beleren;
        src: url('./resources/beleren.ttf');
    }}
    @font-face {{
        font-family: 'Gotham Narrow Medium';
        src: url('./resources/gotham-narrow-medium.otf');
    }}
    @font-face {{
        font-family: 'Gotham Narrow Bold';
        src: url('./resources/gotham-narrow-bold.otf');
    }}
    body {{
        font-family: 'Open Sans', 'Helvetica', 'Arial', sans-serif;
        overscroll-behavior: none;
        margin: 0px;
        background-color: #f3f3f3;
    }}
    .decks-page-container {{
        width: 75%;
        max-width: 1200px;
        margin: 40px auto;
    }}
    .filter-container {{
        display: flex;
        gap: 10px;
        margin: 0 auto 30px auto;
        align-items: center;
        width: 90%;
    }}
    .filter-container input, .filter-container select {{
        padding: 8px 12px;
        border: 1px solid #d5d9d9;
        border-radius: 4px;
        font-size: 16px;
    }}
    .filter-container > input, .filter-container > .card-search-container {{
        flex: 2;
        min-width: 0;
    }}
    .filter-container > select {{
        flex: 1;
        min-width: 0;
    }}
    .card-search-container {{
        position: relative;
        display: flex;
    }}
    .card-search-container input {{
        width: 100%;
    }}
    .autocomplete-dropdown {{
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        border: 1px solid #d5d9d9;
        border-top: none;
        border-radius: 0 0 4px 4px;
        max-height: 200px;
        overflow-y: auto;
        overscroll-behavior: contain;
        z-index: 100;
        display: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .autocomplete-item {{
        padding: 8px 12px;
        cursor: pointer;
        font-size: 14px;
        border-bottom: 1px solid #f0f0f0;
    }}
    .autocomplete-item:hover {{
        background-color: #f3f3f3;
    }}
    .chip-container {{
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: -20px auto 20px auto;
        width: 90%;
    }}
    .chip {{
        display: flex;
        align-items: center;
        gap: 8px;
        background: #00bfff;
        color: white;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 14px;
        font-family: 'Gotham Narrow Medium', sans-serif;
    }}
    .chip span {{
        cursor: pointer;
        font-weight: bold;
        opacity: 0.8;
    }}
    .chip span:hover {{
        opacity: 1;
    }}
    .decks-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fill, 320px);
        gap: 25px;
        justify-content: center;
    }}
    .deck-card {{
        background-color: white;
        border: 1px solid #d5d9d9;
        border-radius: 8px;
        overflow: hidden;
        text-decoration: none;
        color: inherit;
        transition: transform 0.2s, box-shadow 0.2s;
        height: 220px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }}
    .deck-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
    }}
    .deck-card-bg {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-size: 120%;
        background-position: center 20%;
        z-index: 1;
    }}
    .deck-card-overlay {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(to bottom, rgba(0,0,0,0) 20%, rgba(0,0,0,0.85) 100%);
        z-index: 2;
    }}
    .deck-card-info {{
        position: relative;
        z-index: 3;
        padding: 15px;
        color: white;
    }}
    .deck-card-info h1 {{
        font-family: 'Gotham Narrow Bold', sans-serif;
        font-size: 22px;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.9);
        line-height: 1.1;
    }}
    .deck-card-info h2 {{
        font-family: 'Gotham Narrow Medium', sans-serif;
        font-size: 14px;
        margin: 4px 0 0 0;
        opacity: 0.9;
        font-style: italic;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
        font-weight: normal;
    }}
    .pagination {{
        margin-top: 40px;
        display: flex;
        justify-content: center;
        gap: 10px;
    }}
    .pagination button {{
        padding: 8px 16px;
        border: 1px solid #d5d9d9;
        background: white;
        border-radius: 4px;
        cursor: pointer;
    }}
    .pagination button:disabled {{
        opacity: 0.5;
        cursor: not-allowed;
    }}
    .pagination button.active {{
        background: #171717;
        color: white;
        border-color: #171717;
    }}
    .no-results {{
        display: none;
        text-align: center;
        padding-top: 60px;
        padding-bottom: 60px;
        width: 100%;
    }}
    .no-results img {{
        width: 150px;
        margin-bottom: 20px;
        opacity: 0.3;
        filter: drop-shadow(0 0 4px #000);
    }}
    .no-results h1 {{
        font-family: Beleren;
        color: #494949;
        margin: 0;
        font-size: 40px;
    }}
    .no-results p {{
        color: #797979;
        font-size: 18px;
        margin-top: 10px;
    }}
</style>
<body>
'''

    with open(os.path.join('scripts', 'snippets', 'header.txt'), encoding='utf-8-sig') as f:
        html_content += f.read()

    html_content += '''
    <div class="decks-page-container">
        <div class="filter-container">
            <input type="text" id="name-filter" placeholder="Filter by deck name..." oninput="handleFilterChange()">
            <div class="card-search-container">
                <input type="text" id="card-search" placeholder="Filter by card name..." oninput="handleCardSearch(event)" autocomplete="off">
                <div id="autocomplete-dropdown" class="autocomplete-dropdown"></div>
            </div>
            <select id="format-filter" onchange="handleFilterChange()">
                <option value="">All Formats</option>
            </select>
        </div>
        <div id="chip-container" class="chip-container"></div>
        <div id="no-results" class="no-results">
            <img src="./img/deck.png">
            <h1 id="no-results-title">No decks found</h1>
            <p id="no-results-text">Your search didn't match any decks. Try adjusting your search terms.</p>
        </div>
        <div class="decks-grid" id="decks-grid">
            <!-- Decks will be loaded here -->
        </div>
        <div class="pagination" id="pagination">
            <!-- Pagination will be loaded here -->
        </div>
    </div>

    <script>
        let allDecks = [];
        let filteredDecks = [];
        let currentPage = 1;
        const itemsPerPage = 12;
        let cardLookup = {};
        let allCardsArray = [];
        let setConfigs = {};
        let selectedCards = [];
        let specialchars = "";

        async function init() {
            // Show loading state
            document.getElementById('no-results').style.display = 'block';
            document.getElementById('no-results-title').innerText = 'Loading Decks...';
            document.getElementById('no-results-text').innerText = 'Please wait while we fetch the latest decks from the Hub.';

            // Load set configs to know naming conventions
            const setsResponse = await fetch('./lists/all-sets.json');
            const setsData = await setsResponse.json();
            sets_json = setsData; // Ensure sets_json is populated for the loops below
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
                                        s.hubURL = url;
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
            for (const set of sets_json.sets) {
                try {
                    const prefix = set.hubURL ? set.hubURL : ".";
                    const setConfResp = await fetch(`${prefix}/sets/${set.set_code}-files/${set.set_code}.json`);
                    setConfigs[set.set_code] = await setConfResp.json();
                    if (set.hubURL) {
                        setConfigs[set.set_code].hubURL = set.hubURL;
                    }
                } catch (e) {
                    console.error("Could not load config for set:", set.set_code);
                }
            }

            // Load formats dynamically
            await fetch(rootPath + '/lists/formats.json')
                .then(response => response.json())
                .then(data => {
                    const select = document.getElementById("format-filter");
                    // Keep the first option (All Formats)
                    const firstOption = select.options[0];
                    select.innerHTML = '';
                    select.appendChild(firstOption);
                    
                    data.formats.forEach(f => {
                        const option = document.createElement("option");
                        option.value = f;
                        option.innerText = f;
                        select.appendChild(option);
                    });
                }).catch(error => console.error('Error loading formats:', error));

            // Initialize card data structures
            allCardsArray = card_list_arrayified;
            card_list_arrayified.forEach(card => {
                const key = `${card.set}-${card.number}`;
                const isToken = card.shape && card.shape.includes('token');
                if (!cardLookup[key] || (!isToken && cardLookup[key].shape && cardLookup[key].shape.includes('token'))) {
                    cardLookup[key] = card;
                }
            });

            await fetchDecks();
        }

        function getCardStats(item) {
            const name = item.name || item.card_name;
            const num = item.num || item.number;
            const set = item.set;

            const findFunc = (c) => {
                const notToken = !c.shape || !c.shape.includes("token");
                const matchSet = c.set === set;
                if (name && num) {
                    return matchSet && c.card_name === name && c.number == num && notToken;
                } else if (name) {
                    return matchSet && c.card_name === name && notToken;
                } else {
                    return matchSet && c.number == num && notToken;
                }
            };

            let stats = allCardsArray.find(findFunc);
            if (!stats && name && num) {
                stats = allCardsArray.find(c => c.set === set && c.card_name === name && (!c.shape || !c.shape.includes("token")));
                if (!stats) {
                    stats = cardLookup[`${set}-${num}`];
                }
            } else if (!stats) {
                stats = cardLookup[`${set}-${num}`];
            }
            return stats;
        }

        document.addEventListener("DOMContentLoaded", async function () {
'''

    with open(os.path.join('scripts', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
        html_content += f.read()

    html_content += '''
            init();
        });

        function goToSearch() {
            window.location.href = rootPath + "/search?search=" + encodeURIComponent(document.getElementById("search").value);
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
        async function fetchDecks() {
            const { data, error } = await _supabase
                .from('decks')
                .select('*')
                .eq('hub', hubName)
                .order('created_at', { ascending: false });

            if (error) {
                console.error('Error fetching decks:', error);
                document.getElementById('no-results-title').innerText = 'Error Loading Decks';
                document.getElementById('no-results-text').innerText = 'There was a problem connecting to the database. Please try again later.';
                return;
            }

            allDecks = data;
            filteredDecks = allDecks;
            renderDecks();
        }

        function handleCardSearch(e) {
            const query = e.target.value.toLowerCase();
            const dropdown = document.getElementById('autocomplete-dropdown');
            dropdown.innerHTML = '';

            if (query.length < 3) {
                dropdown.style.display = 'none';
                return;
            }

            // Filter unique cards by name
            const matches = [];
            const seenNames = new Set();

            for (const card of allCardsArray) {
                if (card.card_name.toLowerCase().includes(query) && !seenNames.has(card.card_name)) {
                    matches.push(card);
                    seenNames.add(card.card_name);
                    if (matches.length >= 10) break;
                }
            }

            if (matches.length > 0) {
                matches.forEach(card => {
                    const div = document.createElement('div');
                    div.className = 'autocomplete-item';
                    div.innerText = card.card_name;
                    div.onclick = () => selectCard(card);
                    dropdown.appendChild(div);
                });
                dropdown.style.display = 'block';
            } else {
                dropdown.style.display = 'none';
            }
        }

        function getCardImgSrc(card) {
            if (!card) return './img/card_back.png';
            const setConf = setConfigs[card.set];
            const isPosition = setConf && setConf.image_name === 'position';
            const imgType = card.image_type || 'jpg';
            const isDFC = card.shape && card.shape.includes('double');
            const suffix = isDFC ? '_front' : '';
            
            let namePart = "";
            if (isPosition) {
                namePart = card.position + suffix;
            } else {
                const connector = card.shape && card.shape.includes('token') ? 't_' : '_';
                namePart = `${card.number}${connector}${card.card_name}${suffix}`;
            }
            
            return `./sets/${card.set}-files/img/${namePart}.${imgType}`;
        }

        function selectCard(card) {
            if (selectedCards.some(c => c.card_name === card.card_name)) {{
                document.getElementById('card-search').value = '';
                document.getElementById('autocomplete-dropdown').style.display = 'none';
                return;
            }}

            selectedCards.push(card);
            document.getElementById('card-search').value = '';
            document.getElementById('autocomplete-dropdown').style.display = 'none';
            renderChips();
            handleFilterChange();
        }

        function renderChips() {
            const container = document.getElementById('chip-container');
            container.innerHTML = '';
            selectedCards.forEach((card, index) => {
                const chip = document.createElement('div');
                chip.className = 'chip';
                chip.innerHTML = `
                    ${card.card_name}
                    <span onclick="removeCardFilter(${index})">×</span>
                `;
                container.appendChild(chip);
            });
        }

        function removeCardFilter(index) {
            selectedCards.splice(index, 1);
            renderChips();
            handleFilterChange();
        }

        function handleFilterChange() {
            const nameFilter = document.getElementById('name-filter').value.toLowerCase();
            const formatFilter = document.getElementById('format-filter').value;

            filteredDecks = allDecks.filter(deck => {
                const matchesName = deck.name.toLowerCase().includes(nameFilter);
                const matchesFormat = !formatFilter || deck.format === formatFilter;
                
                let matchesAllCards = true;
                if (selectedCards.length > 0) {
                    const deckCards = (deck.mainboard || []).concat(deck.sideboard || []);
                    const deckCardNames = new Set();
                    deckCards.forEach(item => {
                        const c = getCardStats(item);
                        if (c) deckCardNames.add(c.card_name);
                    });

                    matchesAllCards = selectedCards.every(sc => deckCardNames.has(sc.card_name));
                }

                return matchesName && matchesFormat && matchesAllCards;
            });

            currentPage = 1;
            renderDecks();
        }

        function renderDecks() {
            const grid = document.getElementById('decks-grid');
            const noResults = document.getElementById('no-results');
            grid.innerHTML = '';

            if (filteredDecks.length === 0) {
                noResults.style.display = 'block';
                document.getElementById('no-results-title').innerText = 'No decks found';
                document.getElementById('no-results-text').innerText = "Your search didn't match any decks. Try adjusting your search terms.";
                document.getElementById('pagination').innerHTML = '';
                return;
            } else {
                noResults.style.display = 'none';
            }

            const start = (currentPage - 1) * itemsPerPage;
            const end = start + itemsPerPage;
            const pageItems = filteredDecks.slice(start, end);

            pageItems.forEach(deck => {
                const card = getMostExpensiveCard(deck);
                let imageUrl = './img/card_back.png';

                if (card) {
                    const setConf = setConfigs[card.set];
                    const isPosition = setConf && setConf.image_name === 'position';
                    const imgType = card.image_type || 'jpg';
                    const isDFC = card.shape && card.shape.includes('double');
                    const suffix = isDFC ? '_front' : '';
                    
                    let namePart = "";
                    if (isPosition) {
                        namePart = card.position + suffix;
                    } else {
                        const connector = card.shape && card.shape.includes('token') ? 't_' : '_';
                        namePart = `${card.number}${connector}${card.card_name}${suffix}`;
                    }
                    
                    const prefix = (setConf && setConf.hubURL) ? setConf.hubURL : ".";
                    imageUrl = `${prefix}/sets/${card.set}-files/img/${namePart}.${imgType}`;
                }
                
                const cardEl = document.createElement('a');
                cardEl.href = `./deck?id=${deck.id}`;
                cardEl.className = 'deck-card';
                cardEl.innerHTML = `
                    <div class="deck-card-bg" style="background-image: url('${imageUrl}')"></div>
                    <div class="deck-card-overlay"></div>
                    <div class="deck-card-info">
                        <h1>${deck.name || 'Untitled Deck'}</h1>
                        <h2>${deck.format && deck.format !== 'None' ? deck.format : ''}</h2>
                    </div>
                `;
                grid.appendChild(cardEl);
            });

            renderPagination();
        }

        function getMostExpensiveCard(deck) {
            const board = (deck.mainboard || []);
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

        function renderPagination() {
            const pagination = document.getElementById('pagination');
            pagination.innerHTML = '';

            const totalPages = Math.ceil(filteredDecks.length / itemsPerPage);
            if (totalPages <= 1) return;

            const prevBtn = document.createElement('button');
            prevBtn.innerText = 'Previous';
            prevBtn.disabled = currentPage === 1;
            prevBtn.onclick = () => { currentPage--; renderDecks(); };
            pagination.appendChild(prevBtn);

            for (let i = 1; i <= totalPages; i++) {
                const btn = document.createElement('button');
                btn.innerText = i;
                if (i === currentPage) btn.className = 'active';
                btn.onclick = () => { currentPage = i; renderDecks(); };
                pagination.appendChild(btn);
            }

            const nextBtn = document.createElement('button');
            nextBtn.innerText = 'Next';
            nextBtn.disabled = currentPage === totalPages;
            nextBtn.onclick = () => { currentPage++; renderDecks(); };
            pagination.appendChild(nextBtn);
        }

        init();
    </script>
</body>
</html>'''

    with open(output_html_file, 'w', encoding='utf-8-sig') as f:
        f.write(html_content)
    print(f"Generated {output_html_file}")

if __name__ == "__main__":
    generateHTML()
