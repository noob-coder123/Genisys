from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import csv
import sys
import pickle
import random
import pyfiglet
import os
import datetime
from colorama import init, Fore
from telethon.tl.types import UserStatusRecently

init()

lg = Fore.LIGHTGREEN_EX
rs = Fore.RESET
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN


info = lg + '[' + w + 'INFO' + lg + ']' + rs
error = lg + '[' + r + 'ERROR' + lg + ']' + rs
success = w + '[' + lg + 'SUCCESS' + w + ']' + rs
INPUT = lg + '[' + w + 'INPUT' + lg + ']' + rs
colors = [lg, w, r, cy]
def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Genisys')
    print(random.choice(colors) + logo + rs)

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

clr()
banner()
print(info + lg + ' Version: 2.1 | Author: Cryptonian | TG- @Cryptonian_007' + rs)
print(info + lg + ' Filter active users without any hassle!' + rs + '\n')
f = open('vars.txt', 'rb')
accs = []
while True:
    try:
        accs.append(pickle.load(f))
    except EOFError:
        f.close()
        break
print(f'{INPUT}{lg} Choose an account to scrape members')
i = 0
for acc in accs:
    print(f'{lg}[{w}{i}{lg}] {acc}')
    i += 1
ind = int(input(f'{INPUT}{lg} Enter choice: '))
api_id = accs[ind][0]
api_hash = accs[ind][1]
phone = accs[ind][2]
client = TelegramClient(phone, api_id, api_hash)
client.connect()
if not client.is_user_authorized():
    try:
        client.send_code_request(phone)
        code = input(f'{INPUT}{lg} Enter the code for {phone}{r}: ')
        client.sign_in(phone, code)
    except PhoneNumberBannedError:
        print(f'{error}{r}{phone} is banned!{rs}')
        print(f'{error}{r} Run manager.py to filter them{rs}')
        sys.exit()
username = input(f'{INPUT}{lg} Enter the exact username of the public group[Without @]: {r}')
target_grp = 't.me/' + str(username)
group = client.get_entity(target_grp)
time = datetime.datetime.now().strftime("%H:%M")
print('\n' + info + lg + ' Started on ' + str(time) + rs)
print(f'{info}{lg} Scraping members from {rs}' + str(group.title))
members = []
members = client.get_participants(group, aggressive=True)
print(f'{info}{lg} Saving in members.csv...{rs}')
select = str(input(f'{INPUT}{lg} Do you wanna filter active users?[y/n]: '))
with open("members.csv", "w", encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
    if select == 'y':
        for member in members:
            accept = True
            if not member.status == UserStatusRecently():
                accept = False
            if accept:
                if member.username:
                    username = member.username
                else:
                    username = ''
                writer.writerow([username, member.id, member.access_hash, group.title, group.id])
        print(f'{success}{lg} Filtered!')
    else:
        for member in members:
            if member.username:
                username = member.username
            else:
                username = ''
            writer.writerow([username, member.id, member.access_hash, group.title, group.id])
f.close()
print(f'{success}{lg} Scraping Successful{rs}')
input('\nPress enter to exit...')
clr()
banner()
with open('target_grp.txt', 'w') as f:
    f.write(target_grp)
f.close()
sys.exit()

