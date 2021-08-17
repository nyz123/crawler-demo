import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time
import json
# import urllib3

# urllib3.disable_warnings()

brandIds=[
    # "35430",
    # "6214",
    # "232",
    # "217",
    # '232','527',
    '79'
]
brandName = {
    '35430':'KITO','6214':'ORGAPACK','232':'XINGO 新光','217':'WERNER 稳耐',
    '232':'信高',
    '527':'优利德',
    '79':'福禄克',
}
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Content-Type':'application/json',
}

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


def get_data(brandIds):
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\xy_brand.csv','w',encoding='utf-8')
    img_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'

    writer = csv.writer(csv_file)
    writer.writerow(['商品名称', '价格', '未税价格', '单位','税率', '品牌', '品牌型号', '西域订货号','预计出货日','最小订货量','产品介绍'])      
    for brandId in brandIds:        
        # 分页
        page_total = 19
        cur_page = 19
        # 目录1是否存在
        brand_file = img_path+brandName[brandId]
        if not Path(brand_file).exists():
            os.mkdir(brand_file)

        while cur_page <= page_total:
            print(brandId)
            res = requests.get('https://www.ehsy.com/brand-'+brandId,headers=headers,verify=False)
            soup = BeautifulSoup(res.text,'html.parser')
            product_list = soup.select('.layout-product-list .product-list .product')
            p_total = soup.select('.page-count .fullPage')
            if(page_total == 19 and len(p_total)>0):
                page_total = int(p_total[0].text)
            for i in range(len(product_list)): #len(product_list)
                pro = product_list[i]
                detail_url = 'https://www.ehsy.com/product-'+pro['data-text']+'?p='+str(cur_page)
                print('brandId:'+brandId,'分页：'+str(cur_page),detail_url)
                time.sleep(0.1)
                d_res = requests.get(detail_url,headers=headers,verify=False)
                d_soup = BeautifulSoup(d_res.text,'html.parser')
                pro_detail_div = d_soup.select('.product-info-detail')
                if(len(pro_detail_div)>0):
                    pro_name = pro_detail_div[0].select('h1')[0].text
                    pro_price1 = pro_detail_div[0].select('.line-price .show-price')[0].text.replace('¥','').replace(' ','')
                    pro_price_origin = pro_detail_div[0].select('.line-price .orgin')
                    if(len(pro_price_origin)==2):
                        pro_unit = pro_price_origin[0].text.replace('/','').replace(' ','')
                        pro_price2_arr = pro_price_origin[1].text.replace('¥','').replace(' ','').replace('(','').replace(')','').split('税率：')
                        pro_price2 = pro_price2_arr[0]
                        pro_tax = pro_price2_arr[1]
                    pro_detail_o = pro_detail_div[0].select('.product-info-detail-other .attr-title')
                    if(len(pro_detail_o) >= 4):
                        pro_xydhh = pro_detail_o[0].select('span')[2].text
                        pro_ppxh = pro_detail_o[1].select('span')[2].text
                        pro_yjchr = pro_detail_o[2].select('span')[2].text
                        pro_zxdhl = pro_detail_o[3].select('span')[2].text
                
                # 商品介绍
                pro_cpjs_div = d_soup.select('.tabContent.product-info-css .tec-content')
                
                
                # 主图图片
                pro_main_imgs = d_soup.select('ul.clearfix.pic-small-list.sliderbox img')
                print(len(pro_main_imgs))
                if(len(pro_main_imgs)>0):
                    for index in range(len(pro_main_imgs)): 
                        img = pro_main_imgs[index]
                        p_img_path = brand_file + '\\'+pro_xydhh+'_main_'+str(index+1)+'.jpg'
                        if not Path(p_img_path).exists():
                            download_img(img['src'],p_img_path)   

                # 详情图片
                pro_detail_imgs = d_soup.select('.tabContent.product-info-css .tec-content>div')
                if(len(pro_detail_imgs)>0):
                    for i in range(len(pro_detail_imgs)): 
                        img_div = pro_detail_imgs[i]
                        title = ''
                        title_div = img_div.select('.tec-tittle .cnName')
                        if(len(title_div)>0):
                            title = title_div[0].text

                        imgs = img_div.select('.tec-description img')
                        if(len(imgs)>0):
                            for index in range(len(imgs)):                                
                                p_img_path = brand_file + '\\'+pro_xydhh+'_detail_'+(title if title else str(i+1))+'_'+str(index+1)+'.jpg'
                                if not Path(p_img_path).exists():
                                    download_img(imgs[index]['src'],p_img_path)   
                #  writer.writerow(['商品名称', '价格', '未税价格', '单位','税率', '品牌', '品牌型号', '西域订货号','预计出货日','最小订货量','产品介绍'])  
                pro_cpjs = ''
                if(len(pro_cpjs_div)>0):
                    pro_cpjs = pro_cpjs_div[0].text
                writer.writerow([pro_name,pro_price1,pro_price2,pro_unit,pro_tax,brandName[brandId],pro_ppxh,pro_xydhh,pro_yjchr,pro_zxdhl,pro_cpjs])
             

                
            cur_page = cur_page+1
    csv_file.close()

if __name__ == '__main__':    
    get_data(brandIds)
