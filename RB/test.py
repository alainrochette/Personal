import requests
r = requests.get('https://api.discogs.com/database/search?track=Feel+No+Ways&artist=Drake&format=album')
resp_json = r.json()
# releases = resp_json['releases']
print(resp_json)
