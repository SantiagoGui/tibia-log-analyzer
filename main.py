import re
import json
from collections import defaultdict

output = {
    "unknow_total_damage": 0,
    "total_damage": 0,
    "hit_points_healed": 0,
    "experience_gained": 0,
    "mana_gained": 0,
    "damage_taken_by_creature_kind": defaultdict(int),
    "loot_items": defaultdict(int),
    "black_knight_life": 0
}

with open("logfile.txt", "r") as arquivo:
    for line in arquivo:
        if re.search("You lose", line):
            splitted_line = line.strip().split(" ")
            if len(splitted_line) > 5:
                if len(splitted_line) == 12:
                    creature_hit = int(splitted_line[3])
                    creature_name = splitted_line[-1].replace(".", "")
                    output["total_damage"] += creature_hit
                elif len(splitted_line) == 13:
                    creature_hit = int(splitted_line[3])
                    creature_name = (splitted_line[-2] + " " + splitted_line[-1]).replace(".", "")
                    output["total_damage"] += creature_hit
                output["damage_taken_by_creature_kind"][creature_name] += creature_hit
            else:
                unknow_damage = int(splitted_line[3])
                output["total_damage"] += unknow_damage
                output["unknow_total_damage"] += unknow_damage

        if re.search("You healed", line):
            splited_line = line.strip().split(" ")
            output["hit_points_healed"] += int(splited_line[5])

        if re.search("You gained", line):
            splited_line = line.strip().split(" ")
            if len(splited_line) == 6:
                output["experience_gained"] += int(splited_line[3])
            else:
                output["mana_gained"] += int(splited_line[3])

        if re.search("A Black Knight loses", line):
            splited_line = line.strip().split(" ")
            output["black_knight_life"] += int(splited_line[5])

        loot_match = re.search("Loot of a (\w+): ([\w\s',]+)\.", line)
        if loot_match:
            items = loot_match.group(2).split(', ')
            for item in items:
                if re.search('nothing', item) is None:

                    item_parts = item.strip().split(' ', 1)
                    if len(item_parts) == 2:
                        amount, name = item_parts
                    else:
                        amount = '1'
                        name = item_parts[0]
                    amount = amount.strip() if amount else '1'
                    name = name.strip() if name else item
                    amount = int(amount) if amount.isdigit() else 1
                    if name.startswith('a '):
                        name = name[2:]
                    name = name.strip()
                    if name.endswith('s') and name[:-1]:
                        name = name[:-1]
                    output["loot_items"][name] += amount

json = json.dumps(output, indent=4)
print(json)

