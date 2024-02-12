# Python script to remove duplicates within the same playlist
# NOTE: singles and songs from albums count as different songs and therefore not as duplicates
#       working on that

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri='http://127.0.0.1:5000',
        scope="playlist-modify-private,playlist-read-private,playlist-modify-public"))
    return sp

def find_playlist_by_name(sp, playlist_name):
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():
            return playlist['id']
    return None

def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def remove_duplicate_tracks(sp, playlist_id, tracks):
    track_uris = [item['track']['uri'] for item in tracks]
    unique_track_uris = list(set(track_uris))  # Convert set back to list to keep the order

    if len(unique_track_uris) < len(track_uris):
        print(f"Found {len(track_uris) - len(unique_track_uris)} duplicate tracks. Removing duplicates...")

        # Clear the playlist first before adding unique tracks back
        sp.playlist_replace_items(playlist_id, [])

        # Add unique tracks back to the playlist in batches of 100
        for i in range(0, len(unique_track_uris), 100):
            batch = unique_track_uris[i:i+100]
            sp.playlist_add_items(playlist_id, batch)

        print("Duplicates removed.")
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    sp = authenticate_spotify()
    playlist_name = input("Enter the playlist name: ")
    playlist_id = find_playlist_by_name(sp, playlist_name)
    if playlist_id:
        tracks = get_playlist_tracks(sp, playlist_id)
        remove_duplicate_tracks(sp, playlist_id, tracks)
    else:
        print("Playlist not found. Please check the name and try again.")