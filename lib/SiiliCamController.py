import requests
from random import randint

class SiiliCameraController:
    def __init__(self):
        self.base_url = 'http://localhost:6042'

    def get_siili_cameras(self):
        """Fetches information about available OBS sources and their selected NDI sources."""
        try:
            response = requests.get(f'{self.base_url}/getSources', stream=True)
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
            response = requests.post(f'{self.base_url}/setNDISource', json=payload, stream=True)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error setting camera source: {e}")
            return None
    

def set_random_ndi_source(matcher: str = "twitch"):
    
    controller = SiiliCameraController()
    cameras = controller.get_siili_cameras()
    print(cameras)


    # switch twitch camera named source to a random
    for camera in cameras["sources"]:
        if matcher in camera["obs_source_name"].lower():
            camera_info_to_edit = camera
            break
    else:
        print(f"no siilicam obs sources with name '{matcher}' in it")
        return
    
    other_cameras = cameras['available_ndi_sources']
    if len(other_cameras) == 0:
        print("no other cameras than the selected one")
        return
    
    random_camera_index = randint(0, len(other_cameras)-1)
    random_camera = other_cameras[random_camera_index]
    controller.set_camera_source(camera_info_to_edit['obs_source_name'], random_camera)

if __name__ == "__main__":
    set_random_ndi_source()