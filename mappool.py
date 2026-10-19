import requests
import csv

def get_beatmap_info(beatmap_id):
    url = f"https://osu.ppy.sh/api/get_beatmaps?k=YOUR_API_KEY&b={beatmap_id}"
    # TODO: Replace 'YOUR_API_KEY' with your actual osu! API key
    response = requests.get(url)
    return response.json()

file_name = "ro" + input("Round of?")
if file_name == "rogs":
    file_name = "gs"

with_combo = []
fieldnames = ['id', 'artist - title [difficulty]', 'sr', 'bpm', 'length', 'cs', 'ar', 'od', 'mapper', 'map id', 'combo']
file = open("" + file_name + ".csv", mode='r') # TODO: input file path for the mappools/ folder
csv_reader = csv.DictReader(file)
for row in csv_reader:
    if row['map id'] != '':
        row['combo'] = get_beatmap_info(row['map id'])[0]['max_combo']
        row['artist - title [difficulty]'] = row['artist - title [difficulty]'].replace("[", "&#91;").replace("]", "&#93;")
        with_combo.append(row)
file.close()

file = open("" + file_name + ".csv", mode='w', newline='') # TODO: input file path for the mappools/ folder
csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
csv_writer.writeheader()
for row in with_combo:
    csv_writer.writerow(row)
file.close()

