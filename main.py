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
from sessions import get_session

class TelegramBot:
    def __init__(self, api_id, api_hash, session_name):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.current_status = None

    def print_status(self, add_text=""):
        print(f"{add_text}{datetime.now().time().strftime("%H:%M")} - {self.current_status}")    

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
        self.print_status("Changed. ")

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
       
    async def continuous_print_status(self):
        while True:
            self.print_status()
            await asyncio.sleep(3600)

    def get_setted_status(self, bio_text):
        for i in status_dict:
            if status_dict[i]['text'] == bio_text:
                return i

    async def start(self):
        await self.client.start()
        me = await self.client.get_me()
        full = await self.client(GetFullUserRequest(me.username))
        self.current_status = self.get_setted_status(full.full_user.about)

        print("Status check started!")

        @self.client.on(events.NewMessage(outgoing=True, pattern='!check'))
        async def handler(event):
            self.print_status("Checked. ")
            m = await event.respond(f'Check - {datetime.now().time().isoformat(timespec="minutes")} - {self.current_status}')
            await asyncio.sleep(5)
            await self.client.delete_messages(event.chat_id, [event.id, m.id])

        @self.client.on(events.NewMessage(outgoing=True, pattern='!exit'))
        async def handler(event):
            await self.client.disconnect()

        @self.client.on(events.NewMessage(outgoing=True, pattern='!work'))
        async def handler(event):
            await self.set_status(work)
            await self.result_and_clear(event, work)
        
        @self.client.on(events.NewMessage(outgoing=True, pattern='!life'))
        async def handler(event):
            await self.set_status(life)
            await self.result_and_clear(event, life)

        @self.client.on(events.NewMessage(outgoing=True, pattern='!sleep'))
        async def handler(event):
            await self.set_status(sleep)
            await self.result_and_clear(event, sleep)

        # start time check
        self.client.loop.create_task(self.check_time_status())

        # start print status
        self.client.loop.create_task(self.continuous_print_status())
        
        await self.client.run_until_disconnected()


if __name__ == '__main__':
    session_name = get_session()
    bot = TelegramBot(settings.API_ID, settings.API_HASH, session_name)
    asyncio.run(bot.start())
