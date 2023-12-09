import requests
from random import randint
import json
import time
import asyncio

class SiiliCameraController:
    def __init__(self):
        self.base_url = 'http://127.0.0.1:6042'
        self.session = requests.Session()

    def get_siili_cameras(self):
        """Fetches information about available OBS sources and their selected NDI sources."""
        try:
            response = self.session.get(f'{self.base_url}/getSources')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching SiiliCameras: {e}")
            return None

    def set_camera_source(self, camera_name, ndi_source):
        """Sets an NDI source for an existing OBS source."""
        try:
            payload = {
                'obs_source_name': camera_name,
                'ndi_source': ndi_source
            }
            response = self.session.post(f'{self.base_url}/setNDISource', json=payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error setting camera source: {e}")
            return None

    def stop(self):
        self.session.close()
        
async def set_random_ndi_source(matcher: str = "twitch"):
    
    controller = SiiliCameraController()
    
    start_ms = int(time.time()*1000)
    for i in range(10):
        
        start_loop = int(time.time()*1000)
        # switch twitch camera named source to a random
        cameras = controller.get_siili_cameras()
        for camera in cameras["sources"]:
                if matcher in camera["obs_source_name"].lower():
                    camera_info_to_edit = camera
                    break
        else:
            print(f"no siilicam obs sources with name '{matcher}' in it")
            return
        current_camera = camera_info_to_edit['selected_ndi_source']
        
        other_cameras = list(filter(lambda x: x!=current_camera, cameras['available_ndi_sources']))
        if len(other_cameras) == 0:
            print("no other cameras than the selected one")
            return
        
        random_camera_index = randint(0, len(other_cameras)-1)
        random_camera = other_cameras[random_camera_index]
        controller.set_camera_source(camera_info_to_edit['obs_source_name'], random_camera)
        
        time.sleep(0.4)
        end_loop = int(time.time()*1000)
        print(f"\tit took for one request {end_loop-start_loop} ms")
    
    
    print(f"end it took in total with 400ms sleeps {end_loop-start_ms} ms")
if __name__ == "__main__":
    asyncio.run(set_random_ndi_source())
