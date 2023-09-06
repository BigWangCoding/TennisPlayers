import requests
from bs4 import BeautifulSoup

source = requests.get("https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players").text

soup = BeautifulSoup(source, "html5lib")

table = soup.find("table")

data = [["Name", "website", "age"]]

table = table.find_all("tr")

for i in table[1:3]:
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

    temp.append(website)

    data.append(temp)

    player_website = requests.get(website).text
    soup = BeautifulSoup(player_website, "html5lib")

    print(soup.prettify())
print(data)


    
    
