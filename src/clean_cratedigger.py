# Cleans CRATEDIGGER of any songs already saved
# this script in specific is tailor made for my personal playlists

# Use clean_playlist to use this script with your playlists

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Authenticate with Spotify using OAuth
def authenticate_spotify():
    # Initializes the Spotify client with user credentials for access
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

# Function to find duplicates based on track IDs in specified playlists
def find_duplicates_in_playlists(sp, cratedigger_tracks, playlist_names):
    user_id = sp.current_user()['id']  # Retrieves the current user's Spotify ID
    playlists = sp.user_playlists(user_id)  # Fetches playlists for the current user
    duplicate_tracks = []  # List to store track IDs found in both CRATEDIGGER and other playlists

    for playlist in playlists['items']:
        if playlist['name'] in playlist_names:  # Checks if the playlist is one of the specified playlists
            playlist_tracks = get_playlist_tracks(sp, playlist['id'])  # Retrieves tracks from the playlist
            for track in playlist_tracks:
                if track['track']['id'] in cratedigger_tracks:  # Checks if the track is in CRATEDIGGER
                    duplicate_tracks.append(track['track']['id'])  # Adds the track ID to the list of duplicates

    return set(duplicate_tracks)  # Returns a set of unique track IDs found as duplicates

if __name__ == "__main__":
    sp = authenticate_spotify()  # Authenticates with Spotify to get a Spotipy client instance

    # Directly define the playlists to check against CRATEDIGGER for duplicates
    playlist_names = ['Airborne', 'Boost', 'Chill']
    cratedigger_id = None  # Initialize the CRATEDIGGER playlist ID

    # Find CRATEDIGGER playlist by name among the user's playlists
    playlists = sp.current_user_playlists()
    for playlist in playlists['items']:
        if playlist['name'] == 'CRATEDIGGER':  # Checks for a playlist named CRATEDIGGER
            cratedigger_id = playlist['id']  # Stores the ID of CRATEDIGGER
            break

    if not cratedigger_id:
        print("CRATEDIGGER playlist not found.")  # Informs the user if CRATEDIGGER is not found
    else:
        # Retrieves tracks from CRATEDIGGER and checks for duplicates in the specified playlists
        cratedigger_tracks = [track['track']['id'] for track in get_playlist_tracks(sp, cratedigger_id)]
        duplicates = find_duplicates_in_playlists(sp, cratedigger_tracks, playlist_names)

        if duplicates:
            # Removes duplicate tracks from CRATEDIGGER
            for track_id in duplicates:
                sp.playlist_remove_all_occurrences_of_items(cratedigger_id, [track_id])
            print(f"Removed {len(duplicates)} duplicates from CRATEDIGGER.")
        else:
            print("No duplicates found.")  # Informs the user if no duplicates were found
