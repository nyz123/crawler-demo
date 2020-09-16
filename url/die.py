import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://www.tdcj.texas.gov/death_row/dr_executed_offenders.html'
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\data\\'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

def get_data(url):
    csv_file = open(file_path+'die.csv','w',encoding='utf-8')

    writer = csv.writer(csv_file)
    writer.writerow(['名称','国家','日期','最后一句话'])
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    print(soup.title)    
    lis = soup.find_all(name='tr')
    for i in range(1,len(lis)):
        first_name = lis[i].select('td')[4].text
        last_name = lis[i].select('td')[3].text
        date = lis[i].select('td')[7].text
        country = lis[i].select('td')[8].text
        last_statement_url = 'https://www.tdcj.texas.gov/death_row/' + lis[i].select('td')[2].a.attrs['href']
        statement_res = requests.get(last_statement_url)
        statement_soup = BeautifulSoup(statement_res.text,'html.parser',from_encoding='utf-8')
        statement = ""
        ps = statement_soup.select('#content_right p:last-child')
        if(len(ps)>0):
            statement = ps[0].text
        name = first_name+' '+last_name
        print(name,statement)
        writer.writerow([name,country,date,statement])
    csv_file.close()
if __name__ == '__main__':
    get_data(url)
