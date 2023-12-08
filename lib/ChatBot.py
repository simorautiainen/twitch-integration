import asyncio
import webbrowser
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData

class ChatBot:
    def __init__(self, client_id, client_secret, channel_to_join):
        self.client_id = client_id
        self.client_secret = client_secret
        self.channel_to_join = channel_to_join
        self.USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
        self.twitch = None
        self.chat = None
        self.register_firefox()

    def register_firefox(self):
        firefox_path = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        webbrowser.register('firefox', None, webbrowser.BackgroundBrowser(firefox_path))

    async def on_ready(self, ready_event: EventData):
        print('ChatBot is ready, joining channel:', self.channel_to_join)
        await ready_event.chat.join_room(self.channel_to_join)

    async def init(self):
        self.twitch = Twitch(self.client_id, self.client_secret)
        auth = UserAuthenticator(self.twitch, self.USER_SCOPE, force_verify=True)
        token, refresh_token = await auth.authenticate(browser_name="firefox", browser_new=1)
        await self.twitch.set_user_authentication(token, self.USER_SCOPE, refresh_token)

        self.chat = await Chat(self.twitch)
        self.chat.register_event(ChatEvent.READY, self.on_ready)
        self.chat.start()
            
    async def run(self):
        # Starts the chat functionality
        if not self.chat:
            await self.init()
    async def stop(self):
        # Stops the chat functionality
        if self.chat:
            self.chat.stop()
        if self.twitch:
            await self.twitch.close()