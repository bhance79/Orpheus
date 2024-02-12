import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Authenticate with Spotify using OAuth
def authenticate_spotify():
    # Initializes the Spotipy client with user credentials
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),  # Your Spotify app's client ID - from Environment Variable
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),  # Your Spotify app's client secret - from Environment Variable
        redirect_uri='http://127.0.0.1:5000',  # Redirect URI set in your Spotify app
        scope="playlist-modify-private,playlist-read-private,playlist-modify-public"))  # Scopes define permissions
    return sp

# Find a playlist by name and return its Spotify ID
def find_playlist_by_name(sp, user_id, playlist_name):
    playlists = sp.user_playlists(user_id)  # Fetches playlists for the current user
    for playlist in playlists['items']:  # Iterates through the playlists
        if playlist['name'].lower() == playlist_name.lower():  # Case-insensitive comparison
            return playlist['id']  # Returns the ID of the matching playlist
    return None  # Returns None if no matching playlist is found

# Fetch all tracks from a specified playlist
def get_playlist_tracks(sp, playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)  # Initial fetch of playlist tracks
    tracks.extend(results['items'])  # Adds the first batch of tracks to the list
    while results['next']:  # Checks if there are more tracks to fetch
        results = sp.next(results)  # Fetches the next batch of tracks
        tracks.extend(results['items'])  # Adds subsequent batches of tracks to the list
    return tracks

# Fetch audio features for a list of tracks
def get_audio_features(sp, tracks, sort_feature):
    if sort_feature in ['danceability', 'energy', 'valence', 'tempo', 'loudness', 'acousticness']:
        track_ids = [track['track']['id'] for track in tracks if track['track']['id'] is not None]  # Extract track IDs
        features_list = []
        for i in range(0, len(track_ids), 100):  # Spotify limits batch size to 100
            batch_ids = track_ids[i:i+100]  # Creates batches of up to 100 track IDs
            features_list.extend(sp.audio_features(batch_ids))  # Fetches audio features for each batch
        return features_list
    return None  # Returns None if sorting by popularity (no need to fetch audio features)

# Sort tracks by the specified audio feature or popularity
def sort_tracks(tracks, features, sort_feature, sort_order):
    reverse_order = True if sort_order == '2' else False  # Determines sort order (ascending or descending)
    if features:  # Sorting based on audio features
        track_features = {feature['id']: feature for feature in features}  # Maps track IDs to their audio features
        sorted_tracks = sorted(tracks, key=lambda x: track_features[x['track']['id']][sort_feature], reverse=reverse_order)
    else:  # Sorting based on popularity
        sorted_tracks = sorted(tracks, key=lambda x: x['track']['popularity'], reverse=reverse_order)
    return sorted_tracks

# Replace the tracks in the specified playlist with the sorted list of tracks
def replace_playlist_tracks(sp, playlist_id, sorted_tracks):
    track_uris = [track['track']['uri'] for track in sorted_tracks]  # Extracts URIs of sorted tracks
    max_tracks_per_request = 100  # Spotify's limit for adding/replacing tracks per request
    sp.playlist_replace_items(playlist_id, track_uris[:max_tracks_per_request])  # Replaces the first batch of tracks
    if len(track_uris) > max_tracks_per_request:
        for start_index in range(max_tracks_per_request, len(track_uris), max_tracks_per_request):
            batch = track_uris[start_index:start_index + max_tracks_per_request]  # Creates batches of track URIs
            sp.playlist_add_items(playlist_id, batch)  # Adds remaining batches of tracks to the playlist
    print(f"Playlist {playlist_id} has been updated with tracks sorted by {sort_feature}.")

# Main execution block
if __name__ == "__main__":
    sp = authenticate_spotify()  # Authenticates and creates a Spotipy client
    user_id = sp.current_user()['id']  # Fetches the current user's Spotify ID
    playlist_name = input("Enter the playlist name: ")  # Prompts the user for a playlist name
    playlist_id = find_playlist_by_name(sp, user_id, playlist_name)  # Retrieves the playlist ID by name

    if playlist_id:
        # Prompts the user to choose an audio feature for sorting
        print("Choose a feature to sort by:")
        print("1: Danceability\n2: Energy\n3: Valence\n4: Tempo\n5: Loudness\n6: Acousticness\n7: Popularity")
        feature_option = input("Enter the number of your chosen feature: ")
        # Maps user input to corresponding audio feature
        feature_map = {
            '1': 'danceability', '2': 'energy', '3': 'valence', 
            '4': 'tempo', '5': 'loudness', '6': 'acousticness', '7': 'popularity'
        }
        sort_feature = feature_map.get(feature_option, 'popularity')  # Default to 'popularity' if input is invalid

        # Prompts the user to choose the sorting order
        print("Choose sorting order:")
        print("1: Ascending\n2: Descending")
        sort_order = input("Enter the number of your chosen sorting order: ")

        tracks = get_playlist_tracks(sp, playlist_id)  # Fetches tracks from the specified playlist
        features = None
        if sort_feature != 'popularity':  # Fetches audio features if needed
            features = get_audio_features(sp, tracks, sort_feature)
        sorted_tracks = sort_tracks(tracks, features, sort_feature, sort_order)  # Sorts the tracks
        replace_playlist_tracks(sp, playlist_id, sorted_tracks)  # Updates the playlist with sorted tracks
    else:
        print("Playlist not found. Please check the name and try again.")
