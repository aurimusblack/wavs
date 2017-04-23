s = [None]*9000

import requests
import sys
import config

print "\t\033[92m*************************************************"
print "\t\033[92m*              Directory Bruteforcer            *"
print "\t\033[92m*************************************************"


def useage():
    print "Usage: \npython %s example.com" %sys.argv[0]

def scan(url):
    f = open(config.dir_Path, "r")
    ct = 0
    for path in f:
	scan_url = url + path.strip()
        #print url
        res = requests.get(url=scan_url,headers=config.HEADER,timeout=config.TIMEOUT)
        status = res.status_code
	if status != 404 :
		s.append(scan_url+"/")
        	print "\t\033[92m[%d] %s" %(status,scan_url)
	else:
		print "\t\033[91m[%d] %s" %(status,scan_url)
    f.close()
def rescan():
	for x in s:
		scan(x)

def main():
    if len(sys.argv) != 2:
        useage()
        sys.exit(0)
    url = sys.argv[1]
    if "http://" in url:
	useage()
        sys.exit(0)
    url = "http://%s/" %url
    #print "url:\t %s" %url
    scan(url)
    rescan()



if __name__ == "__main__":
    main()
