import requests
import json
from bs4 import BeautifulSoup


def getinf(url):
    all_images = []
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html5lib")
    infa = soup.find("div", {"class": "fotorama"})
    if infa is None:
        all_images = ["No Images"]
        return all_images
    else:
        images = infa.findAll("img")
        for i in images:
            x = i.get("src")
            all_images.append(x)
        return all_images

url = "https://map.cian.ru/ajax/map/roundabout/?currency=2&deal_type=rent&engine_version=2&maxprice=50000&offer_type=flat&region=1&room1=1&type=4"

link_template = 'https://cian.ru/rent/flat/'

# { 'room_num': "", 'metro': [список с ближайшими станциями метро], 'pics': [список с фото квартиры],
#  cost: "цена квартиры", floor: "этаж", phone: "телефон хозяина", furn: True/False, loc: [координаты],
#  long: True/False, agent: True/False}

all_infa = []
html = requests.get(url).text
json_text = json.loads(html)
infa = json_text["data"]["points"]
for i in infa:
    main = infa[i]
    offers = main["offers"]
    for j in offers:
        room_num = j['property_type']
        price = j['price_rur']
        floor = j["link_text"][3]
        floor = floor[floor.find(" ") + 1:]
        flat_id = j["id"]
    url = link_template + flat_id
    print(url)
    all_pics = getinf(url)
    x = {'room_num': room_num, 'metro': [], 'pics': all_pics,
     "cost": price, "floor": floor, "phone": "телефон", "furn": None, "loc": i,
     "long": None, "agent": None, "link": url}
    all_infa.append(x)
print(all_infa)

