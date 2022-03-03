# This controller handles all the json functionality to have statistics for the fighting game
# Players can be multiple times in json file but assigned to different servers
# Win = 1 point
# Lose = -1 point
# Kill = 1 point
# Seasongames is a feature that is not added yet
# TODO: Json file needs at least this '"{server": {}}' to work. We should automate it

import json
import settings
# To use file stats
import os
# To use is_file()
from pathlib import Path

def statistic_file_exists():
    fight_statistic_file = Path('games/fight/fight_statistics.json')
    return fight_statistic_file.is_file()


def create_statistic_file():
    with open('games/fight/fight_statistics.json', 'w+') as f:
        data = {}
        data['server'] = {}
        json_dump = json.dumps(data)
        f.write(json_dump)
        f.flush
        f.close


def add_new_player(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    data['server'][servername].append({
        'name': player.name,
        'id': str(player.user.id),
        'kills': 0,
        'wins': 0,
        'loses': 0,
        'games': 0,
        'points': 0,
        'seasongames': 0
    })
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


def add_win(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    for item in data['server'][servername]:
        if item['id'] == str(player.user.id):
            item['wins'] += 1
            item['points'] += 1
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


def add_lose(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    for item in data['server'][servername]:
        if item['id'] == str(player.user.id):
            item['loses'] += 1
            item['points'] -= 1
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


def add_kill(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    for item in data['server'][servername]:
        if item['id'] == str(player.user.id):
            item['kills'] += 1
            item['points'] += 1
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


def add_game(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    for item in data['server'][servername]:
        if item['id'] == str(player.user.id):
            item['games'] += 1
            item['seasongames'] += 1
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


def check_player_exists(servername, player):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
        f.close()

    for item in data['server'][servername]:
        if str(player.user.id) == item['id']:
            return True
    return False


def check_server_exists(servername):
    with open('games/fight/fight_statistics.json', 'r') as f:
        # We need to check if the file is empty
        if os.stat("games/fight/fight_statistics.json").st_size == 0:
            return False
        data = json.load(f)
        f.close()

    for key in data['server'].keys():
        if key == servername:
            return True
    return False


def add_server(servername):
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
    data['server'][servername] = []
    with open('games/fight/fight_statistics.json', 'w') as f:
        json.dump(data, f, indent=2)
        f.close()


# Posts the statistic of a user
# You can mention multiple users but need at least one mention
@settings.bot.command()
async def statistic(ctx):
    mentions = ctx.message.mentions
    servername = ctx.guild.name
    if len(mentions) <= 0:
        await ctx.send("No user was selected")
        return
    else:
        with open('games/fight/fight_statistics.json', 'r') as f:
            data = json.load(f)
            f.close()
        for item in data['server'][servername]:
            if str(mentions[0].id) == item['id']:
                await ctx.send(item['name'] + "\n"
                               + "Games: " + str(item['games']) + "\n"
                               + "Wins: " + str(item['wins']) + "\n"
                               + "Loses: " + str(item['loses']) + "\n"
                               + "Kills: " + str(item['kills']) + "\n"
                               + "Rangpoints: " + str(item['points']) + "\n"
                               + "Games this season: " + str(item['seasongames']))
                return
    await ctx.send("No players found with the name: " + mentions[0].name)

# Posts the ranking of all players on that server
@settings.bot.command()
async def ranking(ctx):
    servername = ctx.guild.name
    with open('games/fight/fight_statistics.json', 'r') as f:
        data = json.load(f)
        f.close()
    playerList = []
    for player in data['server'][servername]:
        playerList.append(player)

    def points(val):
        return val['points']

    playerList.sort(key=points, reverse=True)
    stringRanglist = ""
    rank = 0
    lastPlayerPoints = -99999

    for player in playerList:
        if lastPlayerPoints == player['points']:
            stringRanglist += str(rank) + ". " + player['name'] + ": " + str(player['points']) + "\n"
        else:
            lastPlayerPoints = player['points']
            rank += 1
            stringRanglist += str(rank) + ". " + player['name'] + ": " + str(player['points']) + "\n"

    await ctx.send(stringRanglist)