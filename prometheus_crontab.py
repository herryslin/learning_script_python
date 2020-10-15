import urllib2
import time
import socket
import json
import re


# from StringIO import StringIO
# import gzip


# def gzip_compress(c_data):
# 	buf = StringIO()

# 	with gzip.GzipFile(mode='wb', fileobj=buf) as f:
# 		f.write(c_data)

# 	return  buf.getvalue()




res = urllib2.urlopen(url="http://yumrepo.yfcdn.net/top_domain_list",timeout=10)
domains_str = res.read()
domains_list = domains_str.split("\n")



hostname=socket.gethostname()
url = "http://127.0.0.1:8787/metrics"

pushurl= "http://prometheus.cdn.yfcdn.net:9091/metrics/job/lua_edge_push_v2/instance/%s"%hostname
#nginx open gzip
# pushurl= "http://prometheus.cdn.yfcdn.net:9088/metrics/job/lua_edge_push_v2/instance/%s"%hostname
req = urllib2.Request(url=url)

re_str=r'domain="([^"]+)"'

try_num=3
while try_num>0:
	try:
		res = urllib2.urlopen(req,timeout=3)
		if res.code!=200:
			continue

		promString = res.read()
		newPromString = ""
		for i in promString.split("\n"):

			ret = re.findall(re_str,i)
			if len(ret)==1:
				domain = ret[0]
				if domain not in domains_list:
					continue

			if "# HELP" in i:
				continue
			if "_bucket" in i:
				continue

			newPromString += i
			newPromString += "\n"


		# push_req = urllib2.Request(pushurl,data=gzip_compress(newPromString))
		push_req = urllib2.Request(pushurl,data=newPromString)
		# print promString
		push_req.get_method = lambda: 'PUT'
		# push_req.add_header('Content-Encoding','gzip')
		r = urllib2.urlopen(push_req,timeout=60)
		print r.code

		break
	except urllib2.URLError :

		time.sleep(0.5)
	finally:
		try_num -=1


