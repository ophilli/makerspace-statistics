import requests
import json
import time

with requests.Session() as s:
	while(True):	
		parameters = {'request.preventCache' : (int)(time.time() * 1000)}
		print(parameters)

		r = s.get('https://my.clemson.edu/srv/feed/static/buses/positions.json', params = parameters)
		
		print(json.dumps(r.json()[4], indent=2))

		time.sleep(1)
