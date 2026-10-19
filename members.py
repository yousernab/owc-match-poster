import requests
import pickle

def store_members():
    members = {}
    with open("", mode='r') as f: # TODO: input file location of the "members.md" file
        for line in f:
            if "|  | **" in line:
                country = line[line.find("| **") + len("| **"):line.find("** |")]
                members[country] = []
                line = line[line.find("["):line.rfind(")") + 1]
                team = line.split(', ')
                for member in team:
                    members[country].append(member[member.rfind("/") + 1:member.rfind(")")])
    with open("", mode='wb') as f: # TODO: input file location of the "members.pkl" file
        pickle.dump(members, f)

    

def get_user_info(username):
    url = f"https://osu.ppy.sh/api/get_user?k=YOUR_API_KEY&u={username}"
    # TODO: Replace 'YOUR_API_KEY' with your actual osu! API key
    response = requests.get(url)
    return response.json()

def get_members(country):
    with open("", mode='rb') as f: # TODO: input file location of the "members.pkl" file
        members = pickle.load(f)
        # if country == "SS. Honey":
        #     members["SS. Honey"] = ["5182050","11375105","1473890","15293080","4734703","6090175","10743390","13767572"]
        # if country == "kanagattandyrylmagandyktarynyzdan":
        #     members["kanagattandyrylmagandyktarynyzdan"] = ["16817965","11552867","2291265","9405745","2546001","12353810","8964050","23179637"]
        if country == 'Türkiye':
            country = 'TÃ¼rkiye'
        if country not in members:
            return []
        return ["[" + get_user_info(member)[0]['username'].replace("[", "&#91;").replace("]", "&#93;") + "](https://osu.ppy.sh/users/" + member + ")" for member in members[country]]
