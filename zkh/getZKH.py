# -*- coding:utf-8 -*- 
import json
import csv
import requests
import urllib.request
import os
import random
import time

requests.adapters.DEFAULT_RETRIES =5
s = requests.session() 
s.keep_alive = False

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

    # path1 = 'F:\\xdl\\github\\crawler-demo\\zkh\\cates\\'+catalogName + '_clickImage.png'
    # os.mkdir(img_dir)
    csv_file = open('F:\\xdl\\github\\crawler-demo\\zkh\\data\\zkh_cate.csv','w',encoding='utf-8')
    csv_over1000_file = open('F:\\xdl\\github\\crawler-demo\\zkh\\data\\zkh_cate_over1000.csv','w',encoding='utf-8')

    writer = csv.writer(csv_file)
    writer.writerow(['品名','一级目录','二级目录','三级目录','四级目录', '品牌', '价格', '单位', '商品型号', '订货编码','发货期','规格参数'])

    writer_over1000 = csv.writer(csv_over1000_file)
    writer_over1000.writerow(['crmId','三级目录','总页数'])

    cate_res =  requests.get(cate_url)
    cate_json = json.loads(cate_res.text)
    # 遍历 1 级分类
    for i in range(8,len(cate_json)): # len(cate_json)
        firstCatalog = cate_json[i]['firstCatalog']
        childrenCatalog = cate_json[i]['childrenCatalog']

        # 遍历 2 级分类
        for j in range(8,len(childrenCatalog)): # len(childrenCatalog)           
            for k in range(3,len(childrenCatalog[j]['children'])): #len(childrenCatalog[j].children)
                child_cate = childrenCatalog[j]['children'][k]
                catalogName = child_cate['catalogName']
                crmId = child_cate['crmId']
                
                page = 0
                total = 0
                while page <= total: # total
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
                    page += 1

                    # !!!!!!!发送请求!!!!!!
                    time.sleep(0.1)
                    pro_res = requests.post(pro_url,headers={'Content-Type':'application/json;charset=UTF-8','Connection':'close'},json=req,verify=False)
                    
                    if pro_res:
                        pro_json = json.loads(pro_res.text)
                        if pro_json and pro_json['page'] and pro_json['page']['content'] and pro_json['page']['totalPages']:
                            pro_content = pro_json['page']['content']
                            if page == 1:
                                total = min(pro_json['page']['totalPages'],300)
                                if total == 300:
                                    writer_over1000.writerow([crmId,catalogName,pro_json['page']['totalPages']])
                            for pro in pro_content:
                                # 写入文档：品名 目录 品牌 价格 单位 商品型号 订货编码
                                proSkuProductName = pro['proSkuProductName'] 
                                # 日志
                                print(time.strftime('%H:%M:%S',time.localtime(time.time())),i,j,k,catalogName,total,page,proSkuProductName)

                                proBrandName = pro['proBrandName']
                                catalogs = pro['catalogs']['catalogs']
                                price = pro['price']
                                unitOfMeasureCode = pro['unitOfMeasureCode']
                                proMaterialNo = pro['proMaterialNo']
                                proSkuNo = pro['proSkuNo']
                                proSkuLeadTime = pro['proSkuLeadTime']
                                specificationList = pro['specificationList'] # 属性
                                specs = ''
                                for s in range(len(specificationList)):
                                    specs += specificationList[s]['proSpecName']+':'+specificationList[s]['specificationValue']
                                    if s!=len(specificationList)-1:
                                        specs += ' '
                                writer.writerow([proSkuProductName,catalogs[0]['catalogName'],catalogs[1]['catalogName'],catalogs[2]['catalogName'],catalogs[3]['catalogName'],proBrandName,price,unitOfMeasureCode,proMaterialNo,proSkuNo,proSkuLeadTime,specs])


    csv_file.close()
    csv_over1000_file.close()

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
    
