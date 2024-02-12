import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

def authenticate_spotify():
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri='http://127.0.0.1:5000',
        scope="playlist-modify-private,playlist-read-private"))
    return sp

def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        tracks.extend(results['items'])
        results = sp.next(results)
    return tracks

def find_duplicates_in_playlists(sp, source_playlist_tracks, playlist_names):
    user_id = sp.current_user()['id']
    playlists = sp.user_playlists(user_id)
    duplicate_tracks = []

    for playlist in playlists['items']:
        if playlist['name'] in playlist_names:
            playlist_tracks = get_playlist_tracks(sp, playlist['id'])
            for track in playlist_tracks:
                if track['track']['id'] in source_playlist_tracks:
                    duplicate_tracks.append(track['track']['id'])

    return set(duplicate_tracks)

if __name__ == "__main__":
    sp = authenticate_spotify()

    # Prompt user for the source playlist name
    source_playlist_name = input("Enter the name of the source playlist: ")
    source_playlist_id = None
    playlist_names = input("Enter the names of playlists to check, separated by a comma: ").split(',')

    # Find the source playlist ID
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == source_playlist_name:
            source_playlist_id = playlist['id']
            break

    if not source_playlist_id:
        print(f"{source_playlist_name} playlist not found.")
    else:
        # Get track IDs from the source playlist
        source_playlist_tracks = [track['track']['id'] for track in get_playlist_tracks(sp, source_playlist_id)]
        # Find duplicates in the specified playlists
        duplicates = find_duplicates_in_playlists(sp, source_playlist_tracks, playlist_names)

        # Remove duplicates from the source playlist
        if duplicates:
            for track_id in duplicates:
                sp.playlist_remove_all_occurrences_of_items(source_playlist_id, [track_id])
            print(f"Removed {len(duplicates)} duplicates from {source_playlist_name}.")
        else:
            print("No duplicates found.")
