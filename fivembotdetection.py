import requests
import os
import json
import argparse

parser = argparse.ArgumentParser(description='Script to check if FiveM server Botting.')
parser.add_argument('cfxcode', type=str, help='The cfxcode to check the FiveM server API.')
args = parser.parse_args()

api_key = "your steam api key"
cfxcode = args.cfxcode
botscore = 0

def hex_to_steam64(hex_id):
    steam64id = int(hex_id, 16)
    return steam64id

def get_steam_profile(steam64_id, api_key):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam64_id}"
    response = requests.get(url)
    data = response.json()
    try:
        player = data['response']['players'][0]
        return player['personaname']
    except (KeyError, IndexError):
        return False



os.system("curl -X GET https://servers-frontend.fivem.net/api/servers/single/" + str(cfxcode) + " -o response.json")

with open('response.json', encoding='utf-8') as file:
    data = json.load(file)

players = data['Data']['players']

identifiers = []
for item in players:
    for identifier in item['identifiers']:
        if identifier.startswith('steam:'):
            identifiers.append(identifier)

for i in identifiers:
    prefix, steam_hex = i.split(":")
    if not get_steam_profile(hex_to_steam64(steam_hex), api_key):
        botscore += 1

print("The server bot score is : " + str(botscore))
