# OWC Match Poster

I removed some file paths and my osu! and reddit api keys, so those need to be replaced for this code to be useable. I marked them with TODO's

A general outline of how I used the code every OWC

I might have missed some things since I'm writing this based on my memory

At the start of each OWC:
- Change any mentions of year to the current year (they're all 2025 right now)
- Update relevant links to the current years OWC (search for "[Bracket]", "[Info Page]", "[Sheet]" in the "get_mp.py" file)
- Copy the participants table from "https://osu.ppy.sh/wiki/en/Tournaments/OWC" into "members.md" and run "members.py" to store them into "members.pkl" (this is so the match post can list team members that weren't present in a match)
- After qualifiers, input the seeding into "seed" in "bracket.py"
- After qualifiers, manually input the group info into "bracket.py" in "group_a" through "group_h" and run that part of the code uncommented to store the groups in groups.pkl, then recomment it.
- During group stage, set group_stage = True in "bracket.py"
- After group stage, set group_stage = False
- After group stage, set the "curr_bracket" in "bracket.py" based on the match numbering in the challonge bracket with the top team being "r" and bottom team being "b". Run that part uncommented to store the bracket in bracket.pkl, then recomment it.


At the start of each week:
- Copy the map pool from the owc spreadsheet into a csv titled "ro_.csv" (round of _) depending on which round it is, or "gs.csv" if it's group stage, then run "mappool.py" to store the mappool


Each match:
- run "get_mp.py" and follow the instructions in console (input mp id, pick order, bans)
