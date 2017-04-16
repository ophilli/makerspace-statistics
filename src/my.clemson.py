import requests
import json
import time

with requests.Session() as s:
	parameters = {'request.preventCache' : time.time() * 1000};

	x = 0
	while(True):	
		r = s.get('https://my.clemson.edu/srv/feed/static/buses/positions.json', params = parameters)
		
		print(json.dumps(r.json()[4], indent=2))
		
		x += 1
		print(x)

		time.sleep(1)
