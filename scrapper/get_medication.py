from bs4 import BeautifulSoup
import pandas as pd
import csv
import cloudscraper

data = pd.read_csv("dataset.csv")
diseases = []
[diseases.append(x) for x in data['Disease'] if x not in diseases]
#print(diseases)
diseases.remove("GERD")
medicine = {}
scraper = cloudscraper.create_scraper()
for name in diseases:
    page = scraper.get("https://www.webmd.com/drugs/2/search?type=conditions&query="+name)
    soup = BeautifulSoup(page.content,'html.parser')
    result = soup.find('p',class_="results")
    if result == None:
        continue
    else:
        result = str(result).split('>')[1].split('<')[0]
        if 'medications' in result.split():
            medicine[name] = (str(soup.find("tbody").find_next('tr').find_next('td').find_next('a')).split('>')[1].split('<')[0])

        else:
            next_page = str(soup.find('ul', class_="drug-list").find_next('li').find_next('a')).split("href=")[1].split(">")[0]
            scraper_2 = cloudscraper.create_scraper()
            page_2 = scraper_2.get("https://www.webmd.com" + next_page.strip("\""))
            soup_2 = BeautifulSoup(page_2.content, 'html.parser')
            medicine[name] = (str(soup_2.find("tbody").find_next('tr').find_next('td').find_next('a')).split('>')[1].split('<')[0])

print(medicine)
fieldnames = ['Disease','Medication']
with open('medicine2.csv','w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['DISEASE','Medication'])
    for key, value in medicine.items():
        writer.writerow([key,value])

