import requests
import math

class HueController:
    def __init__(self, id, ip):
        self.id = id
        self.hue_ip = ip
        self.base_url = f"https://{self.hue_ip}"
        self.groups = self.get_groups()
        self.scenes = self.get_scenes()

    def trigger_scene(self, group, scene_id):
        requests.put(f"{self.base_url}/api/{self.id}/groups/{group}/action", json={"scene":scene_id}, verify=False)
    
    def group_name_to_id(self, group_name: str):
        for key, value in self.groups.items():
            if value["name"] == group_name:
                return key
        
        return -1
    def scene_name_to_id(self, scene_name: str):
        for key, value in self.groups.items():
            if value["name"] == scene_name:
                return key
        
        return -1
    def get_lights(self):
        return requests.get(f"{self.base_url}/api/{self.id}/lights", verify=False).json()

    def get_groups(self):
        return requests.get(f"{self.base_url}/api/{self.id}/groups", verify=False).json()
    def get_scenes(self):
        return requests.get(f"{self.base_url}/api/{self.id}/scenes", verify=False).json()

    def get_group(self, group_id):
        return requests.get(f"{self.base_url}/api/{self.id}/groups/{group_id}", verify=False).json()

    def edit_light(self, light_id, conf):
        requests.put(f"{self.base_url}/api/{self.id}/lights/{light_id}/state", json=conf, verify=False)

    def edit_group(self, group_id, conf):
        requests.put(f"{self.base_url}/api/{self.id}/groups/{group_id}/action", json=conf, verify=False)

    def enchance_color(self, normalized):
        if normalized > 0.04045:
            return math.pow( (normalized + 0.055) / (1.0 + 0.055), 2.4)
        else:
            return normalized / 12.92

    def RGB_to_XY(self, r, g, b):
        rNorm = r / 255.0
        gNorm = g / 255.0
        bNorm = b / 255.0

        rFinal = self.enchance_color(rNorm)
        gFinal = self.enchance_color(gNorm)
        bFinal = self.enchance_color(bNorm)
        
        X = rFinal * 0.649926 + gFinal * 0.103455 + bFinal * 0.197109
        Y = rFinal * 0.234327 + gFinal * 0.743075 + bFinal * 0.022598
        Z = rFinal * 0.000000 + gFinal * 0.053077 + bFinal * 1.035763

        if X + Y + Z == 0:
            return (0,0)
        else:
            xFinal = X / (X + Y + Z)
            yFinal = Y / (X + Y + Z)
    
        return (xFinal, yFinal)