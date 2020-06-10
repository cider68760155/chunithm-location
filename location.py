import csv
from bs4 import BeautifulSoup
import requests
import time
store_all = []
for pref in range(47):
    r = requests.get(
        "https://location.am-all.net/alm/location?gm=58&ct=1000&at="+str(pref))
    soup = BeautifulSoup(r.text, 'html.parser')
    name = [a.text for a in soup.find_all(class_='store_name')]
    address = [a.text for a in soup.find_all(class_='store_address')]
    assert len(name) == len(address), 'len(name)!=len(address)'
    store = [[name[i], address[i]] for i in range(len(name))]
    store.sort(key=lambda x: x[1])
    store_all.extend(store)
    time.sleep(0.5)

with open('location.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(store_all)
