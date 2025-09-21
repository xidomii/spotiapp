import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="http://127.0.0.1:8000/callback",
    scope="user-library-read playlist-modify-public playlist-modify-private"
))

user_id = sp.current_user()['id']

# Playlist erstellen
playlist = sp.user_playlist_create(user=user_id, name='Lieblingssongs', public=False)
playlist_id = playlist['id']

# Alle gespeicherten Songs abrufen (maximal 2500)
track_uris = []
limit_per_request = 50
max_tracks = 2500
results = sp.current_user_saved_tracks(limit=limit_per_request)
while results and len(track_uris) < max_tracks:
    for item in results['items']:
        if len(track_uris) >= max_tracks:
            break
        track_uris.append(item['track']['uri'])
    if results['next'] and len(track_uris) < max_tracks:
        results = sp.next(results)
    else:
        break

# Songs in 100er-Chunks hinzufügen
for i in range(0, len(track_uris), 100):
    sp.playlist_add_items(playlist_id, track_uris[i:i+100])

print(f"Playlist 'Lieblingssongs' wurde erstellt und mit {len(track_uris)} Songs gefüllt.")
# Alle gespeicherten Songs abrufen (maximal 2500)