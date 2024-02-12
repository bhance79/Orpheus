# Remove duplicates within same playlist

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Function to authenticate with Spotify using OAuth2
def authenticate_spotify():
    # Initialize the Spotify client with user credentials for access
    # Requires setting environment variables for client ID and secret
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),  # Fetches the client ID from environment variables
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),  # Fetches the client secret from environment variables
        redirect_uri='http://127.0.0.1:5000',  # Redirect URI for the OAuth flow, must match the app settings on Spotify Developer Dashboard
        scope="playlist-modify-private,playlist-read-private"))  # Scopes define the permissions the app will have
    return sp

# Function to retrieve all tracks from a specified playlist, considering Spotify's pagination
def get_playlist_tracks(sp, playlist_id):
    tracks = []  # List to hold all tracks from the playlist
    results = sp.playlist_tracks(playlist_id)  # Initial API call to fetch tracks from the playlist
    while results:  # Loop to handle pagination, runs as long as 'results' contains data
        tracks.extend(results['items'])  # Adds the current batch of tracks to the 'tracks' list
        results = sp.next(results)  # Fetches the next batch of tracks, if any
    return tracks  # Returns the complete list of tracks from the playlist

# Function to identify and remove exact duplicates in a playlist based on track URIs
def remove_duplicates_by_uri(sp, playlist_id, tracks):
    seen_uris = set()  # Set to store unique URIs
    duplicates_uris = []  # List to store URIs of duplicate tracks

    for item in tracks:  # Loop through each track in the playlist
        uri = item['track']['uri']  # Extract the URI of the track
        if uri in seen_uris:  # Check if the URI has already been seen
            duplicates_uris.append(uri)  # If so, it's a duplicate, add to the list for removal
        else:
            seen_uris.add(uri)  # Otherwise, add the URI to the set of seen URIs

    # Remove the identified duplicate tracks from the playlist
    if duplicates_uris:
        for uri in duplicates_uris:
            sp.playlist_remove_all_occurrences_of_items(playlist_id, [uri])  # Remove all occurrences of each duplicate URI
        print(f"Removed {len(duplicates_uris)} exact duplicates by URI.")
    else:
        print("No exact duplicates found.")

# Function to identify and remove "true duplicates" based on track title and primary artist name
def remove_true_duplicates(sp, playlist_id, tracks):
    seen_tracks = set()  # Set to store unique track-artist combinations
    duplicates = []  # List to store IDs of duplicate tracks

    for item in tracks:  # Loop through each track in the playlist
        track = item['track']
        track_key = (track['name'], track['artists'][0]['name'])  # Create a unique key based on track name and primary artist

        if track_key in seen_tracks:  # Check if this track-artist combination has already been seen
            duplicates.append(track['id'])  # If so, it's a true duplicate, add to the list for removal
        else:
            seen_tracks.add(track_key)  # Otherwise, add the combination to the set of seen track-artist combinations

    # Remove the identified "true duplicates" from the playlist
    if duplicates:
        for track_id in duplicates:
            sp.playlist_remove_all_occurrences_of_items(playlist_id, [track_id])  # Remove all occurrences of each duplicate track ID
        print(f"Removed {len(duplicates)} true duplicates considering track name and artist.")
    else:
        print("No true duplicates found after URI check.")

# Main execution block
if __name__ == "__main__":
    sp = authenticate_spotify()  # Authenticate with Spotify to get a Spotipy client instance
    playlist_name = input("Enter the playlist name: ")  # Prompt the user to enter the name of the playlist to clean

    # Find the playlist by name among the user's playlists
    playlists = sp.current_user_playlists()
    playlist_id = None
    for playlist in playlists['items']:
        if playlist['name'].lower() == playlist_name.lower():  # Case-insensitive comparison
            playlist_id = playlist['id']  # Store the ID of the matched playlist
            break

    # Proceed if the specified playlist was found
    if playlist_id:
        tracks = get_playlist_tracks(sp, playlist_id)  # Retrieve all tracks from the specified playlist
        remove_duplicates_by_uri(sp, playlist_id, tracks)  # Remove exact duplicates based on URI
        updated_tracks = get_playlist_tracks(sp, playlist_id)  # Fetch tracks again as the playlist may have been modified
        remove_true_duplicates(sp, playlist_id, updated_tracks)  # Remove "true duplicates" based on track name and artist
    else:
        print("Playlist not found.")  # Inform the user if the specified playlist was not found
