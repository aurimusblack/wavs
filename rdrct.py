import requests
import sys
import time
import os


os.system('clear')
print "\t\033[92m*************************************************"
print "\t\033[92m*              Open redirect Scanner            *"
print "\t\033[92m*************************************************"
payload = sys.argv[2]
time.sleep(3)
print ""
print "Getting targets from  the FILE "
print ""
line2 = sys.argv[1]

with open(payload) as fh:
	for x in fh:
		payld = x.strip()
                line3 = line2 + payld
		print line3
		resp = requests.get(line3, verify=True)    
		print resp
		try:
			if resp.history:
                             
		        	print "Request was redirected"
		                             
		               	for resp in resp.history:

		                	print "|"
		                        print resp.status_code, resp.url
                                    

		                print "Final destination:"

		                print "+"
		                print resp.status_code, resp.url

                                
			else:
				print "Request was not redirected"
		except:
		                	print "connection error :("
	

                            
		                

