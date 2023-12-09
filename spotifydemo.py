from lib import SpotifyController, get_spotify_client_info
import time

def main():
    id, secret = get_spotify_client_info()
    controller = SpotifyController(id, secret)
    controller.pause_playback()
    time.sleep(1)
    controller.start_playback()
    result= controller.get_first_search_result("villieläin")
    print(result)
    if result:
        controller.add_to_queue(result["uri"])
        controller.skip_song()
        
if __name__ == "__main__":
    main()