user="wangxiao"
password="wx123456"
def mall(fun):
    def mall_1(*args,**kwargs):
       print('test')
    return mall_1()



def index1():
    print('欢迎进入首页')
    
index1()

@mall
def home():
    print("个人中心")
@mall
def shopping():
    print("购物中心")