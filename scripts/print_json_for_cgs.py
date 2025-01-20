import json

def generateJSON(username):
	output_json_file = "cgs.json"
	cgs = {}

	cgs["allCardsUrl"] = f"https://{username}.github.io/lists/all-cards.json"
	cgs["allSetsUrl"] = f"https://{username}.github.io/lists/all-sets.json"
	cgs["autoUpdateUrl"] = f"https://{username}.github.io/cgs.json"
	cgs["bannerImageUrl"] = f"https://{username}.github.io/img/banner.png"
	cgs["cardBackImageUrl"] = f"https://{username}.github.io/img/card_back.png"
	cgs["cardDataIdentifier"] = "cards"
	cgs["cardIdIdentifier"] = "card_id"
	cgs["cardImageUrl"] = f"https://{username}.github.io"+"{image_path}"
	cgs["cardNameIdentifier"] = "card_name"
	cgs["cardSetIdentifier"] = "set"
	cgs["cardPrimaryProperty"] = "rules_text"

	cgs["cardProperties"] = [
		{
			"name": "number",
			"display": "Card Number",
			"type": "integer"
		},
		{
			"name": "color",
			"delimiter": "",
			"display": "Color",
      		"displayEmpty": "Colorless",
			"type": "stringEnumList"
		},
		{
			"name": "rarity",
			"display": "Rarity",
			"type": "string"
		},
		{
			"name": "type",
			"display": "Type",
			"type": "string"
		},
		{
			"name": "color_identity",
			"delimiter": "",
			"display": "Color Identity",
			"displayEmpty": "Colorless",
			"type": "stringEnumList"
		},
		{
			"name": "cost",
			"display": "Cost",
			"type": "string"
		},
		{
			"name": "rules_text",
			"display": "Rules Text",
			"type": "string"
		},
		{
			"name": "pt",
			"display": "Power/Toughness",
			"type": "string"
		},
		{
			"name": "special_text",
			"display": "Special Text",
			"type": "string"
		},
		{
			"name": "shape",
			"display": "Shape",
			"type": "string"
		},
		{
			"name": "loyalty",
			"display": "Loyalty",
			"type": "integer"
		},
		{
			"name": "notes",
			"display": "Notes",
			"type": "string"
		},
		{
			"name": "image_path",
			"display": "Image Path",
			"type": "string"
		}
	]

	cgs["copyright"] = username
	cgs["deckSharePreference"] = "individual"

	cgs["enums"] = [
		{
			"property": "color",
			"values": {
				"W": "White",
				"U": "Blue",
				"B": "Black",
				"R": "Red",
				"G": "Green"
			}
		},
		{
			"property": "color_identity",
			"values": {
				"W": "White",
				"U": "Blue",
				"B": "Black",
				"R": "Red",
				"G": "Green"
			}
		},
		{
			"property": "rarity",
			"values": {
				"common": "Common",
				"uncommon": "Uncommon",
				"rare": "Rare",
				"mythic": "Mythic Rare"
			}
		}
	]

	cgs["gameDefaultCardAction"] = "tap"
	cgs["gameStartHandCount"] = 7
	cgs["gameStartPointsCount"] = 20
	cgs["name"] = username
	cgs["rulesUrl"] = f"https://{username}.github.io/"

	# Write the JSON content to the output JSON file
	with open(output_json_file, 'w', encoding='utf-8-sig') as file:
		json.dump(cgs, file, indent=4)

	print(f"JSON file saved as {output_json_file}")
