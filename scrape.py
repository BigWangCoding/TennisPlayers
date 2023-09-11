"""
This code searches the Tennis Wiki page and find 
all male tennis player under a certain age and gets their
name, age and grand slam wins
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

GRANDSLAMS = ["Australian Open", "French Open", "Wimbledon Championships", "US Open"]
CURRENT_YEAR = 2023
YEARS = 45

# Calculate the age that they were born in
TOTAL_YEARS = CURRENT_YEAR - YEARS

# Gets the html file for this wiki page
source = requests.get("https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players").text
soup = BeautifulSoup(source, "html5lib")

# Finding the table containing all the male tennis players
table = soup.find("table")
table = table.find_all("tr")

# This list will be exported as csv file
data = []

# Iterate through the list of living male tennis players
for i in table[1:]:

    # Checking if the current player is alive or not
    try:
        birth_year = int(list(i)[3].text)
    except:
        continue
    # Checking if the person is at most n years old
    if birth_year <= TOTAL_YEARS:
        continue
    
    # This list will be appended into data
    temp = []

    # These gets the player's name
    try:
        if list(i)[5].text.isnumeric():
            continue
        name_of_player = i.find("a").text
                
    except TypeError:
        continue
    temp.append(name_of_player)

    # This gets the players wiki page where we can obtain their age and wins
    try:
        id = i.td.span.span.span.a["href"]
        website = f"https://en.wikipedia.org{id}"
    except:
        continue
    player_website = requests.get(website).text
    soup = BeautifulSoup(player_website, "html5lib")
    
    # Finds the table containing the players stats
    player_info = soup.find("table", class_="infobox vcard")

    # their stats are all under the "tr" block
    player_table = player_info.find_all("tr")

    # Record the player's total grand slam wins
    # also tells loop to continue if encountered
    # doubles grand slam
    totalWins = 0
    continueCount = 0

    # the info for each player has a "th" tag and a "td" tag
    # each containing different wanted information
    for info in player_table:
        if continueCount > 0:
            continueCount -= 1
            continue
        # The "th" tag gets the title of the stat
        # The "td" tag gets the actual code of the tag
        th_tag = info.th
        td_tag = info.td

        if not th_tag:
            continue
        

        # This gets the age
        if th_tag.text == "Born":
            age = td_tag.find("span", class_= "noprint ForceAgeToShow").text
            age = age.strip(" ")[1:-1][4:]
            
            temp.append(age)
        # Making sure we don't get doubles results
        # Could possibly add the doubles results in the future
        if th_tag.text == "Grand Slam doubles results":
            continueCount = 4
            continue

        # Calculating the grand slam wins
        try:
            # Gets the name of the title
            name = (td_tag.a["title"]).split(" ")
            name = f"{name[1]} {name[2]}"
            
            if name in GRANDSLAMS:
                       
                try:
                    # if the b tag is equal to W that means they have 
                    # won this specific grand slam before
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
                
# Sorted in order where the person with the highest 
# grand slam wins is on top
data.sort(key=lambda x:x[2], reverse=True)

# Export the information using pandas dataframe
df = pd.DataFrame(data)

# Adding a header to the dataframe
df.to_csv("PlayerStats2023.csv", index=False, header=["Name", "age", "Grand Slam Wins"])    
