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

def download_img(img_url, filepath):
    if not img_url:
        return
    request = urllib.request.Request(img_url)
    try:
        response = urllib.request.urlopen(request)
        if (response.getcode() == 200):
            with open(filepath, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filepath
    except:
        return "failed" 

def get_data(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\gaj.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['ID','品牌','名称','订货号','制造商型号','预计出货日','销售价','包装数量','其他'])
    
    ddList = soup.select('.brandUL dd')
    print('ddList:',len(ddList))
    for i in range(1148,len(ddList)): #len(ddList)
        href = ddList[i].select('h3 a')[0].attrs['href']
        href = href.replace('/b-','').replace('.html','')       
        url1 = 'https://www.mymro.cn/b-'+href+'.html'
        print(i,'当前信息：',time.strftime('%H:%M:%S',time.localtime(time.time())))
        print(url1)
        # 发送请求
        b_res = requests.get(url1,headers=headers)
        b_soup = BeautifulSoup(b_res.text,'html.parser',from_encoding='utf-8')
        all = b_soup.select('.brandULTit>div>a')
        if(len(all)==2): 
            cur_page = 1            
            total_page = 1
            while cur_page<=total_page:
                url2 = 'https://www.mymro.cn' + all[1].attrs['href'] + '&page='+str(cur_page) 
                print(url2) 
                page_res = requests.get(url2,headers=headers)
                page_soup = BeautifulSoup(page_res.text,'html.parser',from_encoding='utf-8')
                brand = page_soup.select('.f-param-item')
                brand_name=''
                if(len(brand)>0):
                    brand_name = brand[0].text.strip()
            
                total = page_soup.select('.p-category .main-box .m-page-box .m-page-list .m-item-label')
                if(len(total)>=1):
                    total_page = int(total[0].text.replace('共','').replace('页',''))
                p_list = page_soup.select('.m-result-table .m-item')
                print('p_list:',len(p_list))
                if(len(p_list)>0):
                  for j in range(0,len(p_list)): #len(p_list)
                    product = p_list[j]
                    name_list = product.select('.m-item-name a')
                    id = name_list[0].attrs['href'].replace('g-','').replace('.html','')
                    name = name_list[0].text
                    # 图片
                    img = product.select('.m-item-img-box img')
                    if(len(img)>0):
                        p_img_path = file_path+id+'.jpg'
                        if not Path(p_img_path).exists():
                            img_url = img[0]['src']
                            if(img_url != 'https://static.mymro.cn/product_images_new/350/hp_np.png'):
                                download_img(img_url,p_img_path) 
                    print(name) 
                    
                    table_list = product.select('.m-table')
                    for ii in range(0,len(table_list)): #len(table_list)
                        table = table_list[ii]
                        tr = table.select('.m-tr')
                        tr2 = table.select('.m-tr2')

                        if(len(tr)>0 and len(tr2)==len(tr)):
                            other = tr2[0].select('.m-td2')
                            other_title = []
                            for dd2 in range(0,len(other)):
                                other_title.append(other[dd2].text.strip())
                            print(other_title)
                            for jj in range(1,len(tr)):
                                td = tr[jj].select('.m-td .text-single')
                                td2 = tr2[jj].select('.m-td2')
                                
                                dhh =''
                                zzsxh =''
                                yjchr =''
                                xsh=''
                                bzsl=''
                                qita=''
                                if(len(td)==4):
                                    dhh = td[0].text
                                    zzsxh = td[1].text
                                    yjchr = td[2].text
                                    xsh = td[3].select('span')[0].text
                                if(len(td2)>0):
                                    for o_i in range(0,len(other_title)):
                                        if(other_title[o_i]=='包装数量'):
                                            bzsl = td2[o_i].text.strip()
                                        else:
                                            qita += other_title[o_i]+':'+td2[o_i].text.strip()+';'

    
                                print(id,name,dhh,zzsxh,yjchr,xsh,bzsl)
                                writer.writerow([id,brand_name,name,dhh,zzsxh,yjchr,xsh,bzsl,qita])
                 
                cur_page += 1
                
           
    
    csv_file.close()

if __name__ == '__main__':
    get_data(url)
