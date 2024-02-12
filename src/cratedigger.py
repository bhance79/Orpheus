# Python script that creates CRATEDIGGER if not created already and adds songs from 'Discovery weekly' to it

import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_discovery_weekly_tracks(sp):
    for playlist in sp.current_user_playlists()['items']:
        if playlist['name'] == 'Discover Weekly':
            discovery_weekly_id = playlist['id']
            results = sp.playlist_tracks(discovery_weekly_id)
            tracks = results['items']
            while results['next']:
                results = sp.next(results)
                tracks.extend(results['items'])
            return tracks
    return []

def add_tracks_to_cratedigger(sp, tracks):
    cratedigger_id = None
    for playlist in sp.current_user_playlists()['items']:
        if playlist['name'] == 'CRATEDIGGER':
            cratedigger_id = playlist['id']
            break
    if not cratedigger_id:
        user_id = sp.current_user()['id']
        cratedigger = sp.user_playlist_create(user_id, 'CRATEDIGGER', public=False)
        cratedigger_id = cratedigger['id']

    track_uris = [track['track']['uri'] for track in tracks]
    sp.playlist_add_items(cratedigger_id, track_uris)

if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri='http://127.0.0.1:5000',
        scope="playlist-modify-private,playlist-read-private"))

    tracks = get_discovery_weekly_tracks(sp)
    if tracks:
        add_tracks_to_cratedigger(sp, tracks)
        print(f"Added {len(tracks)} tracks to CRATEDIGGER.")
    else:
        print("No tracks found in Discovery Weekly.")
