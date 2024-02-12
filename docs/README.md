# Orpheus Project

The Orpheus project offers a suite of Python scripts designed to enhance your Spotify experience by facilitating advanced playlist management. Whether you're looking to remove duplicates, sort tracks by specific attributes, or maintain playlist uniqueness, these tools can help streamline your music library.

## Features

- **Clean Playlist**: The `clean_playlist.py` script allows you to remove tracks from a chosen playlist that already exist in other specified playlists, ensuring each playlist remains unique.
- **CRATEDIGGER Creation**: The `cratedigger.py` script automatically creates a "CRATEDIGGER" playlist, filling it with tracks from Spotify's "Discovery Weekly". This ensures you always have a fresh playlist of new music to explore.
- **Duplicate Removal**: With the `remove_duplicates.py` and `true_duplicates.py` scripts, you can efficiently identify and remove duplicate tracks within a playlist, based on either Spotify URIs or a combination of track names and artist names.
- **Playlist Sorting**: The `sort.py` script offers the ability to sort playlists based on various musical attributes, such as Danceability, Energy, Valence, Tempo, Loudness, and Acousticness, allowing you to set the perfect mood for any occasion.

## Installation

1. **Prerequisites**:
    - Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
    - Install the Spotipy library, a lightweight Python library for the Spotify Web API. You can install it using pip:
        ```sh
        pip install spotipy
        ```

2. **Spotify API Credentials**:
    - Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) to create an app and obtain your `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`.
    - Set the redirect URI in your app settings to `http://127.0.0.1:5000` or whichever URL you desire and save it.
    - Store your Spotify API credentials as environment variables:
        - On Windows:
            ```cmd
            set SPOTIFY_CLIENT_ID=your_client_id_here
            set SPOTIFY_CLIENT_SECRET=your_client_secret_here
            set SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000
            ```
        - On Unix/Linux/macOS:
            ```sh
            export SPOTIFY_CLIENT_ID=your_client_id_here
            export SPOTIFY_CLIENT_SECRET=your_client_secret_here
            export SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000
            ```

3. **Download and Run Scripts**:
    - Clone this repository or download the source code.
    - Navigate to the `src` directory within the downloaded repository.
    - Run any of the provided scripts using Python. For example:
        ```sh
        python sort.py
        ```

## Usage

Each script is interactive and will prompt you for any required information, such as playlist names or sorting preferences. Simply run the script, and follow the prompts to manage your Spotify playlists.

## Contributing

Contributions to the Orpheus project are welcome! Feel free to fork the repository, make your changes, and submit a pull request with your improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
