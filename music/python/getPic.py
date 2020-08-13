import urllib.request

def download_img(img_url, api_token=''):
    header = {"Authorization": "Bearer " + api_token} # 设置http header
    request = urllib.request.Request(img_url, headers=header)
    try:
        response = urllib.request.urlopen(request)
        img_name = "img.png"
        filename = "F:\\xdl\\"+ img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read()) # 将内容写入图片
            return filename
    except:
        return "failed"

if __name__ == '__main__':
    # 下载要的图片
    img_url = "http://jygy-mall-test.oss-cn-hangzhou.aliyuncs.com/mall/images/product1595908086739.png"
    download_img(img_url)