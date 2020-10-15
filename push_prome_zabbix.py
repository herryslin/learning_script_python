import urllib2
import time
import socket
import json


hostname=socket.gethostname()
group=hostname[:7]

headers = {
	"Yf-Status-Domain":"*",
	"Host":"monitor.yfcdn.net"
}
url = "http://127.0.0.1/edgestatus"
pushurl= "http://prometheus.cdn.yfcdn.net:9091/metrics/job/lua_edge_push/instance/%s"%hostname
req = urllib2.Request(url=url,headers=headers)

try_num=3
while try_num>0:
	try:
		res = urllib2.urlopen(req,timeout=3)
		if res.code!=200:
			continue

		jres = json.loads(res.read())

		isfirst = True
		promString = ""
		for domain,metrics in jres.items():

			for metric,value in metrics.items():
				if isfirst:
					promString += "# TYPE edgestatus_%s gauge\n"% metric
				if not isinstance(value, dict):
					promString += "edgestatus_%s{domain=\"%s\",hostname=\"%s\",group=\"%s\",instance=\"%s\"} %.0f\n"%(metric,domain,hostname,group,hostname,value)
				else:
					for k,v in value.items():
						promString += "edgestatus_%s{domain=\"%s\",code=\"%s\",hostname=\"%s\",group=\"%s\",instance=\"%s\"} %.0f\n"%(metric,domain,k,hostname,group,hostname,v)

			isfirst = False

		push_req = urllib2.Request(pushurl,data=promString)

		r = urllib2.urlopen(push_req,timeout=10)
		# print r.code

		break
	except urllib2.URLError :

		time.sleep(0.5)
	finally:
		try_num -=1

