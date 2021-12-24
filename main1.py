import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

Client_ID = "5e5e0c73f7d24baf8d88b6b27244e52b"
Client_Secret = "f13678d072b5437a91878ea51dc75bc1"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=Client_ID,
        client_secret=Client_Secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)

usr_id = sp.current_user()["id"]

ip = input("Which year do you like to travel to? Type the date in this format YYYY-MM-DD: ")

rsp = requests.get(url=f"https://www.billboard.com/charts/hot-100/{ip}")

nums = []
song = []

soup = BeautifulSoup(rsp.text, "html.parser")
no = soup.find_all(name="span", class_="chart-element__rank__number")
[nums.append(i.getText()) for i in no]
sng = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
[song.append(j.getText()) for j in sng]
print(nums)
print(song)

song_uris = []
yr = ip.split("-")[0]
for sg in song:
    result = sp.search(q=f"track:{sg} year:{yr}", type="track")
    # pprint.pprint(result)
    try:
        uri_a = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri_a)
    except IndexError:
        print(f"{sg}: doesn't exist in Spotify. So, Skipped.")
pprint.pprint(song_uris)

playlst = sp.user_playlist_create(user=usr_id, name=f"{ip} billBoard 100", public=False)
# pprint.pprint(playlst)

ab = sp.playlist_add_items(playlist_id=playlst["id"], items=song_uris)
# pprint.pprint(ab)
