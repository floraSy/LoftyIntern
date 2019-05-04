import sys 
import time
import random
import json
import urllib2
import pandas as pd 
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")


#Some User Agents
hds=[{'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},\
    {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},\
    {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},\
    {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'},\
    {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'},\
    {'User-Agent':'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11'},\
    {'User-Agent':'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11'}]

csv_file = pd.DataFrame(columns=["Sold_date","Price","Street","City","State","Beds","Baths","Sq.Ft.","Href"])
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

for p in state_list:
    for zip_code in range(p[0],p[1]+1):
        new_zip = str(zip_code)
        while len(new_zip)< 5:
            new_zip = "0"+new_zip
        print(new_zip)
        page_url = "https://www.redfin.com/zipcode/"+new_zip+"/filter/include=sold-3mo"

        try:
            response = urllib2.Request(page_url,headers=hds[random.randint(0,len(hds)-1)])
            source_code = urllib2.urlopen(response).read()
            plain_text = source_code.decode("utf-8")
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print(e)
            continue
        

        soup = BeautifulSoup(plain_text,features='html.parser')
        next_page = soup.findAll('a',{'class':"clickable goToPage"})
        page_file = getInfo(soup,csv_file)

        for i in next_page:
            link = i.get('href')
            url = "https://www.redfin.com" + link
            time.sleep(20+random.randint(0,10))

            try:
                new_response = urllib2.Request(url,headers=hds[random.randint(0,len(hds)-1)])
                new_code = urllib2.urlopen(new_response).read()
                new_plain_text = new_code.decode("utf-8")
            except (urllib2.HTTPError, urllib2.URLError) as e:
                print(e)
                continue
            
            new_soup = BeautifulSoup(new_plain_text,features='html.parser')
            page_file = getInfo(new_soup,page_file)
        
        time.sleep(20+random.randint(0,5))
    time.sleep(60)

print(page_file.head(n=100))
page_file.to_csv("/home/LoftyCode/InternResults/result.csv",index=False)