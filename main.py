import requests
import json
import os
import time
import re
import uuid
from fake_useragent import UserAgent
from colorama import init, Fore, Style
import fade
import keyboard

def clean_filename(hostname):
    # Remove invalid characters and leading digits
    return re.sub(r'^[0-9]+', '', re.sub(r'[/:"*?<>|]', '', hostname))

def check_if_player_exists(filename, player_data, added_players):
    if not os.path.exists(filename):
        return False

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                existing_player = json.loads(line)
            except json.JSONDecodeError:
                continue

            if existing_player.get('fivem') == player_data.get('fivem'):
                fields_to_check = ['steam', 'name', 'live', 'xbl', 'license', 'license2']
                if all(existing_player.get(field) == player_data.get(field) for field in fields_to_check if existing_player.get(field) or player_data.get(field)):
                    return True

    return player_data['identifiers'] in added_players

def get_server_info(server_id, proxy, added_players):
    url = f'https://servers-frontend.fivem.net/api/servers/single/{server_id}'
    user_agent = UserAgent()
    headers = {
        'User-Agent': user_agent.random,
        'method': 'GET'
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)

        if response.status_code == 200:
            server_data = response.json()
            hostname = clean_filename(str(uuid.uuid4()))  # Default to a UUID

            if 'hostname' in server_data['Data']:
                hostname = clean_filename(server_data['Data']['hostname'])[:100]
            elif 'sv_projectName' in server_data['Data']['vars'] and len(server_data['Data']['vars']['sv_projectName']) >= 10:
                hostname = clean_filename(server_data['Data']['vars']['sv_projectName'])[:100]

            os.makedirs('dump', exist_ok=True)
            filename = f'dump/{hostname}.sql'

            for player in server_data['Data']['players']:
                if not check_if_player_exists(filename, player, added_players):
                    with open(filename, 'a', encoding='utf-8') as file:
                        file.write(json.dumps(player, ensure_ascii=False) + '\n')
                    with open("information/valid.txt", "a") as valid_file:
                        valid_file.write(f"{server_id}\n")
                    print(Fore.BLUE + f'[Player of {hostname}]' + Style.RESET_ALL + f' {player["name"]} was added to the dump!')
                    added_players.append(player['identifiers'])

            print(Fore.CYAN + f'\n[AUTHOR] Developed by nyxos.spk\n[INFO] Server name: {hostname}\n[INFO] Server id: {server_id}\n[INFO] Saved in: {filename}\n[INFO] Server URL: {url}\n')

        else:
            print(Fore.RED + f'\n[ERROR] Error message ({server_id}: {response.status_code})\n')
            with open("information/not_valid.txt", "a") as invalid_file:
                invalid_file.write(f'\n[ERROR] Error message ({server_id}: {response.status_code})\n')

    except Exception as e:
        print(f'Error: {str(e)}')

def process_servers(server_ids, proxies, added_players):
    for server_id, proxy in zip(server_ids, proxies):
        get_server_info(server_id, proxy, added_players)
        time.sleep(0.5)

def main():
    with open('serveur.txt', 'r') as server_file:
        french_server_ids = [line.strip() for line in server_file.readlines()]

    with open('serveur_quebec.txt', 'r') as quebec_server_file:
        quebec_server_ids = [line.strip() for line in quebec_server_file.readlines()]

    with open('proxy.txt', 'r') as proxy_file:
        proxy_list = [{'http': f'socks5://{proxy.strip()}'} for proxy in proxy_file]

    added_players = []
    
    while True:
        for server_id in french_server_ids:
            process_servers([server_id], proxy_list, added_players)

        for server_id in quebec_server_ids:
            process_servers([server_id], proxy_list, added_players)

        print(Fore.MAGENTA + "\n[TIME] Dump completed, please wait (2min)...\n")
        time.sleep(120)

def features():
    print(Fore.MAGENTA + "\n╔══════════════1.5══════════════╗\n[D] 29/08/2024\n[#] Fixed tool\n[+] Added logs\n[+] Added not valid server\n[+] Added valid server\n╚══════════════1.5══════════════╝")
    
def quit_program():
    os.system("pause")

def features2():
    print(Fore.GREEN + ''' 
 _____          _                       
|  ___|__  __ _| |_ _   _ _ __ ___  ___ 
| |_ / _ \/ _` | __| | | | '__/ _ \/ __|
|  _|  __/ (_| | |_| |_| | | |  __/\__ \ 
|_|  \___|\__,_|\__|\__,_|_|  \___||___/          
                - Developer: nyxos.spk       
                - Discord: _bash.__
                - Telegram: https://t.me/nyxosZNkick
''')

def startup():
    os.system("cls")
    banner = '''
 _____ _           __  __                                            
|  ___(_)_   _____|  \/  |  ___  ___ _ __ __ _ _ __   ___ _ __ 
| |_  | \ \ / / _ \ |\/| | / __|/ __| '__/ _` | '_ \ / _ \ '__|
|  _| | |\ V /  __/ |  | | \__ \ (__| | | (_| | |_) |  __/ |   
|_|   |_| \_/ \___|_|  |_| |___/\___|_|  \__,_| .__/ \___|_|   
                                              |_|               
                - Developer: nyxos.spk       
                - Discord: nyxosv19
                - signal: nyxos.77
'''
    faded_text = fade.greenblue(banner)
    print(faded_text)
    print(Fore.BLUE + "[!] PRESS [a] TO START")
    print(Fore.BLUE + "[!] PRESS [b] TO SHOW Features")
    print(Fore.RED + "\n[!] PRESS [Q] TO Quit")

    while True:
        if keyboard.read_key() == "a":
            os.system("cls")
            print(faded_text)
            main()

        if keyboard.read_key() == "b":
            os.system("cls")
            features2()
            features()
            while True:
                if keyboard.read_key() == "z":
                    os.system("cls")
                    startup()

        if keyboard.read_key() == "q":
            os.system("cls")
            exit()

startup()
