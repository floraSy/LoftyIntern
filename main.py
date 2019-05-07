import sys 
import time
import random
import json
import urllib
import os
import pandas as pd 
import requests
import telnetlib
from bs4 import BeautifulSoup



os.getcwd()

start = time.time()

#Some User Agents
my_headers = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

#print("Build IP pool")
proxies = ["116.211.143.11:80",\
    "183.1.86.235:8118",\
    "183.32.88.244:808",\
    "121.40.42.35:9999",\
    "222.94.148.210:808",\
    "218.86.128.100:8118",\
    "121.31.154.12:8123",\
    "121.122.42.35:39249",
    '183.95.80.102:8080',
    '123.160.31.71:8080',
    '115.231.128.79:8080',
    '166.111.77.32:80',
    '43.240.138.31:8080',
    '218.201.98.196:3128',
    "144.217.86.131:3128",
    '197.254.4.130:43656']

for i in proxies:
    info = i.split(":")
    try:
        telnetlib.open(info[0],info[1],timeout=5)
    except:
        proxies.remove(i)
print(proxies)
    

page_file = pd.DataFrame(columns=["Sold_date","Price","Street","City","State","Beds","Baths","Sq.Ft.","Href"])
get_info = []
state_list = [[35801,35816],[99501,99524],[85001,85055],[72201,72217],[94203,94209],\
    [90001,90089],[90209,90213],[80201,80239],[6101,6112],[19901,19905],[20001,20020],\
    [32501,32509],[33124,33190],[32801,32837],[30301,30381],[96801,96830],[83254,83254],\
    [60601,60641],[62701,62709],[46201,46209],[52801,52809],[50301,50323],[67201,67221],\
    [41701,41702],[70112,70119],[4032,4034],[21201,21237],[2101,2137],[49036,49036],\
    [49734,49735],[55801,55808],[39530,39535],[63101,63141],[59044,59044],[68901,68902],\
    [89501,89513],[3217,3217],[7039,7039],[87500,87506],[10001,10048],[27565,27565],\
    [58282,58282],[44101,44179],[74101,74110],[97201,97225],[15201,15244],[2840,2841],\
    [29020,29020],[57401,57402],[37201,37222],[78701,78705],[84321,84323],[5751,5751],\
    [24517,24517],[98004,98009],[25813,25813],[53201,53228],[82941,82941]]


def getInfo(soup,csv_file):
    result_list = soup.findAll('div',{'class':'HomeCardContainer'})
    for i in result_list:
        #script = json.loads(i.find('script',{'type': 'application/ld+json'}).get_text())["@type"]
        date = i.find('span',{'class':"HomeSash font-weight-bold roundedCorners"}).text
        price = i.find('span',{'class':"homecardV2Price"}).text
        date = date.strip("SOLD")
        address = i.find('div',{'class':"addressDisplay font-size-smaller"}).text
        
        address = address.split(",")
        if len(address) == 1:
            city = " "
            state = ""
        elif len(address) == 2:
            city = ""
            state1 = address[1].split(" ")
            state = state1[1]
        elif len(address) == 3:
            city = address[1]
            state1 = address[2].split(" ")
            state = state1[1]
        
        stats = i.findAll('div',{'class':"stats"})
        bed = stats[0].text
        bed_number = bed.split(" ")
        bath = stats[1].text
        bath_number = bath.split(" ")
        sq = stats[2].text
        sq_number = sq.split(" ")
        detail_url = i.find("a",{"class":"cover-all"}).get("href")
        new_row = pd.DataFrame([[date,price,address[0],city,state,bed_number[0],bath_number[0],sq_number[0],detail_url]],\
            columns=["Sold_date","Price","Street","City","State","Beds","Baths","Sq.Ft.","Href"])
        csv_file = csv_file.append(new_row,ignore_index = True)
    return csv_file


print("Web scraper start!")
num = 0
for p in state_list:
    for zip_code in range(p[0],p[1]+1):
        new_zip = str(zip_code)
        while len(new_zip)< 5:
            new_zip = "0"+new_zip
        print("current zipcode:"+new_zip)
        page_url = "https://www.redfin.com/zipcode/"+new_zip+"/filter/include=sold-3mo"
        num = num + 1

        if num%10==0:
            print(page_file.head(n=100))
        if num==200:
            num = 0
            time.sleep(600+random.randint(0,600))

        try:
            p = random.choice(proxies)
            proxy = {"http":p}
            hd = random.choice(my_headers)
            my_header = {'User-Agent':hd}
            response = requests.get(page_url,headers=my_header,proxies=proxy)
            #source_code = urllib.request.urlopen(response).read()
            #plain_text = source_code.decode("utf-8")
            response.encoding = 'utf-8'
            plain_text = response.text
            response.raise_for_status()
        except (requests.exceptions.HTTPError) as e:
            print(e)
            end = time.time()
            print(str((end-start)/3600)+" hours, "+p+" got IP blocked")
            proxies.remove(p)
            if len(proxies) == 0:
                print("All IPs got blocked!")
                break
            else:
                continue
        

        soup = BeautifulSoup(plain_text,features='html.parser')
        next_page = soup.findAll('a',{'class':"clickable goToPage"})
        page_file = getInfo(soup,page_file)
        print(page_file)

        for i in next_page:
            link = i.get('href')
            url = "https://www.redfin.com" + link
            time.sleep(60+random.randint(0,120))

            try:
                p = random.choice(proxies)
                proxy = {"http":"http://"+p}
                hd = random.choice(my_headers)
                my_header = {'User-Agent':hd}
                new_response = requests.get(url,headers=my_header,proxies=proxy)
                #new_code = urllib.request.urlopen(new_response).read()
                #new_plain_text = new_code.decode("utf-8")
                response.encoding = 'utf-8'
                new_plain_text = response.text
                new_response.raise_for_status()
            except (requests.exceptions.HTTPError) as e:
                print(e)
                end = time.time()
                print(str((end-start)/3600)+" hours, "+p+" got IP blocked")
                proxies.remove(p)
                if len(proxies) == 0:
                    print("All IPs got blocked!")
                    break
                else:
                    continue
            
            new_soup = BeautifulSoup(new_plain_text,features='html.parser')
            page_file = getInfo(new_soup,page_file)
            print(page_file)
        
    if len(proxies) == 0:
        break

        
        
        time.sleep(30+random.randint(0,60))
    time.sleep(180+random.randint(0,180))

print(page_file.head(n=100))
page_file.to_csv("result.csv",index=False)