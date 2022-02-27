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
            data['twitch_names'] = {}
            json_dump = json.dumps(data)
            f.write(json_dump)
            f.flush
            f.close

    @staticmethod
    def discord_channel_id_exists(discord_channel_id: str, twitch_name: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
            f.close()

        for id in data['twitch_names'][twitch_name]["channel_ids"]:
            if id == discord_channel_id:
                return True
        return False

    @staticmethod
    def add_discord_channel_id(discord_channel_id: str, twitch_name: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['twitch_names'][twitch_name]["channel_ids"].append(discord_channel_id)
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()
    
    @staticmethod
    def remove_discord_channel_id(discord_channel_id: str, twitch_name: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        data['twitch_names'][twitch_name]["channel_ids"].remove(discord_channel_id)
        with open('alert/channels.json', 'w') as f:
            json.dump(data, f, indent=2)
            f.close()

    @staticmethod
    def twitch_name_exists(twitch_name: str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
            f.close()
        if len(data['twitch_names']) <= 0:
            return False
        if twitch_name in data['twitch_names']:
            return True
        return False

    @staticmethod
    def add_twitch_name(twitch_name:str):
        with open('alert/channels.json', 'r') as f:
            data = json.load(f)
        obj = {
            'last_check': 0,
            'still_online': False,
            "channel_ids": []
        }
        data['twitch_names'][twitch_name] = obj
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
                for twitch_name in data['twitch_names'].items():
                    current_time_s = int(round(time.time()))
                    if current_time_s - twitch_name[1]['last_check'] < settings.twitch_alert_cooldown:
                        continue
                    else: 
                        twitch_name[1]['last_check'] = current_time_s
                        if self.live_on_twitch(twitch_name[0]):
                            if twitch_name[1]['still_online']:
                                break
                            else: 
                                await self.send_alert(twitch_name[1]['channel_ids'], twitch_name[0])
                                twitch_name[1]['still_online'] = True
                        else:
                            twitch_name[1]['still_online'] = False
                        with open('alert/channels.json', 'w') as f:
                            json.dump(data, f, indent=2)
                            f.close()
            except Exception as e:
                print(e)
                continue
                            
    def live_on_twitch(self, twitch_name:str):
        link = "https://api.twitch.tv/helix/streams?user_login=" + twitch_name
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
                return self.live_on_twitch(twitch_name)
            raise("Unknwon Status Error Code: " + response.status_code)
        except Exception as e:
            print(e)
            traceback.print_stack()
            return False

    # Posts a message in saved channel (We iterate through every discord_server and channel to find the right one)
    # Todo: Rewrite how channels are getting checked. Instead of checking every item in every channel, just check the items and then send
    # all channels which added this item a message.
    async def send_alert(self, channel_ids, twitch_name):
        try:
            for id in channel_ids:
                channel = settings.bot.get_channel(id)
                await channel.send("@everyone https://www.twitch.tv/{} JUST WENT ONLINE!".format(twitch_name))
        except Exception as e:
            print(e)
            traceback.print_stack()