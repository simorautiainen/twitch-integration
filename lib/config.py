from dotenv import dotenv_values

def get_client_info():
  config = dotenv_values(".env")

  client_id = config["CLIENT_ID"]
  client_secret = config["CLIENT_SECRET"]
  return client_id, client_secret

def get_channel():
  config = dotenv_values(".env")

  channel = config["CHANNEL"]
  return channel

def get_spotify_client_info():
  config = dotenv_values(".env")

  client_id = config["SPOTIFY_CLIENT_ID"]
  client_secret = config["SPOTIFY_CLIENT_SECRET"]
  return client_id, client_secret

def get_siilicam_obs_source_name():
  config = dotenv_values(".env")

  source_name = config["SIILICAM_OBS_SOURCE_NAME"]
  return source_name

def get_twitch_dev_tokens():
  config = dotenv_values(".env")

  access_token = config["TWITCH_DEV_ACCESS_TOKEN"]
  refresh_token = config["TWITCH_DEV_REFRESH_TOKEN"]
  return access_token,refresh_token

if __name__ == "__main__":
  client_id, client_secret = get_client_info()
  spotify_client_id, spotify_client_secret = get_spotify_client_info()
  channel = get_channel()
  print(f"{client_id = }, {client_secret = } {channel = } {spotify_client_id = } {spotify_client_secret = }")