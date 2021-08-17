import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://www.jisilu.cn/data/cbnew/#cb'
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'}

def get_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    print(soup.title)
    product_cate = soup.select('.crumbs>a')

if __name__ == '__main__':
    get_data(url)
