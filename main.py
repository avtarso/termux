import os
import sys
import asyncio
from datetime import datetime

from telethon import events
from telethon.sync import TelegramClient
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest, DeletePhotosRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import InputPhoto

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import settings
from options import sleep, life, work, status_dict
from time_settings import get_time_status

class TelegramBot:
    def __init__(self, api_id, api_hash):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.current_status = None

    async def update_profile_photo(self, file):
        photos = await self.client.get_profile_photos('me')
        if photos:
            photos_to_delete = [InputPhoto(id=photo.id, access_hash=photo.access_hash, file_reference=photo.file_reference) for photo in photos[:1]]
            await self.client(DeletePhotosRequest(id=photos_to_delete)) 
        await self.client(UploadProfilePhotoRequest(file=file))

    async def set_status(self, status):
        file = await self.client.upload_file(status_dict[status]['file'])
        await self.update_profile_photo(file)
        await self.client(UpdateProfileRequest(about=status_dict[status]['text']))
        self.current_status = status

    async def result_and_clear(self, event, status):
        result = await event.respond(f'Status "{status}" set!')
        await asyncio.sleep(5)
        await self.client.delete_messages(event.chat_id, [event.id, result.id])

    async def check_time_status(self):
        while True:
            new_time_status = get_time_status()
            if new_time_status != self.current_status:
                await self.set_status(new_time_status)
            await asyncio.sleep(60)

    async def start(self):
        await self.client.start()
        me = await self.client.get_me()
        full = await self.client(GetFullUserRequest(me.username))
        self.current_status = full.full_user.about

        print("Status check started!")

        @self.client.on(events.NewMessage(outgoing=True, pattern='!time'))
        async def handler(event):
            m = await event.respond(f'!pong {datetime.now().time().isoformat(timespec="minutes")}')
            await asyncio.sleep(5)
            await self.client.delete_messages(event.chat_id, [event.id, m.id])

        @self.client.on(events.NewMessage(outgoing=True, pattern='!ex'))
        async def handler(event):
            await self.client.disconnect()

        @self.client.on(events.NewMessage(outgoing=True, pattern='!pf1'))
        async def handler(event):
            await self.set_status(work)
            await self.result_and_clear(event, work)
        
        @self.client.on(events.NewMessage(outgoing=True, pattern='!pf2'))
        async def handler(event):
            await self.set_status(life)
            await self.result_and_clear(event, life)

        @self.client.on(events.NewMessage(outgoing=True, pattern='!pf3'))
        async def handler(event):
            await self.set_status(sleep)
            await self.result_and_clear(event, sleep)

        # start time check
        self.client.loop.create_task(self.check_time_status())
        
        await self.client.run_until_disconnected()


if __name__ == '__main__':
    bot = TelegramBot(settings.API_ID, settings.API_HASH)
    asyncio.run(bot.start())
