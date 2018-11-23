import requests, re, sqlite3,time
from bs4 import BeautifulSoup

'''
这是52av的偷拍自拍视频的抓取
'''

def getlink(listpage,conn):
    res0 = requests.get(listpage)
    soup0 = BeautifulSoup(res0.text, "html.parser")
    kk1 = soup0.find_all(name='a', attrs={"href": re.compile(r'^thread-'), "onclick": "atarget(this)"})
    title = [ i.get("title") for i in kk1]
    try:
        videolink = ["http://www.52av.tv/"+i.get("href") for  i in kk1]
        #print(videolink)
        zuhez = set(zip(title,videolink))
        for k in zuhez:
            link = getvideolink(k[1])
            #print(link)
            print(k[0].replace(" ",""),link)
            c.execute("INSERT or IGNORE INTO ziyuanlist VALUES (?,?,?)",(k[0].replace(" ",""),link,0))
            conn.commit()
    except:
        pass

def getvideolink(ss):
        res1 = requests.get(ss)
        soup1 = BeautifulSoup(res1.text, "html.parser")
        gg = soup1.find_all(name='iframe', attrs={"src": re.compile(r'^//video1.yocoolnet.com/.*')})
        #print(gg)
        for dd in gg:
            #print(dd)
            # 从视频页面剥离出纯净的视频播放页面的url，ff
            ff = str(dd.get("src")).replace("//","http://")
            #print(ff)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
                'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
                'Host': 'video1.yocoolnet.com',
                'Proxy - Connection': 'keep - alive',
                'Referer': ff
            }
            res2 = requests.get(ff, headers=headers)
            time.sleep(3)
            soup2 = BeautifulSoup(res2.text, "html.parser")
            # 从纯净的视频播放页面提取出视频的下载链接url,videoclip
            gg = soup2.find_all("script")
            jj = str(gg)
            #print(jj)
            pattern = re.compile('https://test.yocoolnet.com/files/mp4/.*')
            result1 = pattern.findall(jj)
            # result1是片段下载和封面图片链接的列表
            #print(result1)
            # picture是封面链接
            #picturelink = str(result1[1])[0:-2]
            #print(picturelink)
            # videolink视频片段下载链接
            return str(result1[0][0:-3])

if __name__ == '__main__':
    conn = sqlite3.connect("ziyuan.db")
    c = conn.cursor()

    for i in range(1,20):
        url = "http://www.52av.tv/forum-64-"+str(i)+".html"
        getlink(url,conn)

    '''
    url = "http://www.52av.tv/forum-64-21.html"
    getlink(url,conn)
    conn.close()
    '''




'''

import requests,re
html = requests.get("http://www.52av.tv/forum-64-1.html")
html.encoding == html.apparent_encoding
res = re.findall('<li style="width:237px">(.*?)<div class="c cl">(?P<div1>.*?)</div>(.*?)<h3 class="xw0">(?P<h3>.*?)</h3>(.*?)<div class="auth cl">(?P<div2>.*?)</div>(.*?)</li>',html.text,re.S)
lis = []
for i in res:
    try:
        res1 = re.search('(?P<url>\w{6}-\d{5}-\d-\d\.html)"(.*?)title="(?P<title>.*?)"(.*?)<!--<img src="(?P<pic>.*?)"',i[1],re.S)
        lis.append(res1.groupdict())
    except:
        pass

for j in range(len(lis)):
    html1= requests.get("http://www.52av.tv/"+str(lis[j]['url']))
    html1.encoding == html1.apparent_encoding
    res2 = re.search('<center>(.*?)<iframe id="allmyplayer"(.*?)src="(?P<closeurl>.*?)"',html1.text,re.S)
#    print(res2.group("closeurl"))
    headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 4 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19',
                'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8',
                'Host': 'video1.yocoolnet.com',
                'Proxy - Connection': 'keep - alive',
                'Referer':"http://www.52av.tv/"+str(lis[j]['url'])
            }
    html2 = requests.get(res2.group("closeurl"),headers=headers)
    html2.encoding == html2.apparent_encoding
    try:
        res3 = re.search("http://video1.yocoolnet.com/files/mp4.*?\.m3u8",html2.text)
        print (lis[j]['title'],res3.group(0))
    except:
        pass

'''
