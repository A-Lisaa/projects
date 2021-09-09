import requests

for i in range(20):
    print(requests.get(f"https://ws.audioscrobbler.com/2.0/?method=user.getlovedtracks&user=DvaChe59&page={i}&api_key=5b786ecb2cbb8a330422ab32b84be32e", headers={"user-agent":"loved_tracks_copier"}).text)