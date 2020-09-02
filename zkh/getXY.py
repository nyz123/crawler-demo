import requests
import csv
from bs4 import BeautifulSoup
import urllib.request
from pathlib import Path
import os
import time

url = 'http://www.ehsy.com/index.php?route=home/category/ajax_category_sub_tree'
file_path = 'F:\\xdl\\github\\crawler-demo\\zkh\\imgs\\'
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
    print(soup.title)
    tree_li = soup.find_all(class_ ='li-right-title')
    print(len(tree_li))

    csv_file = open('F:\\xdl\\github\\crawler-demo\\zkh\\data\\xy_cate.csv','w',encoding='utf-8')

    writer = csv.writer(csv_file)
    writer.writerow(['品名','一级目录','二级目录','三级目录','类别（四级）', '品牌', '型号', '价格', '单位', '订货编码','发货期','规格参数'])

    # 647,1147 1147,1647  2903
    for i in range(1647,2903): #len(tree_li)
        cate_name = tree_li[i].text
        cate_href = tree_li[i].a.attrs['href']
        print(cate_name,cate_href)
        
        page = 1
        total = 1
        while page <= total: # total
            print(i,total,page,time.strftime('%H:%M:%S',time.localtime(time.time())))  
            page_href = cate_href + '?p=' + str(page)
            # 发送请求
            page_res = requests.get(page_href,headers=headers)
            page_soup = BeautifulSoup(page_res.text,'html.parser',from_encoding='utf-8')
            # 目录
            product_cate1 = page_soup.select('.crumbs>a')
            product_cate2 = page_soup.select('.crumbs>.category-new-bread>.bread-title>.bread-span')
            cate_name1 = product_cate1[1].text
            cate_name2 = product_cate2[0].text
            cate_name3 = product_cate2[1].text
            print(page_href,cate_name1,cate_name2,cate_name3)
            # 目录1是否存在
            my_file = Path(file_path+cate_name1)
            if not my_file.exists():
                os.mkdir(my_file)
            # 分页 
            total_page = []           
            if page == 1:
                total_page = page_soup.select('.pagintion .pg-num-total')                

             # 商品信息
            products = page_soup.select('.product')
            # 属性名称
            product_attr_names =  page_soup.select('.commodity-information li.commodity-parameter>span')
            brand_index = -1 # 品牌Index
            model_index = -1 # 型号Index
            cate_index = -1 # 类别Index
            cate_index = -1 # Index
            p_attr_names = []
            if len(product_attr_names)>0:
                for a_n_i in range(len(product_attr_names)-1):
                    a_n = product_attr_names[a_n_i].text
                    if a_n=='品牌' and brand_index==-1:
                        brand_index = a_n_i
                    elif a_n=='型号' and model_index==-1:
                        model_index = a_n_i
                    elif a_n=='类别' and cate_index==-1:
                        cate_index = a_n_i
                    else:
                        p_attr_names.append(a_n)

                
            print('品牌/型号/类别：',brand_index,model_index,cate_index,p_attr_names)
            # 爬取一页
            for j in range(len(products)): #len(products)
                p_imgs = products[j].select('a>.p-image>.image-div>img') # 图片
                p_img = ''
                if(len(p_imgs)>0):
                    p_img = p_imgs[0].attrs['src']
                p_names = products[j].select('.p-name>a>.high-light')  # 品名
                p_name = ''
                if(len(p_names)>0):
                    p_name = p_names[0].text.replace('，',' ')
                p_skus = products[j].select('.order.ell>span:nth-of-type(n+2)') # sku
                p_sku = ''
                if(len(p_skus)>0):
                    p_sku = p_skus[0].text

                # 下载图片
                p_img_path = file_path + '//'+cate_name1+'//'+p_sku+'.jpg'
                if not Path(p_img_path).exists() and len(p_img)>0:
                    download_img(p_img,p_img_path)
                print(p_name)

                p_attrs =  products[j].select('.product-parameter li') # 属性
                attr=''
                # 遍历属性,价格倒数2，品牌1，型号2，类别3，发货期倒数1 
                a_index = 0
                cate_name4 = ''
                for a_i in range(len(p_attrs)-2):
                    a_n = p_attrs[a_i].text
                    if a_i==brand_index:
                        brand = a_n.replace(' ','')
                    elif a_i==cate_index:
                        cate_name4 = a_n
                    elif a_i==model_index:
                        model = a_n
                    else:
                        attr += p_attr_names[a_index] + ':' + a_n
                        if a_index!=len(p_attr_names)-1:
                            attr += ';'
                        a_index += 1
                price = p_attrs[len(p_attrs)-2].text
                send_date = p_attrs[len(p_attrs)-1].text
                units = products[j].select('.purchase-num .purchase-unit') # 单位
                unit = ''
                if len(units)>0:
                    unit = units[0].text
                writer.writerow([p_name,cate_name1,cate_name2,cate_name3,cate_name4,brand,model,price,unit,p_sku,send_date,attr])

            if page == 1:
                if len(total_page)==0:
                    break
                total_page = int(total_page[0].text.replace('共','').replace('页',''))
                total = total_page # total_page
            page += 1 

    csv_file.close()

if __name__ == '__main__':
    get_data(url)
    