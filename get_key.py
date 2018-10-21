import urllib.request
import json

def chiave(id):
    with urllib.request.urlopen("https://www.airhive.it/api/newWeatherBee.php?id="+id) as url:
        res = json.load(url)
    with open("/chiave/key.txt", "w") as f:
        f.write(res["key"])
    return res["key"]
