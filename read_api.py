import urllib.request
import json

def get_air_data():
    with urllib.request("https://www.airhive.it/api/getCurrentAQ.php") as url:
        return json.dump(url)
