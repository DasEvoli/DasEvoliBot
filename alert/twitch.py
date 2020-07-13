# Module to add the username of a twitch channel to an alert list. Next time the user goes online your channel where you used this command will get a notifcation

import json
import utils
# To use file stats
import os
# To use is_file()
from pathlib import Path
import requests
import settings
import asyncio
import time


# Handles all the json functionality for the alert function
class json_handler:

    @staticmethod
    def check_if_server_exists(server: str):
        with open('alert/channels.json', 'r') as f:
            # We need to check if the file is empty
            if os.stat("alert/channels.json").st_size == 0:
                return False
            data = json.load(f)
            f.close()

        for key in data['server'].keys():
            if key == server:
                return True
        return False

    @staticmethod
    def add_server(server: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['server'][server] = []
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()

    @staticmethod
    def check_if_twitch_channel_exists(server:str, twitch_channel: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
            f.close()

        for item in data['server'][server]:
            if str(twitch_channel) == item['channel']:
                return True
        return False

    @staticmethod
    def add_twitch_channel(server:str, twitch_channel:str, discord_channel_id:int):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['server'][server].append({
            'channel': twitch_channel,
            'last_alert': 0,
            'discord_channel_id': discord_channel_id
        })
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()
    
    @staticmethod
    def remove_twitch_channel(server:str, twitch_channel:str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        count = -1
        for item in data['server'][server]:
            count = count + 1
            if str(twitch_channel) == item['channel']:
                data['server'][server].pop(count)
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()

    @staticmethod 
    def get_all_servers():
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
            f.close()

        server_list = []
        for server in data['server']:
            server_list.append(server)
        return server_list


# Handles all the functionality to get the data from twitch and sends messages if anyone is online
# Todo: We use should separete some json functions to the json class above
class main:
     
    def __init__(self):
        pass

    # This function loops and checks x seconds if any alert should fire
    async def check_alerts(self):
        while True:

            # How often it should fire
            await asyncio.sleep(300)

            # We get the currently saved alerts
            with open('alert/channels.json', 'r') as f:
                data = json.load(f)
                f.close()

            # We iterate through every server and get check every alert
            for server in data['server']:
                for item in data['server'][server]:
                    # Cooldown
                    current_time_s = int(round(time.time()))
                    if current_time_s - item['last_alert'] < 43200: 
                        # Still has cooldown
                        continue
                    else: 
                        if self.check_if_live_on_twitch(item['channel']):
                            # Channel is live and alert has no cooldown
                            # We save the current time for this alert so we can test later if it is on cooldown
                            item['last_alert'] = current_time_s
                            with open('alert/channels.json', 'w') as f:
                                json.dump(data, f, indent=2)
                                f.close()
                            # Alert in saved channel
                            await self.alert_in_channel(item['discord_channel_id'], item['channel'])

    # Get request to twitch api to check if user is online
    def check_if_live_on_twitch(self, twitch_channel:str):
        link = "https://api.twitch.tv/helix/streams?user_login="
        link = link + twitch_channel

        headers = {'Client-ID': settings.client_id}
        response = requests.get(link, headers=headers)
        data = json.loads(response.text)
        # If data is empty channel is offline
        return len(data['data']) > 0

    # Posts a message in saved channel (We iterate through every server and channel to find the right one)
    # There is probably a better, faster way
    async def alert_in_channel(self, channel_id, twitch_channel):
        for guild in utils.bot.guilds:
            for channel in guild.channels:
                if channel.id == channel_id:
                    await channel.send("@everyone https://www.twitch.tv/{} JUST WENT ONLINE!".format(twitch_channel))