from re import findall
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import *

CLIENTID = "CLIENT_ID"
CLIENTSECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENTID,
        client_secret=CLIENTSECRET,
        show_dialog=True,
        cache_path="token.txt",
        username="username",
    )
)

# get songs for input year
year = input("Enter year: YEAR:\n")
URL = f"https://www.billboard.com/charts/hot-100/{year}/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')

song_names_inspect = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_inspect]


user_id = sp.current_user()["id"]
song_uris = []

for song in song_names:
    try:
        # Search for the track with the given name and year
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)

        # Check if there are results
        if result["tracks"]["items"]:
            # Get the first track's URI
            track = result["tracks"]["items"][0]
            uri = track["uri"]
            song_uris.append(uri)
            print(f"Added: {track['name']} by {track['artists'][0]['name']}")
        else:
            print(f"{song} not found on Spotify. Skipped.")
    except Exception as e:
        print(f"Error processing song '{song}': {e}")


playlist = sp.user_playlist_create(user=user_id, name=f"{year} Billboard 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

