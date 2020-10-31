import requests
import pprint
import sys

base_url = 'https://www.warcraftlogs.com/v1'
fights = '/report/fights'
tables = '/report/tables/damage-done'

key = sys.argv[1]
report = '/' + sys.argv[2]


p = {
    'api_key' : key
}

req = requests.get(
    base_url + fights + report, params=p
)


if (req.status_code != 200):
    print(req.url)
    print(req.status_code)
    exit()


raid_comp = req.json()['friendlies']
raid_encounter = req.json()['fights']

for n in raid_encounter:
    if n['boss'] == 0:
        continue
    start, end = n['start_time'], n['end_time']

    print(start, end)
    p =     { 'start' : start,
               'end' : end,
               'api_key' : key}

    encounter = {}


    encounter['physical_debuff'] = False
    encounter['magic_debuff'] = False
    print("Encounter ID: " +str(n['id']))

    for player in raid_comp:
        print(player['name'] + ":" + str(player['id']))

        pid = 0
        if player['type'] == 'NPC':
            print("NPC found, skipping")
            continue
        for f in player['fights']:
            if f['id'] == n['id']:
                print("Found Encounter ID in player's fight list: " + str(n['id']))
                pid = player['id']
                break
        if pid == 0:
            print("Player is not in this encounter, skipping")
            continue

        p = {'start': start,
             'end': end,
             'sourceid' : pid,
             'api_key': key}

        damage_tables = requests.get(base_url + tables + report, params=p )

        print(damage_tables.url)

        encounter[pid] = {}
        encounter[pid]['name'] = player['name']
        encounter[pid]['physical_damage'] = 0
        encounter[pid]['magical_damage'] = 0


       # print(damage_tables.url)
       # print(player['name'])
       # print(player['type'])

        if player['type'] == 'Monk':
            encounter['physical_debuff'] = True
        elif player['type'] == 'DemonHunter':
            encounter['magic_debuff'] = True

        #print(player['name'])

        json = damage_tables.json()['entries']
        print(json)
        for e in json:
            print("Name: " + str(e['name']))
            print("Total Damage: " + str(e['total']))
            print("Spell Type: " + str(e['type']))

            if 'subentries' in e.keys():
                for se in e['subentries']:
                    print("Name: " + str(se['name']))
                    print("Total Damage: " + str(se['total']))
                    print("Spell Type: " + str(se['type']))
                    if se['type'] == 1:
                        encounter[pid]['physical_damage'] = encounter[pid]['physical_damage'] + int(se['total'])
                    else:
                        encounter[pid]['magical_damage'] = encounter[pid]['magical_damage'] + int(se['total'])
            else:
                if e['type'] == 1:
                    encounter[pid]['physical_damage'] = encounter[pid]['physical_damage'] + int(e['total'])
                else:
                    encounter[pid]['magical_damage'] = encounter[pid]['magical_damage'] + int(e['total'])

    pprint.pprint(encounter)

  #  encounter['magic_debuff'] = True
    for p in encounter:
        if 'debuff' in str(p):
            continue
        print(encounter[p]['name'])
        if encounter['physical_debuff'] == True:

            with_buff_damage = encounter[p]['physical_damage']
            with_buff_removed = int( (with_buff_damage)/1.05 )
            buff_contribution = with_buff_damage - with_buff_removed

            if not with_buff_damage > 0:
                print("This player did no physical damage!")
            else:
                print('Physical damage done with debuff: ',with_buff_damage)
                print('Physical damage done without the debuff: ',with_buff_removed)
                print('Physical damage debuff contributed: ', buff_contribution)
        if encounter['magic_debuff'] == True:

            with_buff_damage = encounter[p]['magical_damage']
            with_buff_removed = int( (with_buff_damage)/1.05 )
            buff_contribution = with_buff_damage - with_buff_removed

            if not with_buff_damage > 0:
                print("This player did no magical damage damage!")
            else:
                print('Magical damage done with debuff: ',with_buff_damage)
                print('Magical damage done without the debuff: ',with_buff_removed)
                print('Magical damage debuff contributed: ', buff_contribution)

    exit()



