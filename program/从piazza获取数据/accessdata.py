__author__ = 'zhangyanni'

#coding='utf-8'
import gzip
import http.cookiejar
import urllib.request
import urllib.parse
import json
import codecs
import socket


#ungzip解压数据
def ungzip(data):
    try:        # 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data


#getOpener 函数接收一个 head 参数, 这个参数是一个字典. 函数把字典转换成元组集合, 放进 opener.
#自动处理使用 opener 过程中遇到的 Cookies
#自动在发出的 GET 或者 POST 请求中加上自定义的 Header
cj = http.cookiejar.CookieJar()
pro = urllib.request.HTTPCookieProcessor(cj)
opener = urllib.request.build_opener(pro)
urllib .request .install_opener(opener)

def piazza_login():
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection':'keep-alive',
        'Host':'piazza.com',
        'Referer:':'https://piazza.com/class/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
    #postDict是登录时所post的表单
   
    print('登录中...')


   
    url = 'https://piazza.com/demo_login?nid=i5j09fnsl7k5x0&auth=b2410d0'

    req = urllib.request.Request (url)
    response=urllib .request .urlopen(req)
    print(response)
    data=response.read()
    # print(data)
    #登录到piazza，并get登录后的网页保存在piazza_logindata.txt
    data=data.decode(encoding='UTF-8',errors='ignore')
    saveFile("piazza-login-data",data)
    print("登录成功！")
    


#从piazza的api中获得json数据，根据发送的postJson不同获得不同的数据，可获得某一个标签的所有问题，或指是cid的某一个问题    
def piazza_getdata_from_api(postJson):
    
    
    postData=json.dumps(postJson).encode()
    url="https://piazza.com/logic/api/"
    socket.setdefaulttimeout(2000)
    try:
        req = urllib.request.Request(url,postData)
        response=urllib .request .urlopen(req)
        data=response.read()
        # data = ungzip(data)
        data=data.decode() 
        #处理data的中文
        myjson=json.loads(data)
        newjson=json.dumps(myjson,ensure_ascii=False)
        return newjson
    except:
        print("timeout")
        return "timeout"

#保存数据到文件中  
def saveFile(file_name,data):
    output = codecs.open("piazza-data/"+file_name+".json",'w',"utf-8")
    output.write(data)
    output.close()   
    print("already write to "+file_name+".json")
#读文件
def readFile(file_name):
    fileIn = codecs.open(file_name,'r',"utf-8")
    data=fileIn.read()
    fileIn.close()
    return data

#调用函数登录到piazza
piazza_login()
print("------------------------------------------------------------------------")
select = input('读取全部讨论记录请输入1；读取某一条讨论记录请输入2：')
nid=input("请输入您的nid 例如：https://piazza.com/class/i5j09fnsl7k5x0?cid=493的nid为i5j09fnsl7k5x0：") 
if select=='1':   
    
    postJson={"method":"network.get_my_feed","params":{"nid":nid,"sort":"updated"}}
    data=piazza_getdata_from_api(postJson)
    saveFile("piazza_my_feed",data)
    data=readFile("piazza_my_feed.json")
    #把 json字符串转成字典，便于解析数据
    data_dict=json.loads(data)
    dict = {}
    #获得"result"下的"feed"列表
    items=data_dict['result']['feed']
    #遍历items获得所有问题的id和nr
    for item in items:
        id = item['id']
        nr = item['nr']
        dict[nr]=id
    #根据nr向api发出POST请求获得所有问题的json数据
    for nr in dict.keys():
        print(nr)
        postJson={"method":"content.get","params":{"cid":nr,"nid":"i5j09fnsl7k5x0"}}
        data=piazza_getdata_from_api(postJson)
        file_name=str(nr)
        saveFile(file_name,data)
elif select=='2':
    #获得指定id的json数据
    while(1):
                     
        cid=input('请输入讨论记录的id(例如：https://piazza.com/class/i5j09fnsl7k5x0?cid=493的id为493)：')
        postJson={"method":"content.get","params":{"cid":cid,"nid":nid}}
        data=piazza_getdata_from_api(postJson)
        file_name=str(cid)
        saveFile(file_name,data)
        exit_2=input('退出?(y/n)：')
        if exit_2=='y':
            break
        
    
        
                   

   



