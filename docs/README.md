# Orpheus

Orpheus is a Python project focused on Spotify playlist management, featuring scripts to clean playlists by removing duplicates (`clean.py`) and manage a specific playlist (`cratedigger.py`).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.x
- A Spotify Developer account and the necessary credentials (Client ID, Client Secret, and a Redirect URI)

### Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/bhance79/Orpheus.git
   ```
2. Navigate to the project directory:
   ```
   cd Orpheus
   ```
3. (Optional) If you're using a virtual environment, activate it. If not, skip this step.
   ```
   source env/bin/activate  # For Unix/Linux/Mac
   env\Scripts\activate  # For Windows
   ```
4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage

#### Cleaning Playlists

To clean a playlist by removing duplicate tracks, run the `clean.py` script:

```
python clean.py
```

Follow the prompts to enter the playlist name you wish to clean.

#### Managing Cratedigger Playlist

To manage the Cratedigger playlist, run the `cratedigger.py` script:

```
python cratedigger.py
```

Follow the instructions provided by the script.



## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/<your-github-username>/Orpheus/LICENSE.md) file for details.

## Acknowledgments

- Spotify for the Web API and the opportunity to create something cool.
