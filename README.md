# Twitch integrations

Create a copy of the .envexample file and name it .env and you can start filling the
missing information. This readme acts as a guide what to fill and how

## Twitch setup

This whole project makes an assumption that you are not using **firefox** as your
main browser. **Firefox** is used when you login with your bot account

1. Go to twitch and create new account, remember the password bec
2. Go to your main application and register a application on the twitch developer console
    1. Redirect url as `http://localhost:17563` its some twitchAPI specific
    2. copy the client id and secret to your .env file in `CLIENT_ID` and `CLIENT_SECRET`


## Spotify setup

1. Go to spotify developer dashboard and create new app
2. set redirect URI as `http://localhost:8080`
3. Copy the client id and secret of the created app to the `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET`

## ENV

```
CLIENT_ID
CLIENT_SECRET
CHANNEL
SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET
TWITCH_DEV_ACCESS_TOKEN
TWITCH_DEV_REFRESH_TOKEN
HUE_IP
HUE_ID
```
All of those currently must be filled

`CHANNEL` should be your channel, so the channel which the chatbot joins and
which the reward logic asks for permissions

`TWITCH_DEV_ACCESS_TOKEN` and `TWITCH_DEV_REFRESH_TOKEN` are for development and explained how they are below

## To get friends token

1. go to https://twitchtokengenerator.com/
2. fill the client secret and client id.
3. For the copes they are defined in [EventListener](lib/EventListener.py#L<13>) and select yes to all
4. In [TwitchServer](twitchserver.py#L<105>) set the dev=true so it uses the twitch dev access token and refresh token
instead of oauth tokens

## HUE

there is a tutorial here https://developers.meethue.com/develop/get-started-2/ so first send the
```json
{"devicetype":"my_hue_app#iphone peter"}
```
And then go press a button physically on the bridge and then in the user id / token will appear in the command response. `HUE_ID` is the response in the username field. `HUE_IP` is the ip
where the bridges server is in your local network.
