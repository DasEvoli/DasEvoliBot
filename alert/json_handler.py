import json
from pathlib import Path as path

class twitch:

    @staticmethod
    def alert_file_exists():
        f = path('alert/channels.json')
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
