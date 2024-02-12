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

def find_playlist_by_name(sp, user_id, playlist_name):
    playlists = sp.user_playlists(user_id)
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

def get_audio_features(sp, tracks):
    track_ids = [track['track']['id'] for track in tracks if track['track']['id'] is not None]
    features_list = []
    for i in range(0, len(track_ids), 100):  # Spotify limits batch size to 100
        batch_ids = track_ids[i:i+100]
        features_list.extend(sp.audio_features(batch_ids))
    return features_list

def sort_tracks_by_feature(tracks, features, sort_feature, sort_order):
    reverse_order = True if sort_order == '2' else False
    track_features = {feature['id']: feature for feature in features}
    sorted_tracks = sorted(tracks, key=lambda x: track_features[x['track']['id']][sort_feature], reverse=reverse_order)
    return sorted_tracks

def replace_playlist_tracks(sp, playlist_id, sorted_tracks):
    track_uris = [track['track']['uri'] for track in sorted_tracks]
    max_tracks_per_request = 100
    sp.playlist_replace_items(playlist_id, track_uris[:max_tracks_per_request])
    if len(track_uris) > max_tracks_per_request:
        for start_index in range(max_tracks_per_request, len(track_uris), max_tracks_per_request):
            batch = track_uris[start_index:start_index + max_tracks_per_request]
            sp.playlist_add_items(playlist_id, batch)
    print(f"Playlist {playlist_id} has been updated with tracks sorted by audio features.")

if __name__ == "__main__":
    sp = authenticate_spotify()
    user_id = sp.current_user()['id']
    playlist_name = input("Enter the playlist name: ")
    playlist_id = find_playlist_by_name(sp, user_id, playlist_name)

    if playlist_id:
        print("Choose an audio feature to sort by:")
        print("1: Danceability\n2: Energy\n3: Valence\n4: Tempo\n5: Loudness\n6: Acousticness")
        feature_option = input("Enter the number of your chosen feature: ")
        feature_map = {'1': 'danceability', '2': 'energy', '3': 'valence', '4': 'tempo', '5': 'loudness', '6': 'acousticness'}
        sort_feature = feature_map.get(feature_option, 'danceability')

        print("Choose sorting order:")
        print("1: Ascending\n2: Descending")
        sort_order = input("Enter the number of your chosen sorting order: ")

        tracks = get_playlist_tracks(sp, playlist_id)
        features = get_audio_features(sp, tracks)
        sorted_tracks = sort_tracks_by_feature(tracks, features, sort_feature, sort_order)
        replace_playlist_tracks(sp, playlist_id, sorted_tracks)
    else:
        print("Playlist not found. Please check the name and try again.")
