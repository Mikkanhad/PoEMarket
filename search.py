### Resources ###
# https://www.pathofexile.com/api/trade/data/stats


'''
Builds a query as a Dictionary object, dumps that dictionary to JSON to be posted
as query to the Path of Exile Trade Search

"query"
    "status" - online or offline (string)
    "name" - name of item, unique item, div card, etc.
    "type" - item base (Iron Ring, Unset Ring, Vaal Axe)
    "stats" - filter groups/options ***(LIST)***
        "type" - "not", "and", "count", "if", "weighted sum"
        "filters" - Mods from the item like attack speed or % increased physical
            "id" - identifier from [https://www.pathofexile.com/api/trade/data/stats] for each affix on items
            "value" - filtering for values within given range
                "min" - Minimum value (float)
                "max" - Maximum value (float)
                "disabled" - Boolean used to determine whether listed affix will be considered in the search

    "filters" - Dictionary of different filter groups
        "weapon_filters"
            "disabled"
            "filters"
                "damage"
                    "min"
                    "max"
                "crit"
                    "min"
                    "max"
                "aps"
                    "min"
                    "max"
                "dps"
                    "min"
                    "max"
                "edps"
                    "min"
                    "max"
                "pdps"
                    "min"
                    "max"
        "armour_filters"
            "disabled"
            "filters"
                "ar" - Armor
                    "min"
                    "max"
                "es" - Energy Shield
                    "min"
                    "max"
                "ev" - Evasion
                    "min"
                    "max"
                "block" - ...
                    "min"
                    "max"
        "socket_filters"
            "disabled"
            "filters"
                "sockets"
                    "min"
                    "max"
                    "r"
                    "g"
                    "b"
                    "w"
                "links"
                    "min"
                    "max"
                    "r"
                    "g"
                    "b"
                    "w"
        "req_filters"
            "disabled"
            "filters"
                "lvl"
                    "min"
                    "max"
                "dex"
                    "min"
                    "max"
                "str"
                    "min"
                    "max"
                "int"
                    "min"
                    "max"
        "misc_filters"
            "disabled"
            "filters"
                "quality"
                    "min"
                    "max"
                "map_tier"
                    "min"
                    "max"
                "map_iiq"
                    "min"
                    "max"
                "gem_level"
                    "min"
                    "max"
                "ilvl"
                    "min"
                    "max"
                "map_packsize"
                    "min"
                    "max"
                "map_iir"
                    "min"
                    "max"
                "talisman_tier"
                    "min"
                    "max"
                "alternate_art"
                    "option" - STRING BOOL ie. "true"
                "identified"
                    "option"
                "corrupted"
                    "option"
                "crafted"
                    "option"
                "enchanted"
                    "option"
        "trade_filters"
            "disabled"
            "filters"
                "account"
                    "input"
                "sale_type"
                    "option"
                "price"
                    "min"
                    "max"
        "type_filters" - Filter for item class
            "filters"
                "category"
                    "option" - id for item class
                "rarity"
                    "option"
    "sort"
        "price" - Ascending (asc) or Descending (dsc)
'''

import json
import requests

API_URL = "https://www.pathofexile.com/api/trade/search/Metamorph"
TRADE_URL = "https://www.pathofexile.com/api/trade/fetch/"
headers = {'content-type': 'application/json',
           'X-Requested-With': 'XMLHttpRequest'}

query = {"query": {"status": "online",
                   "name": "The Saviour",
                   "stats": [{"type": "and",
                              "filters": []}]},
         "sort": {"price": "asc"}
         }


def build_query(target: dict, category: str, content: dict):
    target[category] = content
    return target


def build_url(api_result, api_id):
    url = TRADE_URL
    url_collection = []
    id_counter = 0
    for element in api_result[:10]:
        if api_result[0] == element:
            url += element
        else:
            url += "," + element
    url += "?query=" + api_id
    url_collection.append(url)
    if len(api_result) > 10:
        url_collection.extend(build_url(api_result[10:], api_id))
    return url_collection


if "__name__" == "__main__":
    r = requests.get(API_URL, data=json.dumps(query), headers=headers)
    results = json.loads(r.text)
    for link in build_url(results['result'], results['id']):
        print(link)
