import re
total_damage = 0
hit_points_healed = 0
experience_gained = 0
damage_taken_by_creature_kind = {}
loot_items = {}

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

