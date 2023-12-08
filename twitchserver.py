from lib import ChatBot, EventListener, SiiliCamController, set_random_ndi_source, get_client_info, get_channel
import asyncio
# lets run our setup

async def main():
    client_id, client_secret = get_client_info()
    channel = get_channel()
    chatbot = ChatBot(client_id, client_secret, channel)
    reward_listener = EventListener(client_id, client_secret, channel)
    await chatbot.run()
    await reward_listener.run()
    input("Press Enter to stop...\n")

    # Stop both the chatbot and the reward listener
    await chatbot.stop()
    await reward_listener.stop()
    set_random_ndi_source()
    
if __name__ == "__main__":
    
    asyncio.run(main())