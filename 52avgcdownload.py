# -*- coding: utf-8 -*-
import requests,os,sqlite3,time
from contextlib import closing

def download_file(url0, path0,newpath):
	with open(path0, "wb") as f:
		for i in range(6000):
			url = url0 + str(i) + '.ts'
			print(url)
			with closing(requests.get(url, stream=True)) as r:
				chunk_size = 1024
				content_size = int(r.headers['content-length'])
				if (content_size > 30):
					#print("下载第" + str(i) + "段，大小为:" + str(content_size))
					n = 1
					for chunk in r.iter_content(chunk_size=chunk_size):
						loaded = n * 1024.0 / content_size
						f.write(chunk)
						f.flush()
						os.fsync(f.fileno())
						n += 1
				else:
					#comm0 = "ffmpeg -i {0} -acodec copy -vcodec copy -f mp4 -bsf:a aac_adtstoasc {1} -y".format(str(path0),str(newpath))	#转码生成新文件
					#os.system(comm0)
					#time.sleep(2)
					#while True:
					#	comm1 = 'onedrivecmd put "{0}" od:/'.format(str(newpath))
					#	print(comm1)
					#	res = os.popen(comm1)
					#	if str(list(res)) != "Annotations must be specified before other elements in a JSON object":
					#		break
					break

if __name__ == '__main__':
	conn = sqlite3.connect("ziyuan.db")
	c = conn.cursor()
	res0 = c.execute("select * from ziyuanlist")
	lis=[]
	for u in res0:
		lis.append(u)
	conn.commit()
	conn.close()
	for i in lis:
		#判断欲下载的资源是否已经下载,是0说明没下载过
		if i[2]==0:
			i0 = str(i[0]).replace(' ','').replace("(","").replace(")","")		#片名
			path0 = "/root/new_52av/oldvideo/" + i0 + ".mp4"
			newpath = "/root/new_52av/newvideo/" + i0 + ".mp4"
			url0 = str(i[1])[0:-5]		#片子m3u8链接
			download_file(url0, path0,newpath)	
			conn1 = sqlite3.connect("ziyuan.db")
			c1 = conn1.cursor()
			#如果执行了下载，则在数据库中把这个资源标志为已经下载
			c1.execute("UPDATE ziyuanlist SET token = 1 WHERE name == ?",(i[0],))
			conn1.commit()
			conn1.close()
			comm0 = "ffmpeg -i {0} -acodec copy -vcodec copy -f mp4 -bsf:a aac_adtstoasc {1} -y".format(str(path0),str(newpath))    #转码生成新文件
			os.system(comm0)
			while True:
				comm1 = 'onedrivecmd put "{0}" od:/video/52av/'.format(str(newpath))
				print(comm1)
				res = os.popen(comm1)
				try:
					clean = str(list(res)[0]).replace("\n","")
					print(clean)
				except:
					clean = "ok"
				if clean != "Annotations must be specified before other elements in a JSON object":
					break
			os.system("rm -rf {0}".format(path0))
			os.system("rm -rf {0}".format(newpath))
			#break
	#    url0 = input("请输入链接:")
	#    path0 = input("存储地址:")
