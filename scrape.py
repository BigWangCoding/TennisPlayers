import requests
from bs4 import BeautifulSoup
import pandas as pd

GRANDSLAMS = ["Australian Open", "French Open", "Wimbledon Championships", "US Open"]
CURRENT_YEAR = 2023
YEARS = 45

TOTAL_YEARS = CURRENT_YEAR - YEARS

source = requests.get("https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players").text

soup = BeautifulSoup(source, "html5lib")

table = soup.find("table")

data = []

table = table.find_all("tr")

for i in table[1:]:
    try:
        birth_year = int(list(i)[3].text)
    except:
        continue

    if birth_year < TOTAL_YEARS:
        continue

    temp = []
    try:
        if list(i)[5].text.isnumeric():
            continue
        name_of_player = list(i)[1].span["data-sort-value"]
    except TypeError:
        continue
    temp.append(name_of_player)

    id = i.td.span.span.span.a["href"]
    website = f"https://en.wikipedia.org{id}"

    player_website = requests.get(website).text
    soup = BeautifulSoup(player_website, "html5lib")
    
    
    player_info = soup.find("table", class_="infobox vcard")

    player_table = player_info.find_all("tr")
    totalWins = 0
    continueCount = 0

    for info in player_table:
        if continueCount > 0:
            continueCount -= 1
            continue

        th_tag = info.th
        
        td_tag = info.td
        if not th_tag:
            continue
        
        if th_tag.text == "Born":
            age = td_tag.find("span", class_= "noprint ForceAgeToShow").text
            age = age.strip(" ")[1:-1][4:]
            
            temp.append(age)

        if th_tag.text == "Grand Slam doubles results":
            continueCount = 4
            continue
        try:
            name = (td_tag.a["title"]).split(" ")
            name = f"{name[1]} {name[2]}"
            
            if name in GRANDSLAMS:
                       
                try:
                    if td_tag.b.text == "W":
                        find = td_tag.find_all("a")
                        wins = len(list(find))
                        totalWins += wins

                except:
                    pass
        except:
            pass
        

    
    temp.append(totalWins)

    #temp.append(website)

    data.append(temp)
                

data.sort(key=lambda x:x[2], reverse=True)
for i in data:
    print(i)

df = pd.DataFrame(data)

df.to_csv("Tennis_Players_Stats.csv", index=False, header=["Name", "age", "Grand Slam Wins"])

