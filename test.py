import requests
import html
import csv
import pickle
# url = f"https://osu.ppy.sh/api/get_match?k=YOUR_API_KEY&mp=116072105"

# response = requests.get(url)

# match_info = response.json()
# print(match_info['games'][3])

# print("A[[".replace("[", "&#91;").replace("]", "&#93;"))

with open('groups.pkl', 'rb') as f:
    print(pickle.load(f))