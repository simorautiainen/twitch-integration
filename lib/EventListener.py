from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first


class EventListener:
    def __init__(self, client_id, client_secret, channel_to_manage):
        self.client_id = client_id
        self.client_secret = client_secret
        self.USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.CHANNEL_MANAGE_REDEMPTIONS]
        self.eventsub = None
        self.twitch = None
        self.broadcaster_id = None
        self.channel_to_manage = channel_to_manage
    async def add_reward_callback(self, reward_id, callback):
        if not self.broadcaster_id:
            print("Error: Broadcaster ID not set. Ensure EventListener is authenticated.")
            return

        # Subscribe to channel point redemption events for the specific reward
        await self.eventsub.listen_channel_points_custom_reward_redemption_add(
            self.broadcaster_id, callback, reward_id)

    async def init(self):
        self.twitch = await Twitch(self.client_id, self.client_secret)
        auth = UserAuthenticator(self.twitch, self.USER_SCOPE)
        token, refresh_token = await auth.authenticate()

        await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)
        user = await first(self.twitch.get_users(logins=[self.channel_to_manage]))
        self.broadcaster_id = user.id
        print(f"Authenticated as broadcaster ID: {self.broadcaster_id}")

        self.eventsub = EventSubWebsocket(self.twitch)
        self.eventsub.start()
    async def run(self):
        # Starts listening for events
        if not self.eventsub:
            await self.init()
    async def stop(self):
      if self.eventsub:
          await self.eventsub.stop()
      if self.twitch:
          await self.twitch.close()