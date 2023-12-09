from dotenv import dotenv_values
import json
import os

config = dotenv_values(".env")
  
def get_client_info():

  client_id = config["CLIENT_ID"]
  client_secret = config["CLIENT_SECRET"]
  return client_id, client_secret

def get_channel():

  channel = config["CHANNEL"]
  return channel

def get_spotify_client_info():
  client_id = config["SPOTIFY_CLIENT_ID"]
  client_secret = config["SPOTIFY_CLIENT_SECRET"]
  return client_id, client_secret

def get_siilicam_obs_source_name():

  source_name = config["SIILICAM_OBS_SOURCE_NAME"]
  return source_name

def get_twitch_dev_tokens():

  access_token = config["TWITCH_DEV_ACCESS_TOKEN"]
  refresh_token = config["TWITCH_DEV_REFRESH_TOKEN"]
  return access_token,refresh_token

def get_twitch_dev_tokens():

  access_token = config["TWITCH_DEV_ACCESS_TOKEN"]
  refresh_token = config["TWITCH_DEV_REFRESH_TOKEN"]
  return access_token,refresh_token

def get_hue_env():

  id = config["HUE_IP"]
  ip = config["HUE_ID"]
  return id, ip

def get_hue_config():
  config_dir = os.path.dirname(os.path.abspath(__file__))
  hue_config_path = os.path.join(config_dir, '..', 'hue_config.json')
  try:
    with open(hue_config_path, 'r') as config_file:
      return json.load(config_file)
  except:
    print("could not open hue file")
  return None

if __name__ == "__main__":
  client_id, client_secret = get_client_info()
  spotify_client_id, spotify_client_secret = get_spotify_client_info()
  channel = get_channel()
  print(f"{client_id = }, {client_secret = } {channel = } {spotify_client_id = } {spotify_client_secret = }")
  print(get_hue_config())