import re
from collections import defaultdict

total_damage = 0
hit_points_healed = 0
experience_gained = 0
mana_gained = 0
damage_taken_by_creature_kind = {}
loot_items = defaultdict(int)

with open("logfile.txt", "r") as arquivo:
    for line in arquivo:
        if re.search("You lose", line):
            splitted_line = line.strip().split(" ")
            if len(splitted_line) > 5:
                if len(splitted_line) == 12:
                    creature_hit = int(splitted_line[3])
                    creature_name = splitted_line[-1].replace(".", "")
                    total_damage += creature_hit
                elif len(splitted_line) == 13:
                    creature_hit = int(splitted_line[3])
                    creature_name = (splitted_line[-2] + " " + splitted_line[-1]).replace(".", "")
                    total_damage += creature_hit
                if creature_name in damage_taken_by_creature_kind:
                    damage_taken_by_creature_kind[creature_name] += creature_hit
                else:
                    damage_taken_by_creature_kind[creature_name] = creature_hit
            else:
                total_damage += int(splitted_line[3])

        if re.search("You healed", line):
            splited_line = line.strip().split(" ")
            hit_points_healed += int(splited_line[5])

        if re.search("You gained", line):
            splited_line = line.strip().split(" ")
            if len(splited_line) == 6:
                experience_gained += int(splited_line[3])
            else:
                mana_gained += int(splited_line[3])

        match = re.search("Loot of a (\w+): ([\w\s',]+)\.", line)
        if match:
            itens = match.group(2).split(', ')
            for item in itens:
                temnothing = re.search('nothing', item)
                if temnothing is None:
                    item_parts = item.strip().split(' ', 1)
                    if len(item_parts) == 2:
                        quantidade, nome = item_parts
                    else:
                        quantidade = '1'
                        nome = item_parts[0]
                    quantidade = quantidade.strip() if quantidade else '1'
                    nome = nome.strip() if nome else item
                    quantidade = int(quantidade) if quantidade.isdigit() else 1
                    if nome.startswith('a '):
                        nome = nome[2:]
                    nome = nome.strip()
                    if nome.endswith('s') and nome[:-1]:
                        nome = nome[:-1]
                    loot_items[nome] += quantidade



print("LOOT: " + str(loot_items))
print("XP: " + str(experience_gained))
print("MANA :" + str(mana_gained))
print("Damage: " + str(total_damage))
print("hitpoint :" + str(hit_points_healed))
print("creature kind: " + str(damage_taken_by_creature_kind))