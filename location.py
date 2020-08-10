import csv
from bs4 import BeautifulSoup
import requests
import time
import sys

def main():
    store_prev=get_from_csv()
    store_now=crawl_store()
    print("crawl end",file=sys.stderr)
    store_now=correct_new(store_prev,store_now)
    write_to_csv(store_prev,'location_prev.csv')
    write_to_csv(store_now,'location.csv')

def crawl_store():
    ret = []
    for pref in range(47):
        r = requests.get(
            "https://location.am-all.net/alm/location?gm=58&ct=1000&at="+str(pref))
        soup = BeautifulSoup(r.text, 'html.parser')
        name = [a.text for a in soup.find_all(class_='store_name')]
        address = [a.text for a in soup.find_all(class_='store_address')]
        assert len(name) == len(address), 'len(name)!=len(address)'
        store = [[name[i], address[i]] for i in range(len(name))]
        store.sort(key=lambda x: x[1])
        ret.extend(store)
        time.sleep(0.5)
    return ret

def write_to_csv(store_all,filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(store_all)

def get_from_csv():
    with open('location.csv',encoding='utf-8') as f:
        reader=csv.reader(f)
        ret=[low for low in reader]
        return ret

def correct_new(store_prev,store_now):
    ret=[]
    idx_prev=0
    idx_now=0
    while(idx_now<len(store_now)):
        if idx_prev==len(store_prev)-1:
            idx_now+=1
        elif store_prev[idx_prev]==store_now[idx_now]:
            ret.append(store_now[idx_now])
            idx_prev+=1
            idx_now+=1
        else:
            if store_prev[idx_prev][0]<store_now[idx_now][0]:
                idx_prev+=1
            elif store_prev[idx_prev][0]>store_now[idx_now][0]:
                ret.append(store_now[idx_now])
                idx_now+=1
            else:
                if store_now[idx_now][1].find(store_prev[idx_prev][1])==-1:
                    while True:
                        print('0:'+store_prev[idx_prev][1])
                        print('1:'+store_now[idx_now][1])
                        selector=input()
                        if selector=='0':
                            ret.append(store_prev[idx_prev])
                            idx_prev+=1
                            idx_now+=1
                            break
                        elif selector=='1':
                            ret.append(store_now[idx_now])
                            idx_prev+=1
                            idx_now+=1
                            break
                else:
                    ret.append(store_prev[idx_prev])
                    idx_prev+=1
                    idx_now+=1
    return ret

if __name__=='__main__':
    main()