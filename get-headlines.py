import urllib.request
import json

api = ""
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

