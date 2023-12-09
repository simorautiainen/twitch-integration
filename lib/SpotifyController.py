import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
import time

class SpotifyController:
    def __init__(self, client_id, client_secret, scope='user-read-playback-state user-modify-playback-state user-read-currently-playing'):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8080", scope=scope))

    def add_to_queue(self, link):
        """Adds a song to the Spotify queue using a link."""
        logging.info(f'Adding new song to Spotify queue: {link}')
        try:
            info = self.spotify.track(link)
            self.spotify.add_to_queue(link)
            return info['name'] + ' - ' + ', '.join([art['name'] for art in info['artists']])
        except Exception as e:
            logging.error(f"Link was not legit dude: {e}")
            return ""

    def get_first_search_result(self, search_query):
        """Searches for a song and returns the first result."""
        logging.info(f'Searching for a song: {search_query}')
        try:
            data = self.spotify.search(search_query, limit=1, type='track')
            track = data["tracks"]["items"][0]  # First track from search result
            return track
        except Exception as e:
            logging.error(f"Not a valid search: {e}")
            return None

    def pause_playback(self):
        """Pauses the current playback."""
        try:
            self.spotify.pause_playback()
        except Exception as e:
            logging.error(f"Error pausing playback: {e}")

    def start_playback(self):
        """Starts or resumes playback."""
        try:
            self.spotify.start_playback()
        except Exception as e:
            logging.error(f"Error starting playback: {e}")
    def skip_song(self):
        """Skips song"""
        try:
            self.spotify.next_track()
        except Exception as e:
            logging.error(f"Error starting playback: {e}")
            
    def get_track_info(self, link):
        """Skips song"""
        try:
            return self.spotify.track(link)
        except:
            return None
