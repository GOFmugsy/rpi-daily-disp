import urllib.request
import json

api = ""

apiJson = urllib.request.urlopen("https://api.nytimes.com/svc/mostpopular/v2/viewed/1.json?api-key=" + api).read()

decode = apiJson.decode('utf-8')

apiDict = json.loads(decode)

print(apiDict.keys())
