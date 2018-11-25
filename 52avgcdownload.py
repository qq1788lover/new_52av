# -*- coding: utf-8 -*-
import requests, os, sqlite3, time, re, threading
from contextlib import closing
from dwz import getdwz

def download_file(video_m3u8, oldpath, newpath):
    with open(oldpath, "wb") as f:
        i = 0
        while True:
            url = video_m3u8[0:-5] + str(i) + '.ts'  # 对m3u8链接切片，构造ts
            print(url)
            with closing(requests.get(url, stream=True)) as r:  # r对应一个ts完整请求
                content_size = int(r.headers['content-length'])  # 获取ts大小
                if (content_size < 50):
                    break
                for chunk in r.iter_content(chunk_size=1024):  # 对ts大小按1024进行存到硬盘
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
            i = i + 1  # 存完一个ts，进行下一个ts


def handle_file(video_m3u8, oldpath, newpath):
    # 1.数据库处理
    conn = sqlite3.connect("ziyuan.db")
    c = conn.cursor()
    c.execute("UPDATE ziyuanlist SET token = 1 WHERE downlink = ?", (video_m3u8,))
    conn.commit()
    conn.close()
    # 2.视频转码处理
    comm = "ffmpeg -i {0} -acodec copy -vcodec copy -f mp4 -bsf:a aac_adtstoasc {1} -y".format(str(oldpath),str(newpath))  # 转码生成新文件
    os.system(comm)


def upload_file(video_m3u8, oldpath, newpath):
    while True:
        comm = 'onedrivecmd put "{0}" od:/video/52av/'.format(str(newpath))
        print(comm)
        res = os.popen(comm)
        try:
            clean = str(list(res)[0]).replace("\n", "")
            print(clean)
        except:
            clean = "ok"
        if clean != "Annotations must be specified before other elements in a JSON object":
            break


def share_file(video_m3u8, oldpath, newpath,video_name):
    comm = "onedrivecmd share {0}".format("od:/video/52av/"+video_name+".mp4")
    res = os.popen(comm)
    sharelink = str(list(res)[0]).replace("\n", "")
    print(sharelink)

    conn = sqlite3.connect("ziyuan.db")
    c = conn.cursor()
    c.execute("UPDATE ziyuanlist SET downlink = ? WHERE sharelink = ?", (video_m3u8,sharelink))
    conn.commit()
    conn.close()


def dwz(video_m3u8, oldpath, newpath,video_name):

    conn = sqlite3.connect("ziyuan.db")
    c = conn.cursor()
    sharelink = c.execute("SELECT sharelink WHERE downlink = ?",(video_m3u8,))
    dwz = getdwz(sharelink)
    print(dwz)
    c.execute("UPDATE ziyuanlist SET dwz = ? WHERE sharelink = ?", (dwz,))
    conn.commit()
    conn.close()


def action(video_m3u8, oldpath, newpath,video_name):
    download_file(video_m3u8, oldpath, newpath)
    handle_file(video_m3u8, oldpath, newpath)
    upload_file(video_m3u8, oldpath, newpath)
    share_file(video_m3u8, oldpath, newpath,video_name)
    dwz(video_m3u8, oldpath, newpath)
    os.system("rm -rf {0}".format(oldpath))
    os.system("rm -rf {0}".format(newpath))


if __name__ == '__main__':

    # 从数据库获取 没被下载过的资源 的结果集，存入list列表，并进行去重！
    conn = sqlite3.connect("ziyuan.db")
    c = conn.cursor()
    db_result = c.execute("SELECT * FROM ziyuanlist WHERE token = 0 AND downlink NOT NULL ")
    result_list = []
    for u in db_result:
        result_list.append(u)
    conn.commit()
    conn.close()
    result_list = set(result_list)  # 列表去重

    threads_list = []  # 线程列表
    # 遍历list列表
    for i in result_list:
        video_name = re.sub("[“”（）？，、。！【】\s]", "", str(i[0]))  # 片名
        prefix0 = "F:\\videotutorial\\ceshi\\"
        prefix = "/root/new_52av/"
        oldpath = prefix + "oldvideo/" + video_name + ".mp4"
        newpath = prefix + "newvideo/" + video_name + ".mp4"
        video_m3u8 = str(i[1])  # 片子完整的m3u8链接
        t = threading.Thread(target=action, args=(video_m3u8, oldpath, newpath,video_name))
        threads_list.append(t)

    for t in threads_list:
        t.start()
        while True:
            # 判断正在运行的线程数量,如果小于5则退出while循环,
            if (len(threading.enumerate()) < 8):
                break

