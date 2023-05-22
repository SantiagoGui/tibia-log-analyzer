import re
import json
from collections import defaultdict

total_damage = 0
total_healed = 0
total_experience = 0
total_mana = 0
creature_hits = defaultdict(int)
loot_items = defaultdict(int)
black_knight_life = 0
lose_pattern = re.compile(r"lose (\d+) (.+)$")
yourself_heal_pattern = re.compile(r"healed yourself for \d+")
experience_pattern = re.compile(r"You gained (\d+) exp")
mana_pattern = re.compile(r"You gained (\d+) mana")
loot_pattern = re.compile(r"Loot of a")

with open("logfile.txt", "r") as arquivo:
    for line in arquivo:
        # Extracting damage and damage_by_creature
        if lose_pattern.search(line):
            word_array = lose_pattern.search(line).group().replace(".", "").split()
            damage = int(word_array[1])
            creature = word_array[-1]
            if len(word_array) == 11:
                creature = word_array[-2] + " " + creature
            if creature not in ["hitpoint", "hitpoints"]:
                creature_hits[creature] += damage

            total_damage += damage
        # Extracting total healed by the player
        elif yourself_heal_pattern.search(line):
            word_array = yourself_heal_pattern.search(line).group().replace(".", "").split()
            heal = int(word_array[-1])
            total_healed += int(heal)
        # Extracting total experience gained by the player
        elif experience_pattern.search(line):
            word_array = experience_pattern.search(line).group().replace(".", "").split()
            experience = int(word_array[-2])
            total_experience += int(experience)

        elif mana_pattern.search(line):
            word_array = mana_pattern.search(line).group().replace(".", "").split()
            mana = int(word_array[-2])
            total_mana += int(mana)

        # Extracting Black Knight life
        elif re.search("A Black Knight loses", line):
            splited_line = line.strip().split(" ")
            black_knight_life += int(splited_line[5])

        # Extracting items dropped by creatures
        match = re.search(r"Loot of a (\w+(?: \w+)*): ([\w\s',]+)\.", line)
        if match:
            itens = match.group(2).split(', ')
            for item in itens:
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
                    loot_items[name] += amount

result = {
    "hitpointsHealed": total_healed,
    "damageTaken": {
        "total": total_damage,
        "byCreatureKind": creature_hits
    },
    "experienceGained": total_experience,
    "manaGained": total_mana,
    "loot": loot_items,
    "creatureTotalLife": {
        "blackKnight": black_knight_life

    }
}

json = json.dumps(result, indent=4)
print(json)

