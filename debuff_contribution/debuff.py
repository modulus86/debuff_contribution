import requests
import pprint
import sys


def nop():
    return 0

base_url = 'https://www.warcraftlogs.com/v1'
fights = '/report/fights'
tables = '/report/tables/damage-done'

key = sys.argv[1]
report = '/' + sys.argv[2]


# These are example reports: first report only has 1 monk - Windwalker; the 2nd only has 1 monk - Brew Master
#report = '/CZ1X9txqk3KV8fjy'
#report = '/FBNYw7htHTgaKcxr'

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

    #print(start, end)
    p =     { 'start' : start,
               'end' : end,
               'api_key' : key}

    encounter = {}


    encounter['physical_debuff'] = False
    encounter['magic_debuff'] = False
    #print("Encounter ID: " +str(n['id']))

    for player in raid_comp:
        #print(player['name'] + ":" + str(player['id']))

        pid = 0
        if player['type'] == 'NPC':
            #print("NPC found, skipping")
            continue
        for f in player['fights']:
            if f['id'] == n['id']:
                #print("Found Encounter ID in player's fight list: " + str(n['id']))
                pid = player['id']
                break
        if pid == 0:
            #print("Player is not in this encounter, skipping")
            continue

        p = {'start': start,
             'end': end,
             'sourceid' : pid,
             'api_key': key}

        damage_tables = requests.get(base_url + tables + report, params=p )

        #print(damage_tables.url)

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
        #print(json)
        for e in json:
            #print("Name: " + str(e['name']))
            #print("Total Damage: " + str(e['total']))
            #print("Spell Type: " + str(e['type']))

            if 'subentries' in e.keys():
                for se in e['subentries']:
                    #print("Name: " + str(se['name']))
                    #print("Total Damage: " + str(se['total']))
                    #print("Spell Type: " + str(se['type']))
                    if se['type'] == 1:
                        encounter[pid]['physical_damage'] = encounter[pid]['physical_damage'] + int(se['total'])
                    else:
                        encounter[pid]['magical_damage'] = encounter[pid]['magical_damage'] + int(se['total'])
            else:
                if e['type'] == 1:
                    encounter[pid]['physical_damage'] = encounter[pid]['physical_damage'] + int(e['total'])
                else:
                    encounter[pid]['magical_damage'] = encounter[pid]['magical_damage'] + int(e['total'])

    #pprint.pprint(encounter)

    length = int( (end - start) / 1000)


    magic_contribution = 0
    magic_benefitees = 0
    physical_contribution = 0
    physical_benefitees = 0



  #  encounter['magic_debuff'] = True

    print(n['name'])
    print("Encounter length", length)
    for p in encounter:

        if 'debuff' in str(p):
            continue
        #print(encounter[p]['name'])
        if encounter['physical_debuff'] == True:

            with_buff_damage = encounter[p]['physical_damage']
            with_buff_removed = int( (with_buff_damage)/1.05 )
            buff_contribution = with_buff_damage - with_buff_removed

            physical_contribution += buff_contribution

            if not with_buff_damage > 0:
                #print("This player did no physical damage!")
                continue
            else:
                nop()
                physical_benefitees += 1
                #print('Physical damage done with debuff: ',with_buff_damage)
                #print('Physical damage done without the debuff: ',with_buff_removed)
                #print('Physical damage debuff contributed: ', buff_contribution)
        if encounter['magic_debuff'] == True:

            with_buff_damage = encounter[p]['magical_damage']
            with_buff_removed = int( (with_buff_damage)/1.05 )
            buff_contribution = with_buff_damage - with_buff_removed

            magic_contribution += buff_contribution

            if not with_buff_damage > 0:
                #print("This player did no magical damage damage!")
                continue
            else:
                nop()
                magic_benefitees += 1
                #print('Magical damage done with debuff: ',with_buff_damage)
                #print('Magical damage done without the debuff: ',with_buff_removed)
                #print('Magical damage debuff contributed: ', buff_contribution)


    print('Total Physical damage debuff contribution:',physical_contribution)
    if physical_benefitees > 0:
        print("Physical damage DPS contribution:", (physical_contribution / length))
        print("The number of sources with a physical damage component", physical_benefitees)
        print("The average damage per second gained per source:", (physical_contribution / length) / (physical_benefitees))
        print("The average damage gain per source:", (physical_contribution) / physical_benefitees)

    print('Total Magic damage debuff contribution:', magic_contribution)
    if magic_benefitees > 0:
        print("Magic damage DPS contribution:", (magic_contribution / length))
        print("The number of sources with a magic damage component:", magic_benefitees)
        print("The average damage gain per source:",(magic_contribution) / magic_benefitees)
        print("The average damage per second gained per source:", (magic_contribution / length) / (magic_benefitees))




