#coding = utf-8
#__author__:'sareeliu'
#__date__ : '2018/11/24 22:39'

import requests, re, json

# from urllib import parse
# url = parse.quote("http://tool.chinaz.com/tools/urlencode.aspx")
# hh = requests.get("http://suo.im/api.php?url="+res)

def getdwz(url):

    #先分析网页，拿到 generate_id 和 generate_cid
    html = requests.get("http://suo.im")
    id = re.search('<input type="hidden" id="generate_id" value="(.*)">',html.text).group(1)
    cid = re.search('<input type="hidden" id="generate_cid" value="(.*)">',html.text).group(1)
    # print(id,cid)

    formdata = {
        "url": url,
        "generate_id": id,
        "generate_cid": cid,
        "effective_date": "1"
    }

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,th;q=0.7,zh-TW;q=0.6,ja;q=0.5",
        "Connection": "keep-alive",
        "Content-Length": "205",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Cookie": "sitename=%7Bb09e8760-12eb-536f-ecf7-858cf8435b2e%7D; PHPSESSID=ht4348cdfmuji0sb9qcmfga8o7; tinyurl_generate_cookie_id=qA8ree%262xMZyWac%237Y9XQCU%21u3%231; bdshare_firstime=1543068285605; Hm_lvt_e0b9cd88e830ccbbe41dc1122558b669=1543068285,1543112035,1543113974,1543114205; Hm_lpvt_e0b9cd88e830ccbbe41dc1122558b669=1543114205",
        "Host": "suo.im",
        "Origin": "http://suo.im",
        "Referer": "http://suo.im/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    post_html = requests.post("http://suo.im/front/index/urlCreate/",data=formdata,headers = headers)
    return (json.loads(post_html.text)['list'])

if __name__ == "__main__":
    url = "http://neue.v2ex.com/t/308818"
    dwz = getdwz(url)
    print(dwz)