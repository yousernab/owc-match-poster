import pickle

# ro32 start
# curr_bracket = {
#     "": (1, "r"),
#     "": (1, "b"),
#     "": (2, "r"),
#     "": (2, "b"),
#     "": (3, "r"),
#     "": (3, "b"),
#     "": (4, "r"),
#     "": (4, "b"),
#     "": (5, "r"),
#     "": (5, "b"),
#     "": (6, "r"),
#     "": (6, "b"),
#     "": (7, "r"),
#     "": (7, "b"),
#     "": (8, "r"),
#     "": (8, "b"),
#     "": (9, "r"),
#     "": (9, "b"),
#     "": (10, "r"),
#     "": (10, "b"),
#     "": (11, "r"),
#     "": (11, "b"),
#     "": (12, "r"),
#     "": (12, "b"),
#     "": (13, "r"),
#     "": (13, "b"),
#     "": (14, "r"),
#     "": (14, "b"),
#     "": (15, "r"),
#     "": (15, "b"),
#     "": (16, "r"),
#     "": (16, "b")
# }

# ro16 start
"""
curr_bracket = {
    "Poland": (45, "r"),
    "Philippines": (33, "r"),
    "Russian Federation": (26, "r"),
    "China": (26, "b"),
    "Canada": (27, "r"),
    "Norway": (27, "b"),
    "Germany": (28, "r"),
    "Brazil": (28, "b"),
    "United States": (29, "r"),
    "France": (29, "b"),
    "United Kingdom": (30, "r"),
    "New Zealand": (30, "b"),
    "Australia": (48, "r"),
    "Romania": (39, "r"),
    "South Korea": (32, "r"),
    "Chile": (32, "b"),
    "Austria": (17, "r"),
    "Singapore": (17, "b"),
    "Netherlands": (18, "r"),
    "Taiwan": (18, "b"),
    "Sweden": (19, "r"),
    "Malaysia": (19, "b"),
    "Thailand": (20, "r"),
    "Japan": (20, "b"),
    "Finland": (21, "r"),
    "Peru": (21, "b"),
    "Italy": (22, "r"),
    "Türkiye": (22, "b"),
    "Spain": (23, "r"),
    "Argentina": (23, "b"),
    "Indonesia": (24, "r")
    "Kazakhstan": (24, "b"),
}

with open('curr_bracket.pkl', 'wb') as f:
    pickle.dump(curr_bracket, f)
"""

# group stage:

seed = [
    None,
    "Poland",
    "United States",
    "Australia",
    "Canada",
    "Germany",
    "South Korea",
    "United Kingdom",
    "Russian Federation",
    "China",
    "Chile",
    "Brazil",
    "Romania",
    "Norway",
    "Philippines",
    "France",
    "New Zealand",
    "Austria",
    "Indonesia",
    "Sweden",
    "Spain",
    "Thailand",
    "Finland",
    "Italy",
    "Netherlands",
    "Türkiye",
    "Taiwan",
    "Kazakhstan",
    "Japan",
    "Ukraine",
    "Argentina",
    "Singapore",
    "Vietnam",
    "Malaysia",
    "Uruguay",
    "Greece",
    "Portugal",
    "Denmark",
    "Belgium",
    "Peru",
    "Hong Kong"
]

group_stage = False
"""
group_a = {
    # "Country": {"seed": , "wins": 0, "losses": 0, "pd": 0}
    "China": {"seed": 9, "wins": 0, "losses": 0, "pd": 0},
    "Norway": {"seed": 13, "wins": 0, "losses": 0, "pd": 0},
    "Austria": {"seed": 17, "wins": 0, "losses": 0, "pd": 0},
    "Thailand": {"seed": 21, "wins": 0, "losses": 0, "pd": 0}
    
}
group_b = {
    "Romania": {"seed": 12, "wins": 0, "losses": 0, "pd": 0},
    "New Zealand": {"seed": 16, "wins": 0, "losses": 0, "pd": 0},
    "Indonesia": {"seed": 18, "wins": 0, "losses": 0, "pd": 0},
    "Finland": {"seed": 22, "wins": 0, "losses": 0, "pd": 0}
}
group_c = {
    "Chile": {"seed": 10, "wins": 0, "losses": 0, "pd": 0},
    "France": {"seed": 15, "wins": 0, "losses": 0, "pd": 0},
    "Spain": {"seed": 20, "wins": 0, "losses": 0, "pd": 0},
    "Italy": {"seed": 23, "wins": 0, "losses": 0, "pd": 0}
}
group_d = {
    
    "Brazil": {"seed": 11, "wins": 0, "losses": 0, "pd": 0},
    "Philippines": {"seed": 14, "wins": 0, "losses": 0, "pd": 0},
    "Sweden": {"seed": 19, "wins": 0, "losses": 0, "pd": 0},
    "Netherlands": {"seed": 24, "wins": 0, "losses": 0, "pd": 0}
}
group_e = {
    "Taiwan": {"seed": 26, "wins": 0, "losses": 0, "pd": 0},
    "Vietnam": {"seed": 32, "wins": 0, "losses": 0, "pd": 0},
    "Malaysia": {"seed": 33, "wins": 0, "losses": 0, "pd": 0},
    "Denmark": {"seed": 37, "wins": 0, "losses": 0, "pd": 0}
}
group_f = {
    "Türkiye": {"seed": 25, "wins": 0, "losses": 0, "pd": 0},
    "Argentina": {"seed": 30, "wins": 0, "losses": 0, "pd": 0},
    "Uruguay": {"seed": 34, "wins": 0, "losses": 0, "pd": 0},
    "Belgium": {"seed": 38, "wins": 0, "losses": 0, "pd": 0}
}
group_g = {
    "Kazakhstan": {"seed": 27, "wins": 0, "losses": 0, "pd": 0},
    "Ukraine": {"seed": 29, "wins": 0, "losses": 0, "pd": 0},
    "Portugal": {"seed": 36, "wins": 0, "losses": 0, "pd": 0},
    "Peru": {"seed": 39, "wins": 0, "losses": 0, "pd": 0}
}
group_h = {
    "Japan": {"seed": 28, "wins": 0, "losses": 0, "pd": 0},
    "Singapore": {"seed": 31, "wins": 0, "losses": 0, "pd": 0},
    "Greece": {"seed": 35, "wins": 0, "losses": 0, "pd": 0},
    "Hong Kong": {"seed": 40, "wins": 0, "losses": 0, "pd": 0}
}

groups = {
    "A": group_a,
    "B": group_b,
    "C": group_c,
    "D": group_d,
    "E": group_e,
    "F": group_f,
    "G": group_g,
    "H": group_h
}

with open('groups.pkl', 'wb') as f:
    pickle.dump(groups, f)
"""
# seed = [
#     None,
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     "",
#     ""
# ]

curr_bracket = None

winner_next = [
    None,
    (25, "r"),
    (25, "b"),
    (26, "r"),
    (26, "b"),
    (27, "r"),
    (27, "b"),
    (28, "r"),
    (28, "b"),
    (29, "r"),
    (29, "b"),
    (30, "r"),
    (30, "b"),
    (31, "r"),
    (31, "b"),
    (32, "r"),
    (32, "b"),
    (40, "b"),
    (39, "b"),
    (38, "b"),
    (37, "b"),
    (36, "b"),
    (35, "b"),
    (34, "b"),
    (33, "b"),
    (45, "r"),
    (45, "b"),
    (46, "r"),
    (46, "b"),
    (47, "r"),
    (47, "b"),
    (48, "r"),
    (48, "b"),
    (41, "b"),
    (41, "r"),
    (42, "b"),
    (42, "r"),
    (43, "b"),
    (43, "r"),
    (44, "b"),
    (44, "r"),
    (51, "b"),
    (52, "b"),
    (49, "b"),
    (50, "b"),
    (55, "r"),
    (55, "b"),
    (56, "r"),
    (56, "b"),
    (53, "b"),
    (53, "r"),
    (54, "b"),
    (54, "r"),
    (58, "b"),
    (57, "b"),
    (60, "r"),
    (60, "b"),
    (59, "b"),
    (59, "r"),
    (61, "b"),
    (62, "r"),
    (62, "b")
]

loser_next = [
    None,
    (17, "r"),
    (17, "b"),
    (18, "r"),
    (18, "b"),
    (19, "r"),
    (19, "b"),
    (20, "r"),
    (20, "b"),
    (21, "r"),
    (21, "b"),
    (22, "r"),
    (22, "b"),
    (23, "r"),
    (23, "b"),
    (24, "r"),
    (24, "b"),
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    (33, "r"),
    (34, "r"),
    (35, "r"),
    (36, "r"),
    (37, "r"),
    (38, "r"),
    (39, "r"),
    (40, "r"),
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    None,
    (49, "r"),
    (50, "r"),
    (51, "r"),
    (52, "r"),
    None,
    None,
    None,
    None,
    None,
    None,
    (57, "r"),
    (58, "r"),
    None,
    None,
    None,
    (61, "r"),
    None
]

curr_round = [None]
curr_round += 16 * ["Round of 32"]
curr_round += 8 * ["Losers Round 1"]
curr_round += 8 * ["Round of 16"]
curr_round += 8 * ["Losers Round 2"]
curr_round += 4 * ["Losers Round 3"]
curr_round += 4 * ["Quarterfinals"]
curr_round += 4 * ["Losers Round 4"]
curr_round += 2 * ["Losers Round 5"]
curr_round += 2 * ["Semifinals"]
curr_round += 2 * ["Losers Round 6"]
curr_round += ["Losers Round 7"]
curr_round += ["Winners Finals"]
curr_round += ["Losers Finals"]
curr_round += ["Grand Finals"]

curr_mappool = {
    "Group Stage": "gs",
    "Group A": "gs",
    "Group B": "gs",
    "Group C": "gs",
    "Group D": "gs",
    "Group E": "gs",
    "Group F": "gs",
    "Group G": "gs",
    "Group H": "gs",
    "Round of 32": "ro32",
    "Round of 16": "ro16",
    "Losers Round 1": "ro16",
    "Quarterfinals": "ro8",
    "Losers Round 2": "ro8",
    "Losers Round 3": "ro8",
    "Semifinals": "ro4",
    "Losers Round 4": "ro4",
    "Losers Round 5": "ro4",
    "Finals": "ro2",
    "Winners Finals": "ro2",
    "Losers Round 6": "ro2",
    "Losers Round 7": "ro2",
    "Grand Finals": "ro1",
    "Losers Finals": "ro1"
}

curr_first_to = {
    "Group Stage": 5,
    "Group A": 5,
    "Group B": 5,
    "Group C": 5,
    "Group D": 5,
    "Group E": 5,
    "Group F": 5,
    "Group G": 5,
    "Group H": 5,
    "Round of 32": 5,
    "Round of 16": 5,
    "Losers Round 1": 5,
    "Quarterfinals": 6,
    "Losers Round 2": 6,
    "Losers Round 3": 6,
    "Semifinals": 6,
    "Losers Round 4": 6,
    "Losers Round 5": 6,
    "Finals": 7,
    "Winners Finals": 7,
    "Losers Round 6": 7,
    "Losers Round 7": 7,
    "Grand Finals": 7,
    "Losers Finals": 7
}

winner_next_round = {
    "Round of 32": "the Round of 16.",
    "Round of 16": "the Quarterfinals.",
    "Quarterfinals": "the Semifinals.",
    "Semifinals": "the Winners Finals.",
    "Winners Finals": "the Grand Finals.",
    "Losers Round 1": "Losers Round 2.",
    "Losers Round 2": "Losers Round 3.",
    "Losers Round 3": "Losers Round 4.",
    "Losers Round 4": "Losers Round 5.",
    "Losers Round 5": "Losers Round 6.",
    "Losers Round 6": "Losers Round 7.",
    "Losers Round 7": "the Losers Finals.",
    "Losers Finals": "the Grand Finals."
}

loser_next_round = {
    "Round of 32": "Losers Round 1.",
    "Round of 16": "Losers Round 2.",
    "Quarterfinals": "Losers Round 4.",
    "Semifinals": "Losers Round 6.",
    "Winners Finals": "the Losers Finals."
}

loser_placement = {
    "Losers Round 1": " has been eliminated in 25th-32nd place.",
    "Losers Round 2": " has been eliminated in 17th-24th place.",
    "Losers Round 3": " has been eliminated in 13th-16th place.",
    "Losers Round 4": " has been eliminated in 9th-12th place.",
    "Losers Round 5": " has been eliminated in 7th-8th place.",
    "Losers Round 6": " has been eliminated in 5th-6th place.",
    "Losers Round 7": " has been eliminated in 4th place.",
    "Losers Finals": " has been eliminated in 3rd place."
}

def get_match(winner, loser):
    if winner not in curr_bracket and loser not in curr_bracket:
        return -1
    winner = curr_bracket[winner]
    loser = curr_bracket[loser]
    if winner[0] == loser[0]:
        return winner[0]
    print("mismatch")

def get_opp(curr):
    if curr[1] == "r":
        return (curr[0], "b")
    return (curr[0], "r")

def get_team(curr):
    if curr in curr_bracket.values():
        return ("", [list(curr_bracket.keys())[list(curr_bracket.values()).index(curr)]])
    
    prev = None
    if curr in winner_next:
        prev = winner_next.index(curr)
        return ("the winner of ", [get_team((prev, "r"))[1], get_team((prev, "b"))[1]])
    prev = loser_next.index(curr)
    return ("the loser of ", [get_team((prev, "r"))[1], get_team((prev, "b"))[1]])

def get_string_sub(next):
    if len(next) == 1:
        return next[0]
    return get_string_sub(next[0]) + "/" + get_string_sub(next[1])

def get_string(next):
    if len(next) == 1:
        return next[0]
    return get_string_sub(next[0]) + " vs " + get_string_sub(next[1])

def get_next(winner, loser, persist, pd):
    if group_stage == True:
        with open('groups.pkl', 'rb') as f:
            global groups
            groups = pickle.load(f)
        group = get_group(winner, loser)
        if group == -1:
            print("group not found")
            return
        groups[group][winner]["wins"] += 1
        groups[group][winner]["pd"] += pd
        groups[group][loser]["losses"] += 1
        groups[group][loser]["pd"] -= pd
        if persist:
            with open('groups.pkl', 'wb') as f:
                pickle.dump(groups, f)
        if group == "A" or group == "B" or group == "C" or group == "D":
            return (get_group_standings(group), "^(Top 2 advance to Winners Round of 16)  \n^(Bottom 2 advance to Losers Round of 16)")
        elif group == "E" or group == "F" or group == "G" or group == "H":
            return (get_group_standings(group), "^(Top 2 advance to Losers Round of 16)  \n^(Bottom 2 are eliminated)")
        else:
            print("invalid group")
    
    
    with open('curr_bracket.pkl', 'rb') as f:
        global curr_bracket
        curr_bracket = pickle.load(f)
    
    match_num = get_match(winner, loser)

    if match_num == -1:
        return ("", "")
    
    if match_num == 62:
        return("#### Congratulations to Team " + winner + " for becoming the osu! World Cup 2025 Champions!", "")
    
    curr_bracket[winner] = winner_next[match_num]
    curr_bracket[loser] = loser_next[match_num]
    if persist:
        with open('curr_bracket.pkl', 'wb') as f:
            pickle.dump(curr_bracket, f)

    win_next = get_team(get_opp(winner_next[match_num]))
    win_next_string = win_next[0] + get_string(win_next[1])

    if loser_next[match_num] is None:
        return (winner + " will face " + win_next_string + " in " + winner_next_round[curr_round[match_num]], loser + loser_placement[curr_round[match_num]])
    
    lose_next = get_team(get_opp(loser_next[match_num]))
    lose_next_string = lose_next[0] + get_string(lose_next[1])
    
    return (winner + " will face " +  win_next_string + " in " + winner_next_round[curr_round[match_num]], loser + " will face " + lose_next_string+ " in " + loser_next_round[curr_round[match_num]])

def get_info(red_team, blue_team):
    if group_stage == True:
        with open('groups.pkl', 'rb') as f:
            global groups
            groups = pickle.load(f)
        group = get_group(red_team, blue_team)
        if group == -1:
            print("group not found")
            return
        return ("Group " + group, "", "")
    
    with open('curr_bracket.pkl', 'rb') as f:
        global curr_bracket
        curr_bracket = pickle.load(f)
    if red_team not in curr_bracket and blue_team not in curr_bracket:
        return ("Showmatch", "None", "None")
    red_team = curr_bracket[red_team]
    blue_team = curr_bracket[blue_team]
    if red_team[0] != blue_team[0]:
        print("mismatch")
        return
    if red_team[1] != "r":
        print("not red")
    if blue_team[1] != "b":
        print("not blue")
    
    match_num = red_team[0]

    if match_num == 62:
        return (curr_round[match_num], "Congratulations to Team Winner for becoming the osu! World Cup 2025 Champions!", "None")

    win_next = get_team(get_opp(winner_next[match_num]))
    win_next_string = win_next[0] + get_string(win_next[1])

    if loser_next[match_num] is None:
        return (curr_round[match_num], "Winner will face " + win_next_string + " in " + winner_next_round[curr_round[match_num]], "Loser" + loser_placement[curr_round[match_num]])
    
    lose_next = get_team(get_opp(loser_next[match_num]))
    lose_next_string = lose_next[0] + get_string(lose_next[1])
    
    return (curr_round[match_num], "Winner will face " +  win_next_string + " in " + winner_next_round[curr_round[match_num]], "Loser will face " + lose_next_string + " in " + loser_next_round[curr_round[match_num]])

def get_group(red_team, blue_team):
    for group in groups:
        if red_team in groups[group] and blue_team in groups[group]:
            return group
    return -1

def get_group_standings(group):
    standings = sorted(groups[group].items(), key = lambda item: (-item[1]["wins"], -item[1]["pd"], item[1]["seed"]))
    markdown = "**Group " + group + " Standings:**\n\n| **Team** | **W** | **L** | **PD** |\n|:-:|:-:|:-:|:-:|\n"
    for c in range(4):
        if c < len(standings):
            markdown += "| ***" + standings[c][0] + "*** (#" + str(standings[c][1]["seed"]) + ") | " + str(standings[c][1]["wins"]) + " | " + str(standings[c][1]["losses"]) + " | " + ('{:+d}'.format(standings[c][1]["pd"]) if standings[c][1]["pd"] != 0 else "0") + " |\n"
    return markdown

def set_seeds():
    seeds = [None]
    team = input()
    while team != '':
        seeds.append(team)
        team = input()
    with open('seeds.pkl', 'wb') as f:
        pickle.dump(seeds, f)
    print(seeds)
    return

def get_seeds():
    with open('seeds.pkl', 'rb') as f:
        global seed
        seed = pickle.load(f)
    return


# print(get_info("Poland", "Ukraine"))
# print(get_next("Ukraine", "Poland", False))
# curr_bracket = {}

# with open('curr_bracket.pkl', 'rb') as f:
#     curr_bracket = pickle.load(f)
#     curr_bracket["France"] = (43, "r")
#     curr_bracket["New Zealand"] = (43, "b")

# with open('curr_bracket.pkl', 'wb') as f:
#     pickle.dump(curr_bracket, f)

# print(curr_bracket)

# print(get_info("Japan", "Singapore"))
# print(get_next("Japan", "Singapore", False, 3))

# print(get_info("Türkiye", "Italy"))