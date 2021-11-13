#!/usr/bin/env python3

import urllib.request
import json
import config as cfg

api = cfg.apikey

if not api:
    print("need an api key")
    exit()

apiJson = urllib.request.urlopen("https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=" + api).read()
decode = apiJson.decode('utf-8')
apiDict = json.loads(decode)

i = 0
for article in apiDict["results"]:
	i = i + 1
	if i > 3:
		continue
	print(article["title"])
	print(article["abstract"])
	print()

