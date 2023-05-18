import re
from collections import defaultdict

unknow_total_damage = 0
total_damage = 0
hit_points_healed = 0
experience_gained = 0
mana_gained = 0
damage_taken_by_creature_kind = defaultdict(int)
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
                damage_taken_by_creature_kind[creature_name] += creature_hit
            else:
                unknow_damage = int(splitted_line[3])
                total_damage += unknow_damage
                unknow_total_damage += unknow_damage

        if re.search("You healed", line):
            splited_line = line.strip().split(" ")
            hit_points_healed += int(splited_line[5])

        if re.search("You gained", line):
            splited_line = line.strip().split(" ")
            if len(splited_line) == 6:
                experience_gained += int(splited_line[3])
            else:
                mana_gained += int(splited_line[3])

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
                    loot_items[name] += amount

'''
fazer os extras
passar as variaveis pra um dic dicionario ou jason
'''

print("LOOT: " + str(loot_items))
print("XP: " + str(experience_gained))
print("MANA :" + str(mana_gained))
print("Damage: " + str(total_damage))
print("hitpoint :" + str(hit_points_healed))
print("creature kind: " + str(damage_taken_by_creature_kind))
print("UNKNOW TOTAL DAMAGE: " + str(unknow_total_damage))