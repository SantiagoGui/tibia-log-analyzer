import json
from collections import defaultdict

output = {
    "hitpointsHealed": 0,
    "experienceGained": 0,
    "manaGained": 0,
    "damageTaken": {
        "total": 0,
        "unknowOrigins": 0,
        "byCreatureKind": defaultdict(int)
    },
    "loot": defaultdict(int),
    "creaturesTotalLife": {
        "blackKnight": 0
    }
}

with open("logfile.txt", "r") as arquivo:
    for line in arquivo:
        splitted_line = line.strip().split(" ")
        if "You" in splitted_line and "lose" in splitted_line:
            if len(splitted_line) > 5:
                if len(splitted_line) == 12:
                    creature_hit = int(splitted_line[3])
                    creature_name = splitted_line[-1].replace(".", "")
                    output["damageTaken"]["total"] += creature_hit
                elif len(splitted_line) == 13:
                    creature_hit = int(splitted_line[3])
                    creature_name = (splitted_line[-2] + " " + splitted_line[-1]).replace(".", "")
                    output["damageTaken"]["total"] += creature_hit
                output["damageTaken"]["byCreatureKind"][creature_name] += creature_hit
            else:
                unknow_damage = int(splitted_line[3])
                output["damageTaken"]["total"] += unknow_damage
                output["damageTaken"]["unknowOrigins"] += unknow_damage
        if "You" in splitted_line and "healed" in splitted_line:
            output["hitpointsHealed"] += int(splitted_line[5])

        if "You" in splitted_line and "gained" in splitted_line:
            if len(splitted_line) == 6:
                output["experienceGained"] += int(splitted_line[3])
            else:
                output["manaGained"] += int(splitted_line[3])
        if "A Black Knight loses" in line:
            output["creaturesTotalLife"]["blackKnight"] += int(splitted_line[5])

        splitted_line = line.strip().split(":")
        if len(splitted_line) > 1:
            if "Loot" in splitted_line[1]:
                items = splitted_line[2].strip().split(",")
                for item in items:
                    if "nothing" not in item:
                        item_parts = item.strip().split(' ')
                        if len(item_parts) >= 3:
                            amount = 1
                            if item_parts[0].isdigit():
                                amount = int(item_parts[0])
                                item_parts.pop(0)
                            if item_parts[0] == 'a':
                                amount = 1
                                item_parts.pop(0)
                            name = " ".join(item_parts).replace(".", "")
                        elif len(item_parts) == 2:
                            if item_parts[0].isdigit():
                                amount = int(item_parts[0])
                                item_parts.pop(0)
                            else:
                                amount = 1
                            name = " ".join(item_parts).replace(".", "")
                        elif len(item_parts) == 1:
                            amount = 1
                            name = item_parts[0].replace(".", "")
                        if name.startswith('a '):
                            name = name[2:]
                            name = name.strip()
                        if name.endswith('s') and name[:-1]:
                            name = name[:-1]
                        output["loot"][name] += amount

json = json.dumps(output, indent=4)
print(json)

