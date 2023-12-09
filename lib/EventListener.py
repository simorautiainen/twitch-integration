from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.eventsub.websocket import EventSubWebsocket
from twitchAPI.helper import first
from typing import Callable
from twitchAPI.object.eventsub import ChannelPointsCustomRewardRedemptionAddEvent as Redemption
            
class EventListener:
    def __init__(self, client_id, client_secret, channel_to_manage):
        self.client_id = client_id
        self.client_secret = client_secret
        self.USER_SCOPE = [AuthScope.CHANNEL_READ_REDEMPTIONS, AuthScope.CHANNEL_MANAGE_REDEMPTIONS]
        self.eventsub = None
        self.twitch = None
        self.broadcaster_id = None
        self.channel_to_manage = channel_to_manage
        self.reward_map = dict()
        
    async def add_reward_callback(self, reward_id, callback):
        if not self.broadcaster_id:
            print("Error: Broadcaster ID not set. Ensure EventListener is authenticated.")
            return

        # Subscribe to channel point redemption events for the specific reward
        await self.eventsub.listen_channel_points_custom_reward_redemption_add(
            self.broadcaster_id, callback, reward_id)
    async def custom_reward_callback(self, event: Redemption):
        reward = event.event.reward
        user = event.event.user_name
        user_input = event.event.user_input
        print(f"{user} redeemed reward id: {reward.id}, reward title {reward.title} user input: {user_input}")
            
    async def init(self):
        self.eventsub = EventSubWebsocket(self.twitch)
        self.eventsub.start()

        print("from the init:", self.broadcaster_id)
        await self.eventsub.listen_channel_points_custom_reward_redemption_add(self.broadcaster_id, self.custom_reward_callback)
        await self.fillRewardDict()
    
    async def addCallback(self, rewardId: str, callback: Callable[[Redemption], None]):
        if self.eventsub:
            await self.eventsub.listen_channel_points_custom_reward_redemption_add(self.broadcaster_id, callback, rewardId)
            
    async def authenticate(self):
        self.twitch = await Twitch(self.client_id, self.client_secret)
        auth = UserAuthenticator(self.twitch, self.USER_SCOPE)
        print(auth.return_auth_url())

        token, refresh_token = await auth.authenticate()

        await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)
        user = await first(self.twitch.get_users(logins=[self.channel_to_manage]))
        self.broadcaster_id = user.id
        
    async def authenticate_token(self, token, refresh):
        self.twitch = await Twitch(self.client_id, self.client_secret)
        await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh)

        user = await first(self.twitch.get_users(logins=[self.channel_to_manage]))
        self.broadcaster_id = user.id
        print("broadcaster id:", self.broadcaster_id)
        
    async def getRewards(self):
        return self.reward_map
    
    async def fillRewardDict(self):
        rewards = await self.twitch.get_custom_reward(self.broadcaster_id)
        print("rewards:", rewards)
        for reward in rewards:
            print(f"id: {reward.id}, title: {reward.title}")
            self.reward_map[reward.title] = reward.id
       
    async def run(self):
        # Starts listening for events
        if not self.eventsub:
            await self.authenticate()
            await self.init()
            
    async def stop(self):
      if self.eventsub:
          await self.eventsub.stop()
      if self.twitch:
          await self.twitch.close()