from lib import ChatBot, EventListener, SiiliCameraController, config, SpotifyController, Redemption, HueController
import asyncio
from random import randint
# lets run our setup


class TwitchServerHandler:
    def __init__(self, hue_enabled: bool = True):
        client_id, client_secret = config.get_client_info()
        spotify_client_id, spotify_client_secret = config.get_spotify_client_info()
        self.channel = config.get_channel()
        self.siilicam_source_name = config.get_siilicam_obs_source_name()
        self.reward_listener = EventListener(client_id, client_secret, self.channel)
        self.chat_bot = ChatBot(client_id, client_secret, self.channel)
        self.spotify_controller = SpotifyController(spotify_client_id, spotify_client_secret)
        self.siilicam_controller: SiiliCameraController = SiiliCameraController()
        self.stop_event = asyncio.Event()
        self.hue_enabled = hue_enabled
        if hue_enabled:
            hue_id, hue_ip = config.get_hue_env()
            self.hue_controller = HueController(hue_id, hue_ip)
            self.hue_config = config.get_hue_config()
    async def init_everything(self, dev=False):
        if dev:
            access_token, refresh_token = config.get_twitch_dev_tokens()
            await self.reward_listener.authenticate_token(access_token, refresh_token)
            await self.reward_listener.init()
        else:
            await self.reward_listener.run()
        await self.chat_bot.run()
        self.rewards = await self.reward_listener.getRewards()
        
        # this controls what event listeners do what
        await self.reward_listener.add_reward_callback(self.rewards["SiiliCam"], self.set_random_camera)
        await self.reward_listener.add_reward_callback(self.rewards["Song request"], self.song_request_callback)
        if self.hue_enabled:
            for reward_name, reward_id in self.rewards:
                if reward_name in self.hue_config["rewardsToScenes"].keys():
                    await self.reward_listener.add_reward_callback(self.rewards[reward_name], self.turn_on_scene)
            await self.reward_listener.add_reward_callback(self.rewards["Valot päälle/pois"], self.toggle_lights_callback)
            await self.reward_listener.add_reward_callback(self.rewards["Discovalot"], self.hue_random_colors)

    def add_to_que(self, link):
        print(f"adding new song to spotify que {link}")
        try:

            info = self.spotify_controller.get_track_info(link)
            self.spotify_controller.add_to_queue(link)
            return info['name'] + ' - ' + ', '.join([art['name'] for art in info['artists']])
        except:
            print("Link was not legit dude")
        return None
    async def song_request_callback(self, event: Redemption):
        username = event.event.user_name
        user_input = event.event.user_input
        print(f"SONG REQUEST: user {username} input {user_input}")
        info = self.spotify_controller.get_track_info(user_input)
        if info == None:
            # lets try by searching
            track = self.spotify_controller.get_first_search_result(user_input)
            if track == None:
                await self.chat_bot.send_message("Ei onnistuttu laittaa queen, kiitti pisteistä")
                return
            info = track
        try:
            self.spotify_controller.add_to_queue(info["uri"])
            message = info['name'] + ' - ' + ', '.join([art['name'] for art in info['artists']])
            await self.chat_bot.send_message(f"Queen sujahti: {message}")
        except:
            await self.chat_bot.send_message("Ei onnistuttu laittaa queen vaikka löydettiin se pelikentiltä")
        
    
    # very complex but this switch betweens cameras that are not in use
    async def set_random_camera(self, event: Redemption):
        print(f"user {event.event.user_name} asked for random camera")
        cameras = self.siilicam_controller.get_siili_cameras()
        print(cameras)
        camera_to_edit = None
        cameras_in_use = set()
        for camera in cameras["sources"]:
            
            if self.siilicam_source_name.lower() == camera["obs_source_name"].lower():
                camera_to_edit = camera["obs_source_name"]
            cameras_in_use.add(camera["selected_ndi_source"])
        if camera_to_edit == None:
            print(f"{self.siilicam_source_name} obs source not available")
            return

        free_cameras =list(filter(lambda x: not x in cameras_in_use, cameras["available_ndi_sources"]))
        if len(free_cameras) < 1:
            print("no free cameras to pick random from")
            return
        
        cameras_to_switch_index = randint(0, len(free_cameras)-1)
        camera_to_switch = free_cameras[cameras_to_switch_index]
        self.siilicam_controller.set_camera_source(camera_to_edit, camera_to_switch)
        await self.chat_bot.send_message("Kamera vaihdettu :3")

    def toggle_lights_callback(self, event: Redemption):
        group_name = self.hue_config["groupName"]
        group_id = self.hue_controller.group_name_to_id(group_name)
        group = self.hue_controller.get_group(group_id)
        status = group["state"]["all_on"]
        print(f"light status: {status}")
        if status:
            new_conf = {"on": False}
            self.hue_controller.edit_group(group_id, new_conf)
        else:
            new_conf = {"on": True}
            self.hue_controller.edit_group(group_id, new_conf)
            
    def turn_on_scene(self, event: Redemption):
        group_name = self.hue_config["groupName"]
        group_id = self.hue_controller.group_name_to_id(group_name)
        reward_name = event.event.reward.title
        scene_name = self.hue_config["rewardsToScenes"][reward_name]
        scene_id = self.hue_controller.scene_name_to_id(scene_name)
        self.hue_controller.trigger_scene(group_id, scene_id)
        
    def hue_random_colors(self, event: Redemption):
        hue_color_conf = [{"bri": 254, "sat": 0, "alert": "lselect"}]
        lights = self.hue_controller.get_lights()
        for light in lights:
            if randint(0,10) == 0:
                hue_color_conf = {"bri": 254, "sat": 254, "alert": "lselect", "on": True}
            else:  
                color = self.hue_random_color()
                hue_color_conf = {"bri": 254,"xy":color, "sat": 0, "alert": "lselect", "on": True}

            self.hue_controller.edit_light(light, hue_color_conf)
            
        # set default scene after lightshow
        group_name = self.hue_config["groupName"]
        group_id = self.hue_controller.group_name_to_id(group_name)
        scene_name = self.hue_config["defaultScene"]
        scene_id = self.hue_controller.scene_name_to_id(scene_name)
        self.hue_controller.trigger_scene(group_id, scene_id)
        
    async def stop(self):
        await self.chat_bot.stop()
        await self.reward_listener.stop()
        self.siilicam_controller.stop()
        self.stop_event.set()
    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.stop()
    
        
async def user_input_task(server):
    input("Press Enter to stop...\n")
    await server.stop()
    
async def main():
    server = TwitchServerHandler()

    await server.init_everything()
    asyncio.create_task(user_input_task(server))
    await server.stop_event.wait()


    
if __name__ == "__main__":
    
    asyncio.run(main())