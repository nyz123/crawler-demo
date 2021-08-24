import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'https://www.mymro.cn/brandindex.html'
# https://www.mymro.cn/product/table/319680?b=3928
# https://www.mymro.cn/product/table/319682?b=3928
file_path = 'F:\\xdl\\github\\crawler-demo\\url\\imgs\\'
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'Cookie':'AGL_USER_ID=b8862d59-6436-4394-990a-104cb20afc25; gr_user_id=5fb85d03-d6dd-4699-86aa-d732d8b0fde3; GCL.visitorid=6376471715039768029ed1e768-534d-4ddd-a3bc-30fb6e5a74ae; _ga=GA1.2.606732184.1629091545; bad_id76245970-bdeb-11eb-b324-bd20447c28e4=684492f1-fe52-11eb-b718-1b125cc200a9; _pk_id.1.e727=6376471715039768029ed1e768-534d-4ddd-a3bc-30fb6e5a74ae.1629091545.; Hm_lvt_c9dafaed6952edb29a666e9d22bd945e=1629091545,1629421996; href=https%3A%2F%2Fwww.mymro.cn%2Fb-53.html; nice_id76245970-bdeb-11eb-b324-bd20447c28e4=cd7a9941-0153-11ec-927a-e5b8ea64086f; ASP.NET_SessionId=4zrtuahxzu2i5pe1ua1ffz2j; __RequestVerificationToken=twnJPmk_DjD_d2iWKZqZ5ehQ5G6QezCdtKF3S_z-gXrKYoAwMk6OXwNFzFkiz_L-wkYSKw2; lastview=319690,1437707,325847,326072,325979; result-type=table; accessId=76245970-bdeb-11eb-b324-bd20447c28e4; _gid=GA1.2.1842793084.1629680718; a95b85e9769d6548_gr_session_id=0937bb25-06da-446b-a5c4-e3ebd327c14a; a95b85e9769d6548_gr_session_id_0937bb25-06da-446b-a5c4-e3ebd327c14a=true; _pk_ses.1.e727=1; Hm_lpvt_c9dafaed6952edb29a666e9d22bd945e=1629687945; qimo_seosource_76245970-bdeb-11eb-b324-bd20447c28e4=%E7%AB%99%E5%86%85; qimo_seokeywords_76245970-bdeb-11eb-b324-bd20447c28e4=; qimo_xstKeywords_76245970-bdeb-11eb-b324-bd20447c28e4=; pageViewNum=19',
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
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,'html.parser',from_encoding='utf-8')
    
    csv_file = open('F:\\xdl\\github\\crawler-demo\\url\\data\\gaj.csv','w',encoding='utf-8')
    writer = csv.writer(csv_file)
    writer.writerow(['ID','品牌','名称','订货号','制造商型号','预计出货日','销售价','包装数量','其他'])
    
    ddList = soup.select('.brandUL dd')
    print('ddList:',len(ddList))
    for i in range(0,len(ddList)): #len(ddList)
        href = ddList[i].select('h3 a')[0].attrs['href']
        href = href.replace('/b-','').replace('.html','')       
        url1 = 'https://www.mymro.cn/b-'+href+'.html'
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
                    id = name_list[0].attrs['href'].replace('g-','').replace('.html','')
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
                        # 查询耿多https://www.mymro.cn/product/table/326117?b=53&page123456=2
                        url3 = 'https://www.mymro.cn/product/table/'+id+'?b='+href + '&page123456='+str(cur_page)
                        print(url3)
                        all_pro = requests.get(url3,headers=headers)
                        table = BeautifulSoup(all_pro.text,'html.parser',from_encoding='utf-8')
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

    
                                print(id,brand_name,name,dhh,zzsxh,yjchr,xsh,bzsl)
                                writer.writerow([id,brand_name,name,dhh,zzsxh,yjchr,xsh,bzsl,qita])
                 
                    
                cur_page += 1
                
           
    
    csv_file.close()

if __name__ == '__main__':
    get_data(url)
