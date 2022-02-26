import json
import settings
from pathlib import Path
import requests
import settings
import time
import traceback
import asyncio

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

    @staticmethod
    def add_twitch_channel(discord_server:str, twitch_channel:str, discord_channel_id:int):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['discord_server'][discord_server].append({
            'twitch_channel': twitch_channel,
            'last_check': 0,
            'discord_channel_id': discord_channel_id,
            'still_online': False
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


class main:

    def __init__(self):
        settings.access_token = self.get_access_token()
        if not json_handler.alert_file_exists():
            json_handler.create_alert_file()
            
    # Twitch API requires now an Access Token for every request.
    def get_access_token(self):
        try:
            link = "https://id.twitch.tv/oauth2/token?client_id=" + settings.client_id + "&client_secret=" + settings.client_secret + "&grant_type=client_credentials"
            response = requests.post(link)
            if response.status_code != 200: raise Exception("Couldn't get Access Token. Status Code is not 200.")
            data = json.loads(response.text)
            if not data['access_token']:
                raise Exception("Couldn't get Access Token. No access_token in response text")
            return data['access_token']
        except Exception as e:
            print(e)
            return None

    # This function loops and checks x seconds if any alert should fire. This includes a cooldown.
    # The cooldown is necessary so the alert doesn't fire if the channel was just offline for a short time.
    # After the cooldown check comes a check if the channel was checked before and is just still online.
    # This means when a streamer goes offline and online again after 50 minutes (depending on the setting) it will not fire an alert.
    # Theoretically we could remove the cooldown but then the Twitch API will be called too often.
    async def check_alerts(self):
        while True:
            await asyncio.sleep(settings.twitch_alert_check_delay)
            try:
                with open('alert/channels.json', 'r') as f:
                    data = json.load(f)
                    f.close()
                for discord_server in data['discord_server']:
                    for item in data['discord_server'][discord_server]:
                        current_time_s = int(round(time.time()))
                        if current_time_s - item['last_check'] < settings.twitch_alert_cooldown:
                            continue
                        else: 
                            item['last_check'] = current_time_s
                            if self.live_on_twitch(item['twitch_channel']):
                                if item['still_online']:
                                    break
                                else: 
                                    await self.send_alert(item['discord_channel_id'], item['twitch_channel'])
                                    item['still_online'] = True
                            else:
                                item['still_online'] = False
                            with open('alert/channels.json', 'w') as f:
                                json.dump(data, f, indent=2)
                                f.close()
            except Exception as e:
                print(e)
                continue
                            
    def live_on_twitch(self, twitch_channel:str):
        link = "https://api.twitch.tv/helix/streams?user_login=" + twitch_channel
        try:
            headers = {'client-id': settings.client_id, 'Authorization': "Bearer " + settings.access_token}
            response = requests.get(link, headers=headers)
            data = json.loads(response.text)
            if response.status_code == 200:
                # if Response Data length is larger than 0 it means the user is online
                return len(data['data']) > 0
            if response.status_code == 401:
                settings.access_token = self.get_access_token()
                print("Twitch Access Token was invalid. Generating a new one.")
                return self.live_on_twitch(twitch_channel)
            raise("Unknwon Status Error Code: " + response.status_code)
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    # Posts a message in saved channel (We iterate through every discord_server and channel to find the right one)
    # Todo: Rewrite how channels are getting checked. Instead of checking every item in every channel, just check the items and then send
    # all channels which added this item a message.
    async def send_alert(self, channel_id, twitch_channel):
        try:
            for guild in settings.bot.guilds:
                for channel in guild.channels:
                    if channel.id == channel_id:
                        await channel.send("@everyone https://www.twitch.tv/{} JUST WENT ONLINE!".format(twitch_channel))
        except Exception as e:
            print(e)
            traceback.print_stack()