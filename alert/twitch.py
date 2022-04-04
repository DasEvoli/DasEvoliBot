import json
import settings
import requests
import settings
import time
import traceback
import asyncio
from alert.json_handler import json_handler


class main:
    def __init__(self):
        settings.access_token = self.get_access_token()
        if not json_handler.alert_file_exists():
            json_handler.create_alert_file()
            
    # Twitch API requires now an Access Token for every request
    def get_access_token(self):
        try:
            url = "https://id.twitch.tv/oauth2/token?client_id=" + settings.client_id + "&client_secret=" + settings.client_secret + "&grant_type=client_credentials"
            response = requests.post(url)
            if response.status_code != 200: raise Exception("Couldn't get Access Token. Status Code is not 200.")
            data = json.loads(response.text)
            if not data['access_token']:
                raise Exception("Couldn't get Access Token. No access_token in response text")
            return data['access_token']
        except Exception as e:
            print(e)
            return None

    # This function loops and checks x seconds if any alert should fire. This includes a cooldown
    # The cooldown is necessary so the alert doesn't fire if the channel was just offline for a short time
    # After the cooldown check comes a check if the channel was checked before and is just still online
    # Theoretically we could remove the cooldown but then the Twitch API will be called too often
    async def check_alerts(self):
        while True:
            await asyncio.sleep(settings.twitch_alert_check_delay)
            try:
                with open('alert/channels.json', 'r') as f:
                    data = json.load(f)
                    f.close()
                # items() -> [0] = key, [1] = value
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
        url = "https://api.twitch.tv/helix/streams?user_login=" + twitch_name
        try:
            headers = {'client-id': settings.client_id, 'Authorization': "Bearer " + settings.access_token}
            response = requests.get(url, headers=headers)
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

    async def send_alert(self, channel_ids, twitch_name):
        try:
            for id in channel_ids:
                channel = settings.bot.get_channel(id)
                await channel.send("@everyone https://www.twitch.tv/{} JUST WENT ONLINE!".format(twitch_name))
        except Exception as e:
            print(e)
            traceback.print_stack()