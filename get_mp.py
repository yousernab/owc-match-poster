import time
import requests
import csv
import praw
from bracket import *
from members import *

def get_match_info(match_id):
    url = f"https://osu.ppy.sh/api/get_match?k=YOUR_API_KEY&mp={match_id}"
    # TODO: Replace 'YOUR_API_KEY' with your actual osu! API key
    try:
        response = requests.get(url)
        return response.json()
    except:
        return -1

def get_beatmap_info(beatmap_id):
    url = f"https://osu.ppy.sh/api/get_beatmaps?k=YOUR_API_KEY&b={beatmap_id}"
    # TODO: Replace 'YOUR_API_KEY' with your actual osu! API key
    response = requests.get(url)
    return response.json()

def get_user_info(username):
    url = f"https://osu.ppy.sh/api/get_user?k=YOUR_API_KEY&u={username}"
    # TODO: Replace 'YOUR_API_KEY' with your actual osu! API key
    response = requests.get(url)
    return response.json()

def read_game_info(game_info, players):
    beatmap_info = get_beatmap_info(game_info['beatmap_id'])
    red_score = sum(int(score['score']) for score in game_info['scores'] if int(score['team']) == 2)
    blue_score = sum(int(score['score']) for score in game_info['scores'] if int(score['team']) == 1)
    average_score = (red_score + blue_score) / len(game_info['scores'])
    result = None
    if red_score > blue_score:
        game_info['scores'].sort(key = lambda x: (-int(x['team']), -int(x['score'])))
        result = [1, 0]
    elif blue_score > red_score:
        game_info['scores'].sort(key = lambda x: (int(x['team']), -int(x['score'])))
        result = [0, 1]
    else:
        game_info['scores'].sort(key = lambda x: (-int(x['team']), -int(x['score'])))
        result = [0, 0]
    
    for score in game_info['scores']:
        if score['user_id'] not in players:
            user_info = get_user_info(score['user_id'])
            players[score['user_id']] = {
                'username': user_info[0]['username'].replace("[", "&#91;").replace("]", "&#93;"),
                'team': score['team'],
                'match_sum': 0,
                'games_played': 0         
            }
        players[score['user_id']]['match_sum'] += int(score['score']) / average_score
        players[score['user_id']]['games_played'] += 1

    return result, red_score, blue_score

# def match_costs(players):
#     mc = [{}, {}]
#     for user_id, player in players.items():
#         mc[2 - int(player['team'])]["[" + player['username'] + "](https://osu.ppy.sh/users/" + user_id + ")"] = 2 * player['match_sum'] / (player['games_played'] + 2)
#     return mc

def match_costs(players, countries, members):
    mc = [{}, {}]
    for user_id, player in players.items():
        mc[2 - int(player['team'])]["[" + player['username'] + "](https://osu.ppy.sh/users/" + user_id + ")"] = 2 * player['match_sum'] / (player['games_played'] + 2)
    for i in range(2):
        for member in members[countries[i]]:
            if member not in mc[i]:
                mc[i][member] = -1
    return mc

def reddit_post(title, markdown): # TODO: reddit api
    reddit = praw.Reddit(client_id="",
                         client_secret="",
                         username="",
                         password="",
                         user_agent="")
    subreddit = reddit.subreddit("osugame")
    subreddit.submit(title, flair_id="46adc6b4-89df-11e4-8434-22000bc18bb2", selftext=markdown, spoiler=True)
    return

def get_mappool(file_name):
    file = open("C:\\Users\\Alex\\Downloads\\owc2025\\mappools\\" + file_name + ".csv", mode='r', encoding='utf-8')
    csv_reader = csv.DictReader(file)
    mappool = {}
    for row in csv_reader:
        mappool[row['id']] = row
        mappool[row['map id']] = row
    file.close()
    return mappool

stage = None
first_to = None
mappool = None

def get_bans():
    print("Enter bans (prefix with 'r' for red, 'b' for blue; 'Enter' to finish):")
    red_bans = []
    blue_bans = []
    ban = input()
    while ban != '':
        if ban[:1] == 'r':
            red_bans.append(ban[1:].upper())
        if ban[:1] == 'b':
            blue_bans.append(ban[1:].upper())
        ban = input()
    return red_bans, blue_bans

def get_pick_order():
    colour = input("Which team has first pick (r/b)?")
    if colour == 'r':
        return 0
    if colour == 'b':
        return 1
    return -1

match_id = input("Enter match ID:")

match_name = get_match_info(match_id)['match']['name']
countries = [match_name.split('(')[1].split(')')[0], match_name.split('(')[2].split(')')[0]]

print()
print(countries[0] + " vs " + countries[1])
print()

(stage, win_message, lose_message) = get_info(countries[0], countries[1])

curr_stage = ""
if stage == "Showmatch":
    curr_stage = input("Current Round?")
    first_to = curr_first_to[curr_stage]
    mappool = get_mappool(curr_mappool[curr_stage])
    curr_stage = curr_stage + " "
else:
    first_to = curr_first_to[stage]
    mappool = get_mappool(curr_mappool[stage])

pick = get_pick_order()
red_bans, blue_bans = get_bans()
if pick == -1:
    pick = get_pick_order()

print()
title = "[Spoilers] | " + countries[0] + " vs " + countries[1] + " | OWC 2025 " + curr_stage + stage + " | Post-Match Discussion"
print(title)
print("match link: https://osu.ppy.sh/community/matches/" + match_id)
print("red bans: " + ", ".join(red_bans))
print("blue bans: " + ", ".join(blue_bans))
print("first pick: " + ("red" if pick == 0 else "blue" if pick == 1 else "none"))
print("win message: " + win_message)
print("lose message: " + lose_message)

members = {
    countries[0]: get_members(countries[0]),
    countries[1]: get_members(countries[1])
}

score = [0, 0]
players = {}
counter = 0
abort = 0
match_markdown = ""

while(score[0] < first_to and score[1] < first_to):
    match_info = get_match_info(match_id)

    # give point
    if counter == -1 and score[-1] == -1:
        score[-1] += 1

    # skip point
    if counter == -1 and abort == 0:
        abort += 1

    if score[0] < first_to - 1 and score[1] < first_to - 1 and 'games' in match_info and len(match_info['games']) <= counter + abort + 1:
        time.sleep(8)
    time.sleep(2)
    if 'games' in match_info and len(match_info['games']) > counter + abort + 1 and match_info['games'][counter + abort]['end_time'] == None:
        abort += 1
    if 'games' in match_info and len(match_info['games']) > counter + abort and match_info['games'][counter + abort]['end_time'] != None:
        game_info = match_info['games'][counter + abort]
        result, red_score, blue_score = read_game_info(game_info, players)
        score[0] += result[0]
        score[1] += result[1]
        team = result[1]

        # flip point
        if counter == -1:
            score[0] += result[1] - result[0]
            score[1] += result[0] - result[1]
            team = result[0]
            result[0] = 1 - result[0]
            result[1] = 1 - result[1]
            # first = [score_info for score_info in game_info['scores'] if score_info['team'] == 2 - team]
            # second = [score_info for score_info in game_info['scores'] if score_info['team'] != 2 - team]
            # game_info['scores'] = first + second

        match_markdown += "***\n###Map " + str(counter + 1)
        if counter == first_to * 2 - 2:
            match_markdown += " (Tiebreaker)"
        elif pick == 0 or pick == 1:
            match_markdown += " (picked by " + countries[pick] + ")"
        # else:
        #     if pick == 1:
        #         match_markdown += " (picked by M I L E S and chat)"
        #     if pick == 0:
        #         match_markdown += " (picked by Dada and chat)"
        match_markdown += "\n***\n\n"
        
        map_info = mappool[game_info['beatmap_id']]

        match_markdown += "####" + map_info['id'] + " | [" + map_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + map_info['map id'] + ")\n\n"
        match_markdown += map_info['length'][1:] + " — " + map_info['bpm'] + " BPM — " + map_info['sr'] + " — " + "{:,}".format(int(map_info['combo'])) + "x\n\n"
        match_markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"
        match_markdown += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
        for score_info in game_info['scores']:
            if 2 - team != int(score_info['team']):
                team = 1 - team
                match_markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"

            player_info = players[score_info['user_id']]
            mods = ""
            if score_info['enabled_mods'] is not None and int(score_info['enabled_mods']) > 1:
                if int(score_info['enabled_mods']) & 2 > 0:
                    mods += "EZ"
                if int(score_info['enabled_mods']) & 8 > 0:
                    mods += "HD"
                if int(score_info['enabled_mods']) & 16 > 0:
                    mods += "HR"
                if int(score_info['enabled_mods']) & 1024 > 0:
                    mods += "FL"
                if len(mods) > 0:
                    mods = " +" + mods

            # if score_info['enabled_mods'] is not None and int(score_info['enabled_mods']) & 2 > 0:
            #     if int(score_info['team']) == 1:
            #         blue_score += int(score_info['score'])
            #     if int(score_info['team']) == 2:
            #         red_score += int(score_info['score'])
            #     acc = '{:.2f}'.format(round((int(score_info['count50']) / 6 + int(score_info['count100']) / 3 + int(score_info['count300'])) * 100 / (int(score_info['countmiss']) + int(score_info['count50']) + int(score_info['count100']) + int(score_info['count300'])), 2))
            #     match_markdown += "[" + player_info['username'] + "](https://osu.ppy.sh/users/" + score_info['user_id'] + ")" + mods + " | " + "{:,}".format(int(score_info['score'])) + " (x2)" + " | " + acc + "% | " + "{:,}".format(int(score_info['maxcombo'])) + "x | " + score_info['countmiss'] + " |\n"
            #     continue
            
            acc = '{:.2f}'.format(round((int(score_info['count50']) / 6 + int(score_info['count100']) / 3 + int(score_info['count300'])) * 100 / (int(score_info['countmiss']) + int(score_info['count50']) + int(score_info['count100']) + int(score_info['count300'])), 2))
            match_markdown += "[" + player_info['username'] + "](https://osu.ppy.sh/users/" + score_info['user_id'] + ")" + mods + " | " + "{:,}".format(int(score_info['score'])) + " | " + acc + "% | " + "{:,}".format(int(score_info['maxcombo'])) + "x | " + score_info['countmiss'] + " |\n"

        if result[0] == 1:
            match_markdown += "\n**" + countries[0] + " " + "{:,}".format(red_score) + "** - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
            match_markdown += countries[0] + " wins by " + "{:,}".format(red_score - blue_score) + "\n"
            if score[0] == first_to:
                match_markdown += "\n**" + countries[0] + " (" + str(score[0]) + ")** - " + str(score[1]) + " " + countries[1] + "\n"
            else:
                match_markdown += "\n" + countries[0] + " (" + str(score[0]) + ") - " + str(score[1]) + " " + countries[1] + "\n"
        elif result[1] == 1:
            match_markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - **" + "{:,}".format(blue_score) + " " + countries[1] + "**\n\n"
            match_markdown += countries[1] + " wins by " + "{:,}".format(blue_score - red_score) + "\n"
            if score[1] == first_to:
                match_markdown += "\n" + countries[0] + " " + str(score[0]) + " - **(" + str(score[1]) + ") " + countries[1] + "**\n"
            else:
                match_markdown += "\n" + countries[0] + " " + str(score[0]) + " - (" + str(score[1]) + ") " + countries[1] + "\n"
        else:
            match_markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
            match_markdown += countries[0] + " and " + countries[1] + " tie\n"
            match_markdown += "\n" + countries[0] + " " + score[0] + " - " + score[1] + " " + countries[1] + "\n"
            continue
        
        file = open("C:\\Users\\Alex\\Downloads\\owc2025\\text\\" + countries[0] + " vs " + countries[1] + ".txt", mode='w', encoding='utf-8')
        file.write(match_markdown)
        file.close()
        print("Map " + str(counter+1) + " (" + str(score[0]) + "-" + str(score[1]) + ")")
        pick = 1 - pick
        counter += 1

winner = 0 if score[0] > score[1] else 1
loser = 1 - winner

if stage == "Grand Finals" and winner == 1:
    # Bracket Reset
    print()
    print("Bracket Reset")
    print()
    old_match_id = match_id
    match_id = input("Enter match ID:")

    match_name = get_match_info(match_id)['match']['name']
    old_countries = countries
    countries = [match_name.split('(')[1].split(')')[0], match_name.split('(')[2].split(')')[0]]

    print()
    print(countries[0] + " vs " + countries[1])
    print()

    pick = get_pick_order()
    old_red_bans, old_blue_bans = red_bans, blue_bans
    red_bans, blue_bans = get_bans()
    if pick == -1:
        pick = get_pick_order()
    
    print(title)
    print("match link: https://osu.ppy.sh/community/matches/" + match_id)
    print("red bans: " + ", ".join(red_bans))
    print("blue bans: " + ", ".join(blue_bans))
    print("first pick: " + ("red" if pick == 0 else "blue" if pick == 1 else "none"))
    print("win message: Congratulations to Team Winner for becoming the osu! World Cup 2025 Champions!")
    print("lose message: None")

    old_members = members
    members = {
        countries[0]: get_members(countries[0]),
        countries[1]: get_members(countries[1])
    }

    old_score = score
    score = [0,0]
    old_players = players
    players = {}
    counter = 0
    abort = 0
    old_match_markdown = match_markdown
    match_markdown = ""

    while(score[0] < first_to and score[1] < first_to):
        match_info = get_match_info(match_id)
        if score[0] < first_to - 1 and score[1] < first_to - 1 and 'games' in match_info and len(match_info['games']) <= counter + abort + 1:
            time.sleep(8)
        time.sleep(2)
        if 'games' in match_info and len(match_info['games']) > counter + abort + 1 and match_info['games'][counter + abort]['end_time'] == None:
            abort += 1
        if 'games' in match_info and len(match_info['games']) > counter + abort and match_info['games'][counter + abort]['end_time'] != None:
            game_info = match_info['games'][counter + abort]
            result, red_score, blue_score = read_game_info(game_info, players)
            score[0] += result[0]
            score[1] += result[1]
            team = result[1]
            
            match_markdown += "***\n###Map " + str(counter + 1)
            if counter == first_to * 2 - 2:
                match_markdown += " (Tiebreaker)"
            elif pick == 0 or pick == 1:
                match_markdown += " (picked by " + countries[pick] + ")"
            match_markdown += "\n***\n\n"
            
            map_info = mappool[game_info['beatmap_id']]

            match_markdown += "####" + map_info['id'] + " | [" + map_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + map_info['map id'] + ")\n\n"
            match_markdown += map_info['length'][1:] + " — " + map_info['bpm'] + " BPM — " + map_info['sr'] + " — " + "{:,}".format(int(map_info['combo'])) + "x\n\n"
            match_markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"
            match_markdown += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
            for score_info in game_info['scores']:
                if 2 - team != int(score_info['team']):
                    team = 1 - team
                    match_markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"
                player_info = players[score_info['user_id']]
                mods = ""
                if score_info['enabled_mods'] is not None and int(score_info['enabled_mods']) > 1:
                    mods += " +"
                    if int(score_info['enabled_mods']) & 2 > 0:
                        mods += "EZ"
                    if int(score_info['enabled_mods']) & 8 > 0:
                        mods += "HD"
                    if int(score_info['enabled_mods']) & 16 > 0:
                        mods += "HR"
                    if int(score_info['enabled_mods']) & 1024 > 0:
                        mods += "FL"
                acc = '{:.2f}'.format(round((int(score_info['count50']) / 6 + int(score_info['count100']) / 3 + int(score_info['count300'])) * 100 / (int(score_info['countmiss']) + int(score_info['count50']) + int(score_info['count100']) + int(score_info['count300'])), 2))
                match_markdown += "[" + player_info['username'] + "](https://osu.ppy.sh/users/" + score_info['user_id'] + ")" + mods + " | " + "{:,}".format(int(score_info['score'])) + " | " + acc + "% | " + "{:,}".format(int(score_info['maxcombo'])) + "x | " + score_info['countmiss'] + " |\n"
            
            if result[0] == 1:
                match_markdown += "\n**" + countries[0] + " " + "{:,}".format(red_score) + "** - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
                match_markdown += countries[0] + " wins by " + "{:,}".format(red_score - blue_score) + "\n"
                if score[0] == first_to:
                    match_markdown += "\n**" + countries[0] + " (" + str(score[0]) + ")** - " + str(score[1]) + " " + countries[1] + "\n"
                else:
                    match_markdown += "\n" + countries[0] + " (" + str(score[0]) + ") - " + str(score[1]) + " " + countries[1] + "\n"
            elif result[1] == 1:
                match_markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - **" + "{:,}".format(blue_score) + " " + countries[1] + "**\n\n"
                match_markdown += countries[1] + " wins by " + "{:,}".format(blue_score - red_score) + "\n"
                if score[1] == first_to:
                    match_markdown += "\n" + countries[0] + " " + str(score[0]) + " - **(" + str(score[1]) + ") " + countries[1] + "**\n"
                else:
                    match_markdown += "\n" + countries[0] + " " + str(score[0]) + " - (" + str(score[1]) + ") " + countries[1] + "\n"
            else:
                match_markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
                match_markdown += countries[0] + " and " + countries[1] + " tie\n"
                match_markdown += "\n" + countries[0] + " " + score[0] + " - " + score[1] + " " + countries[1] + "\n"
                continue
            
            file = open("C:\\Users\\Alex\\Downloads\\owc2025\\text\\" + countries[0] + " vs " + countries[1] + ".txt", mode='w', encoding='utf-8')
            file.write(match_markdown)
            file.close()
            print("Map " + str(counter+1) + " (" + str(score[0]) + "-" + str(score[1]) + ")")
            pick = 1 - pick
            counter += 1

    old_winner = winner
    winner = 0 if score[0] > score[1] else 1
    old_loser = loser
    loser = 1 - winner

    markdown = "## Match 1: **" + old_countries[old_winner] + " " + str(old_score[old_winner]) + "** - " + str(old_score[old_loser]) + " " + old_countries[old_loser] + "\n\n" if old_winner == 0 else "## Match 1: " + old_countries[old_loser] + " " + str(old_score[old_loser]) + " - **" + str(old_score[old_winner]) + " " + old_countries[old_winner] + "**\n\n"
    markdown += "## Match 2: **" + countries[winner] + " " + str(score[winner]) + "** - " + str(score[loser]) + " " + countries[loser] + "\n\n" if winner == 0 else "## Match 2: " + countries[loser] + " " + str(score[loser]) + " - **" + str(score[winner]) + " " + countries[winner] + "**\n\n"
    
    markdown += "#### Congratulations to Team " + countries[winner] + " for becoming the osu! World Cup 2025 Champions!\n\n"
    
    markdown += "***\n\n" + "[Lobby 1](https://osu.ppy.sh/community/matches/" + old_match_id + ") | [Lobby 2](https://osu.ppy.sh/community/matches/" + match_id + ") | [Bracket](https://challonge.com/OWC2025) | [A Stream](https://www.twitch.tv/osulive) | [B Stream](https://www.twitch.tv/osulive_2) | [Info Page](https://osu.ppy.sh/wiki/en/Tournaments/OWC/2025) | [Sheet](https://apps.leoflt.com/s/owc2025-info)\n\n"

    old_red_mc = sorted(match_costs(old_players, old_countries, old_members)[0].items(), key = lambda item: -item[1])
    old_blue_mc = sorted(match_costs(old_players, old_countries, old_members)[1].items(), key = lambda item: -item[1])
    old_red_seed = "#" + str(seed.index(old_countries[0]))
    old_blue_seed = "#" + str(seed.index(old_countries[1]))
    markdown += "***\n**Match 1 Match Costs (osuplus [?](https://i.imgur.com/BJPOKDY.png)):**\n\n| ***" + old_countries[0] + "*** |" + old_red_seed + "| ***" + old_countries[1] + "*** |" + old_blue_seed + "|\n|:-:|:-:|:-:|:-:|\n"
    for p in range(8):
        if p < len(old_red_mc):
            if old_red_mc[p][1] == -1:
                markdown += "| " + old_red_mc[p][0] + " | - |"
            else:
                markdown += "| " + old_red_mc[p][0] + " | " + '{:.3f}'.format(round(old_red_mc[p][1], 3)) + " |"
        else:
            markdown += "|||"
        if p < len(old_blue_mc):
            if old_blue_mc[p][1] == -1:
                markdown += " " + old_blue_mc[p][0] + " | - |\n"
            else:
                markdown += " " + old_blue_mc[p][0] + " | " + '{:.3f}'.format(round(old_blue_mc[p][1], 3)) + " |\n"
        else:
            markdown += "||\n"
    red_mc = sorted(match_costs(players, countries, members)[0].items(), key = lambda item: -item[1])
    blue_mc = sorted(match_costs(players, countries, members)[1].items(), key = lambda item: -item[1])
    red_seed = "#" + str(seed.index(countries[0]))
    blue_seed = "#" + str(seed.index(countries[1]))
    markdown += "***\n**Match 2 Match Costs (osuplus [?](https://i.imgur.com/BJPOKDY.png)):**\n\n| ***" + countries[0] + "*** |" + red_seed + "| ***" + countries[1] + "*** |" + blue_seed + "|\n|:-:|:-:|:-:|:-:|\n"
    for p in range(8):
        if p < len(red_mc):
            if red_mc[p][1] == -1:
                markdown += "| " + red_mc[p][0] + " | - |"
            else:
                markdown += "| " + red_mc[p][0] + " | " + '{:.3f}'.format(round(red_mc[p][1], 3)) + " |"
        else:
            markdown += "|||"
        if p < len(blue_mc):
            if blue_mc[p][1] == -1:
                markdown += " " + blue_mc[p][0] + " | - |\n"
            else:
                markdown += " " + blue_mc[p][0] + " | " + '{:.3f}'.format(round(blue_mc[p][1], 3)) + " |\n"
        else:
            markdown += "||\n"
    
    markdown += "***\n#Match 1\n"
    if len(old_red_bans) + len(old_blue_bans) > 0:
        markdown += "***\n" + "**Bans:**\n\n" + "*" + old_countries[0] + "*\n\n"
        for i in range(len(old_red_bans)):
            ban_info = mappool[old_red_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"
        markdown += "*" + old_countries[1] + "*\n\n"
        for i in range(len(old_blue_bans)):
            ban_info = mappool[old_blue_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"
        
    markdown = markdown + old_match_markdown

    markdown += "***\n#Match 2\n"
    if len(red_bans) + len(blue_bans) > 0:
        markdown += "***\n" + "**Bans:**\n\n" + "*" + countries[0] + "*\n\n"
        for i in range(len(red_bans)):
            ban_info = mappool[red_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"
        markdown += "*" + countries[1] + "*\n\n"
        for i in range(len(blue_bans)):
            ban_info = mappool[blue_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"
    
    markdown = markdown + match_markdown

    file = open("C:\\Users\\Alex\\Downloads\\owc2025\\text\\Grand Finals.txt", mode='w', encoding='utf-8')
    file.write(markdown)
    file.close()

    reddit_post(title, markdown)

    print("posted")
else:
    markdown = "## **" + countries[winner] + " " + str(score[winner]) + "** - " + str(score[loser]) + " " + countries[loser] + "\n\n" if winner == 0 else "## " + countries[loser] + " " + str(score[loser]) + " - **" + str(score[winner]) + " " + countries[winner] + "**\n\n"

    (win_message, lose_message) = get_next(countries[winner], countries[loser], True, score[winner] - score[loser])

    if win_message != "":
        markdown += win_message + "\n\n"
    if lose_message != "":
        markdown += lose_message + "\n\n"

    if "Group" in stage:
        markdown += "***\n\n" + "[Lobby](https://osu.ppy.sh/community/matches/" + match_id + ") | [A Stream](https://www.twitch.tv/osulive) | [B Stream](https://www.twitch.tv/osulive_2) | [Info Page](https://osu.ppy.sh/wiki/en/Tournaments/OWC/2025) | [Sheet](https://apps.leoflt.com/s/owc2025-info)\n\n"
    else:
        markdown += "***\n\n" + "[Lobby](https://osu.ppy.sh/community/matches/" + match_id + ") | [Bracket](https://challonge.com/OWC2025) | [A Stream](https://www.twitch.tv/osulive) | [B Stream](https://www.twitch.tv/osulive_2) | [Info Page](https://osu.ppy.sh/wiki/en/Tournaments/OWC/2025) | [Sheet](https://apps.leoflt.com/s/owc2025-info)\n\n"

    red_mc = sorted(match_costs(players, countries, members)[0].items(), key = lambda item: -item[1])
    blue_mc = sorted(match_costs(players, countries, members)[1].items(), key = lambda item: -item[1])
    red_seed = "#" + str(seed.index(countries[0])) if stage != "Showmatch" else ""
    blue_seed = "#" + str(seed.index(countries[1])) if stage != "Showmatch" else ""
    markdown += "***\n**Match Costs (osuplus [?](https://i.imgur.com/BJPOKDY.png)):**\n\n| ***" + countries[0] + "*** |" + red_seed + "| ***" + countries[1] + "*** |" + blue_seed + "|\n|:-:|:-:|:-:|:-:|\n"
    # markdown += "| [SadShiba](https://osu.ppy.sh/users/10747626) | - | [Lightin](https://osu.ppy.sh/users/7595619) | - |\n"
    for p in range(max(8,len(red_mc),len(blue_mc))):
        if p < len(red_mc):
            if red_mc[p][1] == -1:
                markdown += "| " + red_mc[p][0] + " | - |"
            else:
                markdown += "| " + red_mc[p][0] + " | " + '{:.3f}'.format(round(red_mc[p][1], 3)) + " |"
        else:
            markdown += "|||"
        if p < len(blue_mc):
            if blue_mc[p][1] == -1:
                markdown += " " + blue_mc[p][0] + " | - |\n"
            else:
                markdown += " " + blue_mc[p][0] + " | " + '{:.3f}'.format(round(blue_mc[p][1], 3)) + " |\n"
        else:
            markdown += "||\n"

    if len(red_bans) + len(blue_bans) > 0:
        markdown += "***\n" + "**Bans:**\n\n" + "*" + countries[0] + "*\n\n"
        for i in range(len(red_bans)):
            ban_info = mappool[red_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"
        markdown += "*" + countries[1] + "*\n\n"
        for i in range(len(blue_bans)):
            ban_info = mappool[blue_bans[i]]
            markdown += ban_info['id'] + " | [" + ban_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + ban_info['map id'] + ")\n\n"

    markdown = markdown + match_markdown

    file = open("C:\\Users\\Alex\\Downloads\\owc2025\\text\\" + countries[0] + " vs " + countries[1] + ".txt", mode='w', encoding='utf-8') # TODO: input file path to 
    file.write(markdown)
    file.close()

    reddit_post(title, markdown)

    print("posted")

    if stage == "Showmatch" and score[0] + score[1] < first_to * 2 - 1:
        old_counter = counter
        while(counter == old_counter):
            time.sleep(10)
            match_info = get_match_info(match_id)
            if 'games' in match_info and len(match_info['games']) > counter + abort + 1 and match_info['games'][counter + abort]['end_time'] == None:
                abort += 1
            if 'games' in match_info and len(match_info['games']) > counter + abort and match_info['games'][counter + abort]['end_time'] != None:
                game_info = match_info['games'][counter + abort]
                result, red_score, blue_score = read_game_info(game_info, players)
                team = result[1]
                
                markdown += "***\n###Map " + str(counter + 1)
                markdown += " (Tiebreaker Showcase)"
                markdown += "\n***\n\n"
                
                map_info = mappool[game_info['beatmap_id']]

                markdown += "####" + map_info['id'] + " | [" + map_info['artist - title [difficulty]'] + "](https://osu.ppy.sh/beatmaps/" + map_info['map id'] + ")\n\n"
                markdown += map_info['length'][1:] + " — " + map_info['bpm'] + " BPM — " + map_info['sr'] + " — " + "{:,}".format(int(map_info['combo'])) + "x\n\n"
                markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"
                markdown += "|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n"
                for score_info in game_info['scores']:
                    if 2 - team != int(score_info['team']):
                        team = 1 - team
                        markdown += "| ***" + countries[team] + "*** | **Score** | **Accuracy** | **Combo** | **Miss** |\n"
                    player_info = players[score_info['user_id']]
                    mods = ""
                    if score_info['enabled_mods'] is not None and int(score_info['enabled_mods']) > 1:
                        mods += " +"
                        if int(score_info['enabled_mods']) & 2 > 0:
                            mods += "EZ"
                        if int(score_info['enabled_mods']) & 8 > 0:
                            mods += "HD"
                        if int(score_info['enabled_mods']) & 16 > 0:
                            mods += "HR"
                        if int(score_info['enabled_mods']) & 1024 > 0:
                            mods += "FL"
                    acc = '{:.2f}'.format(round((int(score_info['count50']) / 6 + int(score_info['count100']) / 3 + int(score_info['count300'])) * 100 / (int(score_info['countmiss']) + int(score_info['count50']) + int(score_info['count100']) + int(score_info['count300'])), 2))
                    markdown += "[" + player_info['username'] + "](https://osu.ppy.sh/users/" + score_info['user_id'] + ")" + mods + " | " + "{:,}".format(int(score_info['score'])) + " | " + acc + "% | " + "{:,}".format(int(score_info['maxcombo'])) + "x | " + score_info['countmiss'] + " |\n"
                
                if result[0] == 1:
                    markdown += "\n**" + countries[0] + " " + "{:,}".format(red_score) + "** - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
                    markdown += countries[0] + " wins by " + "{:,}".format(red_score - blue_score) + "\n"
                elif result[1] == 1:
                    markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - **" + "{:,}".format(blue_score) + " " + countries[1] + "**\n\n"
                    markdown += countries[1] + " wins by " + "{:,}".format(blue_score - red_score) + "\n"
                else:
                    markdown += "\n" + countries[0] + " " + "{:,}".format(red_score) + " - " + "{:,}".format(blue_score) + " " + countries[1] + "\n\n"
                    markdown += countries[0] + " and " + countries[1] + " tie\n"
                
                file = open("C:\\Users\\Alex\\Downloads\\owc2025\\text\\" + countries[0] + " vs " + countries[1] + ".txt", mode='w', encoding='utf-8')
                file.write(markdown)
                file.close()
                print("Map " + str(counter+1))
                pick = 1 - pick
                counter += 1