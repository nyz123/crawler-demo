import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://www.mymro.cn/brandindex.html'
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

def get_data(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\gaj.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['ID','品牌名','数量'])
    
    ddList = soup.select('.brandUL dd')
    for i in range(786,len(ddList)): #len(ddList)
        href = ddList[i].select('h3 a')[0].attrs['href']
        href = href.replace('/b-','').replace('.html','')       
        
        print(i,'当前信息：',time.strftime('%H:%M:%S',time.localtime(time.time())))
        # 发送请求
        # 
        b_res = requests.get('https://www.mymro.cn/b-'+href+'.html',headers=headers)
        b_soup = BeautifulSoup(b_res.text,'html.parser',from_encoding='utf-8')
        all = b_soup.select('.brandULTit>div>a')
        if(len(all)==2):           
            page_res = requests.get('https://www.mymro.cn'+all[1].attrs['href'],headers=headers)
            page_soup = BeautifulSoup(page_res.text,'html.parser',from_encoding='utf-8')
            brand = page_soup.select('.f-param-item')
            b_name = ''
            num = 0
            if(len(brand)>0):
                brand_name = brand[0].text
                b_name = brand[0].attrs['data-value']
                num = brand_name.split('(')[1].split(')')[0]
            print(href,b_name,num)
            writer.writerow([href,b_name,num])
    
    csv_file.close()

if __name__ == '__main__':
    get_data(url)
