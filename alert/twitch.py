# Module to add the username of a twitch channel to an alert list. Next time the user goes online your channel where you used this command will get a notification

import json
import settings
import os
from pathlib import Path
import requests
import settings
import asyncio
import time


# Handles all the json functionality for the alert function
class json_handler:

    @staticmethod
    def alert_file_exists():
        f = Path('alert/channels.json')
        return f.is_file()

    @staticmethod
    def create_alert_file():
        with open('alert/channels.json', 'w+') as f:
            data = {}
            data['discord_server'] = {}
            json_dump = json.dumps(data)
            f.write(json_dump)
            f.flush
            f.close

    @staticmethod
    def discord_server_exists(discord_server: str):
        with open('alert/channels.json', 'r') as f:
            # We need to check if the file is empty
            data = json.load(f)
            if len(data['discord_server']) < 1:
                return False
            f.close()

        for key in data['discord_server'].keys():
            if key == discord_server:
                return True
        return False

    @staticmethod
    def add_discord_server(discord_server: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['discord_server'][discord_server] = []
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()

    @staticmethod
    def twitch_channel_exists(discord_server:str, twitch_channel: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
            f.close()
        for item in data['discord_server'][discord_server]:
            if str(twitch_channel) == item['twitch_channel']:
                return True
        return False

    # We need discord_channel_id so we know where the bot should post the message
    @staticmethod
    def add_twitch_channel(discord_server:str, twitch_channel:str, discord_channel_id:int):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['discord_server'][discord_server].append({
            'twitch_channel': twitch_channel,
            'last_alert': 0,
            'discord_channel_id': discord_channel_id,
            'was_online': False
        })
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()
    
    @staticmethod
    def remove_twitch_channel(discord_server:str, twitch_channel:str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        # Count is the index. It counts up when twitch-channel is not the searched one
        count = -1
        for item in data['discord_server'][discord_server]:
            count = count + 1
            if str(twitch_channel) == item['twitch_channel']:
                data['discord_server'][discord_server].pop(count)
                break
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()


# Handles all the functionality to get the data from twitch and sends messages if anyone is online
# Todo: We use should separete some json functions to the json class above
class main:

    def __init__(self):
        settings.api_token = self.get_api_token()
        if not json_handler.alert_file_exists():
            json_handler.create_alert_file()
            
    # Twitch api requires now for every api call an access_token
    def get_api_token(self):
        try:
            link = "https://id.twitch.tv/oauth2/token?client_id=" + settings.client_id + "&client_secret=" + settings.client_secret + "&grant_type=client_credentials"
            response = requests.post(link)
            if response.status_code != 200:
                print("Couldn't get a new access_token!")
                return None
            data = json.loads(response.text)
            if not data['access_token']:
                return None
            return data['access_token']
        except Exception as e:
            print(e)
            return None

    # This function loops and checks x seconds if any alert should fire
    async def check_alerts(self):
        while True:
            # We wait a bit so we don't call it too often
            await asyncio.sleep(10)

            try:
                # We get the currently saved alerts
                with open('alert/channels.json', 'r') as f:
                    data = json.load(f)
                    f.close()

                # We iterate through every server and get check every alert
                for discord_server in data['discord_server']:
                    for item in data['discord_server'][discord_server]:
                        # Cooldown (currently 1 hour)
                        current_time_s = int(round(time.time()))
                        if current_time_s - item['last_alert'] < 3600:
                            # Still has cooldown
                            continue
                        else: 
                            if await self.live_on_twitch(item['twitch_channel']):
                                # Twitch Channel is live and alert has no cooldown
                                # We save the current time for this alert so we can test later if it is on cooldown
                                item['last_alert'] = current_time_s
                                if item['was_online']:
                                    with open('alert/channels.json', 'w') as f:
                                        json.dump(data, f, indent=2)
                                        f.close()
                                    break
                                else: 
                                    await self.send_alert(item['discord_channel_id'], item['twitch_channel'])
                                    item['was_online'] = True
                                    with open('alert/channels.json', 'w') as f:
                                        json.dump(data, f, indent=2)
                                        f.close()
                            else:
                                if item['was_online']:
                                    item['was_online'] = False
                                    with open('alert/channels.json', 'w') as f:
                                        json.dump(data, f, indent=2)
                                        f.close()
            except Exception as e:
                print('Exception thrown in check_alerts: ')
                print(e)
                self.check_alerts()
                            

    # Get request to twitch api to check if user is online
    async def live_on_twitch(self, twitch_channel:str):
        link = "https://api.twitch.tv/helix/streams?user_login=" + twitch_channel
        try:
            headers = {'client-id': settings.client_id, 'Authorization': "Bearer " + settings.api_token}
            response = requests.get(link, headers=headers)
            data = json.loads(response.text)
            # 401 means authorization failed. We get a new token
            if response.status_code == 401:
                print("Bot is not authorized to check if channel is online")
                settings.api_token = self.get_api_token()
                self.live_on_twitch(twitch_channel)
            # If data is empty but status code 200, channel is offline. If it's not empty channel is online
            if response.status_code == 200:
                return len(data['data']) > 0
            if response.status_code != 200:
                print("Unknown status error code: ")
                print(response.status_code)
                return False
        except Exception as e:
            print(e)
            return False

    # Posts a message in saved channel (We iterate through every discord_server and channel to find the right one)
    # There is probably a better, faster way
    async def send_alert(self, channel_id, twitch_channel):
        try:
            for guild in settings.bot.guilds:
                for channel in guild.channels:
                    if channel.id == channel_id:
                        await channel.send("@everyone https://www.twitch.tv/{} JUST WENT ONLINE!".format(twitch_channel))
        except Exception as e:
            print(e)
            return False