from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import time
import random
import pyfiglet
from telethon.tl.types import PeerUser
from colorama import init, Fore
#import traceback
import os
init()

r = Fore.RED
g = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, g, w, ye, cy]
info = g + '[' + w + 'INFO' + g + ']' + rs
attempt = g + '[' + w + 'ATTEMPT' + g + ']' + rs
sleep = g + '[' + w + 'SLEEP' + g + ']' + rs
error = g + '[' + r + 'ERROR' + g + ']' + rs
def banner():
    f = pyfiglet.Figlet(font='slant')
    logo = f.renderText('Genisys')
    print(random.choice(colors) + logo + rs)
    print(f'{info}{g} Genisys Adder V2.1 by Cryptonian{rs}')
    print(f'{info}{g} Telegram- @Cryptonian_007{rs}\n')
def clscreen():
    os.system('cls')
clscreen()
banner()
api_id = int(sys.argv[1])
api_hash = str(sys.argv[2])
phone = str(sys.argv[3])
file = str(sys.argv[4])
group = str(sys.argv[5])
scraped = str(sys.argv[6])
class Relog:
    def __init__(self, lst, filename):
        self.lst = lst
        self.filename = filename
    def start(self):
        with open(self.filename, 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
            for user in self.lst:
                writer.writerow([user['username'], user['user_id'], user['access_hash'], user['group'], user['group_id']])
            f.close()
def update_list(lst, temp_lst):
    count = 0
    while count != len(temp_lst):
        del lst[0]
        count += 1
    return lst
users = []
with open(file, 'r', encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=',', lineterminator='\n')
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = row[2]
        user['group'] = row[3]
        user['group_id'] = row[4]
        users.append(user)
    f.close()
client = TelegramClient(phone, api_id, api_hash)
client.connect()
time.sleep(1.5)
target_group = client.get_entity(group)
entity = InputPeerChannel(target_group.id, target_group.access_hash)
group_name = target_group.title
n = 0
print(f'{info}{g} Getting entities{rs}\n')
target_m = client.get_entity(scraped)
client.get_participants(target_m, aggressive=True)
print(f'{info}{g} Adding members to {group_name}{rs}\n')
added_users = []
for user in users:
    n += 1
    if n % 50 == 0:
        print(f'{sleep}{g} Sleep 2 min to prevent possible account ban{rs}')
        time.sleep(120)
    try:
        print(user)
        added_users.append(user)
        user_to_add = client.get_entity(user['id'])
        client(InviteToChannelRequest(entity, [user_to_add]))
        us_id = user['id']
        print(f'{attempt}{g} Adding {us_id}{rs}')
        print(f'{sleep}{g} Sleep 20s{rs}')
        time.sleep(20)
    except PeerFloodError:
        print(f'\n{error}{r} Aborted. Peer Flood Error{rs}')
        count = 0
        while count <= len(added_users):
            del users[0]
            count += 1
        if not len(users) == 0:
            with open(file, 'w', encoding='UTF-8') as f:
                writer = csv.writer(f, delimiter=',', lineterminator='\n')
                writer.writerow(['username', 'user id', 'access hash', 'group', 'group id'])
                for user in users:
                    writer.writerow([user['username'], user['id'], user['access_hash'], user['group'], user['group_id']])
                f.close()  
    except UserPrivacyRestrictedError:
        print(f'{error}{r} User Privacy Error[non-serious]{rs}')
        continue
    except ValueError:
        print(f'{error}{r} Error in processing entity{rs}')
        continue
    except KeyboardInterrupt:
        print(f'{error}{r} Aborted. Keyboard Interrupt{rs}')
        update_list(users, added_users)
        if not len(users) == 0:
            print(f'{info}{g} Remaining users logged to {file}')
            logger = Relog(users, file)
            logger.start()
    except Exception as e:
        print(f'{error}{r} Some Other error in adding{rs}')
        print(e)
        continue
length = str(len(users))
print(f'{info}{g}{length} attempts completed.')
os.system(f'del {file}')
sys.exit()