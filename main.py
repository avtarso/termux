import sys
import os
from telethon.sync import TelegramClient
from telethon import events
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import settings

print(settings.API_ID)
print(settings.API_HASH)


with TelegramClient('session_name', settings.API_ID, settings.API_HASH) as client:

    # @client.on(events.NewMessage(incoming=True, from_users='me'))
    # async def handler(event):
    #     print(event.message.message)
    #     if event.message.message == "ping":
    #         await client.send_message('me', 'pong')
    #     elif event.message.message == "exit":
    #         client.disconnect()
    #     else:
    #         await client.send_message('me', 'error')

    @client.on(events.NewMessage(outgoing=True, pattern='!ping'))
    async def handler(event):
        # Say "!pong" whenever you send "!ping", then delete both messages
        m = await event.respond('!pong')
        await asyncio.sleep(5)
        await client.delete_messages(event.chat_id, [event.id, m.id])


    @client.on(events.NewMessage(outgoing=True, pattern='!exit'))
    async def handler(event):
        client.disconnect()
       
            
    client.run_until_disconnected()
