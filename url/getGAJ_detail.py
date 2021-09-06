import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time
from html import unescape 
# 885有问题！！！
url = 'https://www.mymro.cn/brandindex.html'
# https://www.mymro.cn/product/table/319680?b=3928
# https://www.mymro.cn/product/table/319682?b=3928
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\data\\imgs\\'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Cookie':'AGL_USER_ID=b8862d59-6436-4394-990a-104cb20afc25; gr_user_id=5fb85d03-d6dd-4699-86aa-d732d8b0fde3; GCL.visitorid=6376471715039768029ed1e768-534d-4ddd-a3bc-30fb6e5a74ae; _ga=GA1.2.606732184.1629091545; bad_id76245970-bdeb-11eb-b324-bd20447c28e4=684492f1-fe52-11eb-b718-1b125cc200a9; _pk_id.1.e727=6376471715039768029ed1e768-534d-4ddd-a3bc-30fb6e5a74ae.1629091545.; Hm_lvt_c9dafaed6952edb29a666e9d22bd945e=1629091545,1629421996; href=https%3A%2F%2Fwww.mymro.cn%2Fb-53.html; nice_id76245970-bdeb-11eb-b324-bd20447c28e4=cd7a9941-0153-11ec-927a-e5b8ea64086f; ASP.NET_SessionId=4zrtuahxzu2i5pe1ua1ffz2j; __RequestVerificationToken=twnJPmk_DjD_d2iWKZqZ5ehQ5G6QezCdtKF3S_z-gXrKYoAwMk6OXwNFzFkiz_L-wkYSKw2; lastview=319690,1437707,325847,326072,325979; result-type=table; accessId=76245970-bdeb-11eb-b324-bd20447c28e4; _gid=GA1.2.1842793084.1629680718; a95b85e9769d6548_gr_session_id=0937bb25-06da-446b-a5c4-e3ebd327c14a; a95b85e9769d6548_gr_session_id_0937bb25-06da-446b-a5c4-e3ebd327c14a=true; _pk_ses.1.e727=1; Hm_lpvt_c9dafaed6952edb29a666e9d22bd945e=1629687945; qimo_seosource_76245970-bdeb-11eb-b324-bd20447c28e4=%E7%AB%99%E5%86%85; qimo_seokeywords_76245970-bdeb-11eb-b324-bd20447c28e4=; qimo_xstKeywords_76245970-bdeb-11eb-b324-bd20447c28e4=; pageViewNum=19',
}

def download_img(img_url, filepath):
    print (img_url)
    if(not img_url or img_url.startswith('https://172.31.0.246')):
        return
    r = requests.get(img_url, headers={}, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open(filepath, 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r


def get_data(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\gaj.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['链接','是否有历史','ID','品牌','名称','订货号','制造商型号','预计出货日','销售价','包装数量','其他','一级分类','二级分类','三级分类','四级分类','产品描述'])
    
    ddList = soup.select('.brandUL dd')
    print('ddList:',len(ddList))
    isBegin = False;
    for i in range(0,len(ddList)): #len(ddList)
        href = ddList[i].select('h3 a')[0].attrs['href']
        href = href.replace('/b-','').replace('.html','')       
        url1 = 'https://www.mymro.cn/b-'+href+'.html'
       
        print(isBegin)
        if(href == '1441'):
            print(href)
            isBegin = True
        if(isBegin == False):
            continue;
        
        print(i,'当前信息：',time.strftime('%H:%M:%S',time.localtime(time.time())))
        print('品牌：',url1)
        # 发送请求
        b_res = requests.get(url1,headers=headers)
        b_soup = BeautifulSoup(b_res.text,'html.parser',from_encoding='utf-8')
        all = b_soup.select('.brandULTit>div>a')
        if(len(all)==2): 
            cur_page = 1            
            total_page = 1
            while cur_page<=total_page:
                url2 = 'https://www.mymro.cn' + all[1].attrs['href'] + '&page='+str(cur_page) 
                print('分页：',url2) 
                page_res = requests.get(url2,headers=headers)
                page_soup = BeautifulSoup(page_res.text,'html.parser',from_encoding='utf-8')
                brand = page_soup.select('.p-category .filter-box .f-card:nth-child(2) .f-param-list-expand .f-param-item')
                brand_name=''
                if(len(brand)>0):
                    brand_name = brand[0].text.strip()
            
                total = page_soup.select('.p-category .main-box .m-page-box .m-page-list .m-item-label')
                if(len(total)>=1):
                    total_page = int(total[0].text.replace('共','').replace('页',''))
                p_list = page_soup.select('.m-result-table .m-item')
                print('商品列表:',len(p_list))
                if(len(p_list)>0):
                  for j in range(0,len(p_list)): #len(p_list)
                    product = p_list[j]
                    name_list = product.select('.m-item-name a')
                    p_href = name_list[0].attrs['href']
                    id = p_href.replace('g-','').replace('.html','')
                    name = name_list[0].text
                    # 图片
                    # img = product.select('.m-item-img-box img')
                    # if(len(img)>0):
                    #     p_img_path = file_path+id+'.jpg'
                    #     if not Path(p_img_path).exists():
                    #         img_url = img[0]['src']
                    #         if(img_url != 'https://static.mymro.cn/product_images_new/350/hp_np.png'):
                    #             download_img(img_url,p_img_path) 
                    print('商品名称：',name) 

                    table_list = product.select('.m-table')
                    print('商品列表有否：',len(table_list))
                    if(len(table_list) > 0):
                        # https://www.mymro.cn/u-10W9164.html
                        url3 = 'https://www.mymro.cn/'+p_href
                        print(url3)
                        all_pro = requests.get(url3,headers=headers)
                        detail = BeautifulSoup(all_pro.text,'html.parser',from_encoding='utf-8')

                        # .bread-crumd a
                        categorys = detail.select('.bread-crumd a')
                        cate_names = []
                        if(len(categorys) >= 6):
                            for c_i in range(1,5):
                                cate_names.append(categorys[c_i].text.strip())
                        print('分类：',cate_names)  

                        # .proDetailDiv  div:second产品描述
                        cpms = ''
                        isHistory = False
                        if(len(detail.select('.proDetailTit-history'))==0):
                            print('no history')
                            isHistory = False
                            proDetailDiv = detail.select('.proDetailDiv>div')
                            proDetailCpmsDiv = detail.select('.proDetailDiv>div:nth-child(2)>div:first-child')
                            if(len(proDetailCpmsDiv)>0):
                                cpms = proDetailCpmsDiv[0].text.strip()
                            if(len(proDetailDiv)>2):
                                isShuiyin = False
                                for pp in range(2,len(proDetailDiv)):#len(proDetailDiv)
                                    proDetailDivItem = proDetailDiv[pp]
                                    if(proDetailDivItem.text.strip()=='产品图片'): 
                                        isShuiyin = True
                                    if(not isShuiyin):
                                        proDetailDivItem_img = proDetailDivItem.select('img') 
                                        for img_index in range(0,len(proDetailDivItem_img)):  
                                            src = proDetailDivItem_img[img_index]['src']
                                            src = src if src.startswith('http') else ('https://'+src)
                                            src_arr = src.split('.')
                                            suffix = src_arr[len(src_arr)-1]
                                            path = file_path+id+'_'+str(img_index)+'.'+suffix;
                                            print(src,path)
                                            download_img(src,path) 
                        else:
                            print('has history')
                            isHistory = True
                            proDetailDiv = detail.select('.proDetailDiv>div:first-child>div:nth-child(2)')
                            cpms = proDetailDiv[0].text.strip()
                            proDetailDivItem_img = proDetailDiv[0].select('img') 
                            for img_index in range(0,len(proDetailDivItem_img)):
                                src = proDetailDivItem_img[img_index]['src']
                                src = src if src.startswith('http') else ('https://'+src)
                                src_arr = src.split('.')
                                suffix = src_arr[len(src_arr)-1]
                                path = file_path+id+'_'+str(img_index)+'.'+suffix;
                                print(src,path)
                                download_img(src,path)                           

                        dhh =''
                        zzsxh =''
                        yjchr =''
                        xsh=''
                        bzsl=''
                        qita=''
                        # .fixLeftTable .leftTable1 .pxTR td 标题
                        # .fixLeftTable .leftTable2 tr 值
                        fixLeftTable = detail.select('.fixLeftTable .leftTable1 .pxTR td')
                        fixLeftTableValue = detail.select('.fixLeftTable .leftTable2 tr')
                        # .scrollRightTable .rightTable1 .pxTR [title]
                        # .scrollRightTable .rightTable2 tr
                        scrollRightTable = detail.select('.scrollRightTable .rightTable1 .pxTR td')
                        scrollRightTableValue = detail.select('.scrollRightTable .rightTable2 tr')
                        # .fixRightTable .fixRightTable1 .pxTR .px 标题
                        # .fixRightTable .fixRightTable2 tr 值 
                        fixRightTable = detail.select('.fixRightTable .fixRightTable1 .pxTR .px')
                        fixRightTableValue = detail.select('.fixRightTable .fixRightTable2 tr')
                        if(len(fixLeftTable)==2 and len(fixRightTable)==2 and len(fixLeftTableValue) == len(scrollRightTableValue)):
                            other_title = []
                            for kk in range(0,len(scrollRightTable)):
                                other_title.append(scrollRightTable[kk].text.strip())
                            print(other_title)

                            for jj in range(0,len(fixLeftTableValue)):
                                left_a = fixLeftTableValue[jj].select('td span a')                                
                                dhh = left_a[0].text.strip()
                                zzsxh = left_a[1].text.strip()
                                right_a = fixRightTableValue[jj].select('td')
                                yjchr = right_a[0].text.strip()
                                xsh= right_a[1].text.strip()
                                scrool_a = (scrollRightTableValue[jj]).select('td')
                                for o_i in range(0,len(other_title)):
                                    if(other_title[o_i]=='包装数量'):
                                        bzsl = scrool_a[o_i].text.strip()
                                    else:                                        
                                        qita += other_title[o_i]+':'+scrool_a[o_i].text.strip()+';'

                                writer.writerow([url3,isHistory,id,brand_name,name,dhh,zzsxh,yjchr,xsh,bzsl,qita,cate_names[0],cate_names[1],cate_names[2],cate_names[3],cpms])
                    
                cur_page += 1
                
           
    
    csv_file.close()

if __name__ == '__main__':
    get_data(url)
    # download_img('https://172.31.0.246/pis/PMS/%E5%BE%AE%E4%BF%A1%E6%88%AA%E5%9B%BE_20201221102144_1608517327837.png','1.png')
