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
```
All of those currently must be filled

`CHANNEL` should be your channel, so the channel which the chatbot joins and
which the reward logic asks for permissions

