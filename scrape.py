import requests
from bs4 import BeautifulSoup

source = requests.get("https://en.wikipedia.org/wiki/List_of_male_singles_tennis_players").text

soup = BeautifulSoup(source, "lxml")

table = soup.find("table")

data = [["Name", "website", "age"]]

table = table.find_all("tr")

for i in table[1:5]:

    if list(i)[5].text.isnumeric():
        continue

    name_of_player = list(i)[1].span["data-sort-value"]

    print(name_of_player)



    