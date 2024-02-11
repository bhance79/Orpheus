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

def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def sort_tracks(tracks, sort_option, sort_order):
    reverse_order = True if sort_order == '2' else False  # '2' corresponds to descending order

    if sort_option == '1':  # Track Name
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['name'], reverse=reverse_order)
    elif sort_option == '2':  # Artist Name
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['artists'][0]['name'], reverse=reverse_order)
    elif sort_option == '3':  # Album Name
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['album']['name'], reverse=reverse_order)
    elif sort_option == '4':  # Release Date
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['album']['release_date'], reverse=reverse_order)
    elif sort_option == '5':  # Track Duration
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['duration_ms'], reverse=reverse_order)
    elif sort_option == '6':  # Popularity
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['popularity'], reverse=reverse_order)
    else:
        print("Invalid option. Defaulting to Track Name sorting in ascending order.")
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['name'], reverse=False)
    return sorted_tracks

def replace_playlist_tracks(sp, playlist_id, sorted_tracks):
    track_uris = [track['track']['uri'] for track in sorted_tracks]

    # Spotify API allows a maximum of 100 tracks to be added/replaced per request
    max_tracks_per_request = 100

    # Clear the playlist first before adding sorted tracks back
    sp.playlist_replace_items(playlist_id, track_uris[:max_tracks_per_request])

    # If more than 100 tracks, add the rest in batches
    if len(track_uris) > max_tracks_per_request:
        for start_index in range(max_tracks_per_request, len(track_uris), max_tracks_per_request):
            batch = track_uris[start_index:start_index + max_tracks_per_request]
            sp.playlist_add_items(playlist_id, batch)

    print(f"Playlist {playlist_id} has been updated with sorted tracks.")

if __name__ == "__main__":
    sp = authenticate_spotify()
    user_id = sp.current_user()['id']
    playlist_name = input("Enter the playlist name: ")
    playlist_id = input("Enter the playlist ID (if you know it, otherwise leave blank): ")

    if not playlist_id:
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                playlist_id = playlist['id']
                break

    if playlist_id:
        print("Choose a sorting option:")
        print("1: Track Name\n2: Artist Name\n3: Album Name\n4: Release Date\n5: Track Duration\n6: Popularity")
        sort_option = input("Enter the number of your chosen sorting option: ")

        print("Choose sorting order:")
        print("1: Ascending\n2: Descending")
        sort_order = input("Enter the number of your chosen sorting order: ")

        tracks = get_playlist_tracks(sp, playlist_id)
        sorted_tracks = sort_tracks(tracks, sort_option, sort_order)
        replace_playlist_tracks(sp, playlist_id, sorted_tracks)
    else:
        print("Playlist not found.")
