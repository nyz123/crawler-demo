# -*- coding:utf-8 -*- 
import json
import csv
import requests
import urllib.request
import os
import random

def generate_random_str(randomlength=4):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

def get_data():   

    cate_url = 'https://www.zkh360.com/servezkhApi/catalog/listIndexCatalogs?tranceId=602230911597140007244'
    pro_url = 'https://web.zkh360.com/api/search/listProductInfo'

    csv_file = open('F:\\xdl\\github\\crawler-demo\\zkh\\data\\zkh_cate.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['品名','一级目录','二级目录','三级目录','四级目录', '品牌', '价格', '单位', '商品型号', '订货编码','规格参数'])

    cate_res =  requests.get(cate_url)
    cate_json = json.loads(cate_res.text)
    # 遍历1级分类
    for i in range(0,len(cate_json)): # cate_json
        firstCatalog = cate_json[i]['firstCatalog']
        print('----------------------------------')

        childrenCatalog = cate_json[i]['childrenCatalog']

        for j in range(0,len(childrenCatalog)): # len(childrenCatalog)
            catalogName = childrenCatalog[j]['catalogName']
            clickImagePath = childrenCatalog[j]['clickImagePath']
            # path1 = 'F:\\xdl\\github\\crawler-demo\\zkh\\cates\\'+catalogName + '_clickImage.png'
            # download_img(clickImagePath,path1)
            crmId = childrenCatalog[j]['crmId']
            # img_dir = 'F:\\xdl\\github\\crawler-demo\\zkh\\'+catalogName 
            # os.mkdir(img_dir)

            page = 0
            total = 0
            while page <= total: # total
                page += 1
                req = {
                    'from': page,
                    'size': 20,
                    'keyword': None,
                    'fz': False,
                    'catalogueId': crmId,
                    'productFilter': { 'brandIds': [], 'properties': {} },
                    'cityCode': 310100,
                    'extraFilter': { 'showIndustryFeatured': False, 'inStock': False },
                    'searchType': { 'notNeedCorrect': False },
                    'clp': True,
                }
                pro_res = requests.post(pro_url,headers={'Content-Type':'application/json;charset=UTF-8'},json=req,verify=False)
                
                if pro_res:
                    pro_json = json.loads(pro_res.text)
                    if pro_json and pro_json['page'] and pro_json['page']['content'] and pro_json['page']['totalPages']:
                        pro_content = pro_json['page']['content']
                        if page == 1:
                            total = min(pro_json['page']['totalPages'],49)
                        for pro in pro_content:
                            # 品名 目录 品牌 价格 单位 商品型号 订货编码
                            proSkuProductName = pro['proSkuProductName'] 
                            print(i,catalogName,j,total,page,proSkuProductName)
                            proBrandName = pro['proBrandName']
                            catalogs = pro['catalogs']['catalogs']
                            price = pro['price']
                            unitOfMeasureCode = pro['unitOfMeasureCode']
                            proMaterialNo = pro['proMaterialNo']
                            proSkuNo = pro['proSkuNo']
                            specificationList = pro['specificationList'] # 属性
                            proImgPath_Z1 = pro['proImgPath_Z1']
                            # for ii in range(len(proImgPath_Z1)):
                                # img_path = img_dir + '\\'+ proSkuNo + '_' + generate_random_str() + '.jpg'
                                # download_img(proImgPath_Z1[ii],img_path)
                            specs = ''
                            for s in range(len(specificationList)):
                                specs += specificationList[s]['proSpecName']+':'+specificationList[s]['specificationValue']
                                if s!=len(specificationList)-1:
                                    specs += ' '
                            writer.writerow([proSkuProductName,catalogs[0]['catalogName'],catalogs[1]['catalogName'],catalogs[2]['catalogName'],catalogs[3]['catalogName'],proBrandName,price,unitOfMeasureCode,proMaterialNo,proSkuNo,specs])


    csv_file.close()

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

if __name__ == '__main__':
    get_data()
    
