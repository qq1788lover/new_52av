#! /bin/python
#
import os,re

res = os.popen("onedrivecmd list od:/video/52av/")
res_list = list(res)[1:]
#print(len(res_list))
#quit()
for i in res_list:
	ev = str(i).split("\t")[0].replace("\n","")
	print(ev)
