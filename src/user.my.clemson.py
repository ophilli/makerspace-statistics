import requests
import json
import time

with requests.Session() as s:
	parameters = {'cn' : 'ophilli', 'request.preventCache' : (int)(time.time() * 1000)}
	print(parameters)
	headers = {'Referer' : 'https://my.clemson.edu'}
	print(headers)

	r = s.get('https://my.clemson.edu/srv/feed/dynamic/directory/getInfoByCN', params=parameters, headers=headers)
	
	print(json.dumps(r.json(), indent=2))
