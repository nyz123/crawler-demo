import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time
import json

# urls = [
#     'https://web.zkh360.com/view/brand/brandList.html?brand_id=208325',
#     # 'https://web.zkh360.com/view/brand/brandList.html?brand_id=200356',
#     # 'https://web.zkh360.com/view/brand/brandList.html?brand_id=215037',
#     # 'https://web.zkh360.com/view/brand/brandList.html?brand_id=198317',
# ]

url ='https://web.zkh360.com/api/search/listProductInfo'
brandIds = [
    # '208325','200356',
    '204442','198682','198455','197778'
]
brandName = {
    '208325':'KITO','200356':'ORGAPACK','215037':'XINGO 新光','198317':'WERNER 稳耐',
    '204442':'DL 得力',
    '198682':'XG 信高',
    '198455':'UNI-T 优利德',
    '197778':'FLUKE 福禄克',
}
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Content-Type':'application/json',
    'Cookie': 'citycode=%7B%22provinceName%22%3A%22%E4%B8%8A%E6%B5%B7%E5%B8%82%22%2C%22cityName%22%3A%22%E4%B8%8A%E6%B5%B7%E5%B8%82%22%2C%22provinceCode%22%3A310000%2C%22cityCode%22%3A310100%7D; CART_SESSION=947534422; hadskfhjayuasdhjk=%4067d0897870-jnjkghyg-990767!hjkh()%2F.kdj; gr_user_id=d0f2e7c0-8dd3-420b-b2c7-1550b6765d67; 8ccf9443d38f1ead_gr_session_id_2c693c82-f694-4e03-b0db-90e34f7ca9f7=false; 8ccf9443d38f1ead_gr_session_id=2c693c82-f694-4e03-b0db-90e34f7ca9f7'
}
data = {
    "from":0,
    "size":20,
    "keyword":None,
    "fz":False,
    "catalogueId":None,
    "productFilter":{
        "brandIds":[],
        "properties":{}
    },
    "cityCode":310100,
    "extraFilter":{
        "showIndustryFeatured":False,
        "inStock":False
    },
    "searchType":{
        "notNeedCorrect":False
    }
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


def get_data(url):
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\zkh_brand.csv','w',encoding='utf-8')
    img_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'

    writer = csv.writer(csv_file)
    writer.writerow(['商品名称', '价格', '未税价格', '单位','税率', '品牌', '商品型号', '订货编码','包装规格','起订量','最小包装量','产品介绍'])

    for brandId in brandIds:        
        # 分页
        page_total = 1
        cur_page = 0
        # 目录1是否存在
        brand_file = img_path+brandName[brandId]
        if not Path(brand_file).exists():
            os.mkdir(brand_file)
        while cur_page < page_total:
            data['from'] = cur_page
            cur_page = cur_page+1
            # brandID
            data['productFilter']['brandIds'] = [brandId]
            res = requests.post(url,headers=headers,json=data,verify=False)
            res_json = json.loads(res.text)
            res_content = res_json['page']['content']
            if(page_total == 1):
                page_total = res_json['page']['totalPages']
            for i in range(len(res_content)): #len(res_content)
                pro = res_content[i]
                detail_url = 'https://www.zkh360.com/item/'+pro['proSkuNo']+'.html?proSkuNo='+pro['proSkuNo']+'&proSkuId='+str(pro['proSkuId'])+'&level4CatalogueId='+str(pro['level4CatalogueId'])
                print('brandId:'+brandId,'分页：'+str(cur_page),detail_url)
                detail_res = requests.get(detail_url,headers=headers,verify=False)
                soup = BeautifulSoup(detail_res.text,'html.parser',from_encoding='utf-8')
                pro_name_div = soup.select('.zkh-pdt-name')
                if len(pro_name_div)>=1:
                    pro_name = pro_name_div[0].text
                pro_material_div = soup.select('.zkh-material-panel .zkh-prop-item .zkh-prop-info')
                if len(pro_material_div)>=6:
                    pro_brand = pro_material_div[0].text
                    pro_spxh = pro_material_div[1].text
                    pro_dhbm = pro_material_div[2].text
                    pro_bzgg = pro_material_div[3].text
                    pro_qdl = pro_material_div[4].text
                    pro_zxbzl = pro_material_div[5].text
                
                pro_price_li = soup.select('.zkh-price-l>li')
                if len(pro_price_li)>=2:
                    pro_price1_div = pro_price_li[0].select('.textRed')[0]
                    pro_price1_1 = pro_price1_div.select('b')
                    if(len(pro_price1_1)>0):
                        pro_price1 = pro_price1_div.select('b')[0].text
                        pro_unit = pro_price1_div.text.split(pro_price1)[1].strip()[1:]
                    else:
                        pro_price1 = pro_price1_div.text
                    
                    pro_price2_2 = pro_price_li[1].select('.zkh-prop-info')
                    pro_price2 = ""
                    pro_tax = ''
                    if(len(pro_price2_2)>0):
                        pro_price2_str = pro_price_li[1].select('.zkh-prop-info')[0].text.replace('￥','').replace('（','').replace('：','').replace('）','').strip().split('税率')
                        pro_price2 = pro_price2_str[0]
                        pro_tax = pro_price2_str[1]           
            

                # 产品介绍/注意事项
                pro_detail_div = soup.select('.product-introduce-desc-wrap .content-wrap .product-props-row')
                pro_cpjs = ''
                if(len(pro_detail_div) > 0):                
                    for item in pro_detail_div:
                        pro_cpjs = pro_cpjs+item.text

                # 主图图片
                pro_main_imgs = soup.select('.gallery-wrap .gallery-slick-wrap .gallery-slick-box .gallery-slick-dots li img')
                if(len(pro_main_imgs)>0):
                    for index in range(len(pro_main_imgs)): 
                        img = pro_main_imgs[index]
                        p_img_path = brand_file + '\\'+pro_dhbm+'_main_'+str(index+1)+'.jpg'
                        if not Path(p_img_path).exists():
                            download_img(img['src'],p_img_path)   

                # 详情图片
                pro_detail_imgs = soup.select('.product-introduce-desc-wrap .content-wrap .product-props-row img')
                if(len(pro_detail_imgs)>0):
                    for index in range(len(pro_detail_imgs)): 
                        img = pro_detail_imgs[index]
                        p_img_path = brand_file + '\\'+pro_dhbm+'_detail_'+str(index+1)+'.jpg'
                        if not Path(p_img_path).exists():
                            download_img(img['src'],p_img_path)   
                        

                #  writer.writerow(['商品名称', '价格', '未税价格', '单位','税率', '品牌', '商品型号', '订货编码','包装规格','起订量','最小包装量','产品介绍'])      
                writer.writerow([pro_name,pro_price1,pro_price2,pro_unit,pro_tax,pro_brand,pro_spxh,pro_dhbm,pro_bzgg,pro_qdl,pro_zxbzl,pro_cpjs])
        
    csv_file.close()

if __name__ == '__main__':    
    get_data(url)
