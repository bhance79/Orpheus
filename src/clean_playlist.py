# Remove tracks from source playlist if already exists in other playlist(s)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Function to authenticate with Spotify using OAuth
def authenticate_spotify():
    # Initializes the Spotify client with user credentials
    # Requires setting environment variables for client ID, secret, and a redirect URI
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),  # Fetches the client ID from environment variables
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),  # Fetches the client secret from environment variables
        redirect_uri='http://127.0.0.1:5000',  # The redirect URI where Spotify will send the authorization code
        scope="playlist-modify-private,playlist-read-private"))  # Scopes define the permissions the app will have
    return sp

# Function to retrieve all tracks from a specified playlist, handling Spotify's pagination
def get_playlist_tracks(sp, playlist_id):
    tracks = []  # List to hold all tracks from the playlist
    results = sp.playlist_tracks(playlist_id)  # Initial API call to fetch tracks from the playlist
    while results:  # Loop to handle pagination, runs as long as 'results' contains data
        tracks.extend(results['items'])  # Adds the current batch of tracks to the 'tracks' list
        results = sp.next(results)  # Fetches the next batch of tracks, if any
    return tracks  # Returns the complete list of tracks from the playlist

# Function to find duplicates based on track name and primary artist in specified playlists
def find_duplicates_in_playlists(sp, source_playlist_tracks_info, playlist_names):
    user_id = sp.current_user()['id']  # Retrieves the current user's Spotify ID
    playlists = sp.user_playlists(user_id)  # Fetches playlists for the current user
    duplicate_tracks_info = set()  # Set to store unique track-artist combinations found as duplicates

    for playlist in playlists['items']:
        if playlist['name'] in playlist_names:  # Checks if the playlist is one of the specified playlists to check against
            playlist_tracks = get_playlist_tracks(sp, playlist['id'])  # Retrieves tracks from the playlist
            for track in playlist_tracks:
                # Creates a tuple of track name and primary artist's name as a unique identifier
                track_info = (track['track']['name'], track['track']['artists'][0]['name'])
                if track_info in source_playlist_tracks_info:  # Checks if this unique identifier is in the source playlist
                    duplicate_tracks_info.add(track_info)  # Adds the identifier to the set of duplicates

    return duplicate_tracks_info  # Returns the set of unique track-artist combinations found as duplicates

# Function to remove tracks in batches from a playlist, adhering to Spotify's API limits
def batch_remove_tracks(sp, playlist_id, tracks_to_remove):
    max_tracks_per_request = 100  # Spotify's limit for the number of tracks that can be removed in a single request
    # Loops through the list of tracks to remove, processing in batches of up to 100
    for i in range(0, len(tracks_to_remove), max_tracks_per_request):
        batch = tracks_to_remove[i:i + max_tracks_per_request]  # Creates a batch of tracks to remove
        sp.playlist_remove_all_occurrences_of_items(playlist_id, batch)  # Removes the batch of tracks from the playlist

if __name__ == "__main__":
    sp = authenticate_spotify()  # Authenticates with Spotify to get a Spotipy client instance

    # User input for the source playlist and other playlists to check for duplicates
    source_playlist_name = input("Enter the name of the source playlist: ")
    playlist_names = input("Enter the names of playlists to check, separated by a comma: ").split(',')

    # Find the source playlist by name among the user's playlists
    source_playlist_id = None
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'].lower() == source_playlist_name.lower():  # Case-insensitive comparison to find the source playlist
            source_playlist_id = playlist['id']  # Stores the ID of the source playlist
            break

    if source_playlist_id:
        source_playlist_tracks = get_playlist_tracks(sp, source_playlist_id)  # Retrieves tracks from the source playlist
        # Creates a set of tuples with track name and primary artist for each track in the source playlist
        source_playlist_tracks_info = {(track['track']['name'], track['track']['artists'][0]['name']) for track in source_playlist_tracks}

        duplicates = find_duplicates_in_playlists(sp, source_playlist_tracks_info, playlist_names)  # Finds duplicates across specified playlists

        if duplicates:
            tracks_to_remove = [track['track']['uri'] for track in source_playlist_tracks if (track['track']['name'], track['track']['artists'][0]['name']) in duplicates]
            batch_remove_tracks(sp, source_playlist_id, tracks_to_remove)  # Removes identified duplicates from the source playlist in batches
            print(f"Removed {len(tracks_to_remove)} tracks from {source_playlist_name}.")
        else:
            print("No duplicates found.")  # Informs the user if no duplicates were found
    else:
        print(f"Playlist '{source_playlist_name}' not found.")  # Informs the user if the source playlist was not found
