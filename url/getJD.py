import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://i-list.jd.com/list.html?cat=9855,9858,9921'
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}       
proxy = {
    'https':'221.178.232.130:8080'
}

def get_data(url):
    cur_page = 1
    page_total = 2
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\jd_cate.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['名称','单位','包装单','品牌','型号','规格','销售价格','特价','主图','详情图','发货期','一级分类','二级分类','三级分类'])
        
    while cur_page <= 1: # total
        params = '&page='+ str(cur_page) +'&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main' 
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')
        tree_li = soup.find_all(class_ ='gl-item')
        total_str = soup.select('.filter .f-pager .fp-text i')
        if(len(total_str)>0):
            page_total = total_str[0].text
        print('第'+str(cur_page)+'页,共'+str(page_total)+'页')   
        cur_page = cur_page+1
        for i in range(0,1): # len(tree_li)
            item = tree_li[i]
            time.sleep(0.1)
            sku = item.select('.j-sku-item')[0]['data-sku']            
            detail_url = 'https://i-item.jd.com/'+sku+'.html'
            print(detail_url)
            detail_res = requests.get(detail_url,headers=headers)
            detail_soup = BeautifulSoup(detail_res.text,'html.parser')
            name = detail_soup.select('.sku-name')
            if(len(name)>0):
                name = name[0].text.strip()
                

    csv_file.close()


if __name__ == '__main__':
    get_data(url)
