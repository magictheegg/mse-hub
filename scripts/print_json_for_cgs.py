import json
import os

def generateJSON():
	output_json_file = "cgs.json"
	cgs = {}

	domain = os.path.basename(os.getcwd())
	username = domain.split(".")[0]

	cgs["allCardsUrl"] = f"https://{domain}/lists/all-cards.json"
	cgs["allSetsUrl"] = f"https://{domain}/lists/all-sets.json"
	cgs["autoUpdateUrl"] = f"https://{domain}/{output_json_file}"
	cgs["bannerImageUrl"] = f"https://{domain}/img/banner.png"
	cgs["cardBackImageUrl"] = f"https://{domain}/img/card_back.png"
	cgs["cardDataIdentifier"] = "cards"
	cgs["cardIdIdentifier"] = "card_id"
	cgs["cardImageUrl"] = f"https://{domain}"+"{image_path}"
	cgs["cardNameBackIdentifier"] = "card_name2"
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
			"type": "stringEnumList",
			"frontName": "color",
			"backName": "color2"
		},
		{
			"name": "rarity",
			"display": "Rarity",
			"type": "string"
		},
		{
			"name": "type",
			"display": "Type",
			"type": "string",
			"frontName": "type",
			"backName": "type2"
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
			"type": "string",
			"frontName": "cost",
			"backName": "cost2"
		},
		{
			"name": "rules_text",
			"display": "Rules Text",
			"type": "string",
			"frontName": "rules_text",
			"backName": "rules_text2"
		},
		{
			"name": "pt",
			"display": "Power/Toughness",
			"type": "string",
			"frontName": "pt",
			"backName": "pt2"
		},
		{
			"name": "loyalty",
			"display": "Loyalty",
			"type": "integer",
			"frontName": "loyalty",
			"backName": "loyalty2"
		},
		{
			"name": "flavor_text",
			"display": "Flavor Text",
			"type": "string",
			"frontName": "flavor_text",
			"backName": "flavor_text2"
		},
		{
			"name": "artist",
			"display": "Artist",
			"type": "string",
			"frontName": "artist",
			"backName": "artist2"
		},
		{
			"name": "image_path",
			"display": "Image Path",
			"type": "string",
			"frontName": "image_path",
			"backName": "image_path2"
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
	cgs["rulesUrl"] = f"https://{domain}/"
	cgs["setCodeIdentifier"] = "set_code"
	cgs["setDataIdentifier"] = "sets"
	cgs["setNameIdentifier"] = "set_name"

	# Write the JSON content to the output JSON file
	with open(output_json_file, 'w', encoding='utf-8-sig') as file:
		json.dump(cgs, file, indent=4)

	print(f"JSON file saved as {output_json_file}")
