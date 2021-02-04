from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle
import pyfiglet
from colorama import init, Fore
import os
from time import sleep

init()
r = Fore.RED
n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
f = pyfiglet.Figlet(font='slant')
banner = f.renderText('Genisys')
print(r)
print(banner)
print(n)
print('\n'+lg+'Genisys Account Manager V2.1'+n)
print('Author: Cryptonian | TG- @Cryptonian_007\n')
sleep(4)

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

while True:
    clr()
    print(r)
    print(banner)
    print(n)
    print(lg+'\n[1] Add new accounts and remove old ones'+n)
    print(lg+'[2] Add new accounts to existing ones'+n)
    print(lg+'[3] Filter all banned accounts'+n)
    print(lg+'[4] List out all the accounts'+n)
    print(lg+'[5] Delete specific accounts'+n)
    a = int(input('\nEnter your choice: '))
    if a == 1:
        with open('vars.txt', 'wb') as f:
            while True:
                a = int(input('Enter API ID: '))
                b = str(input('Enter API Hash: '))
                c = str(input('Enter Phone Number: '))
                pickle.dump([a, b, c], f)
                ab = input('Do you want to add more accounts?[y/n]: ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+lg+'[i] Saved all accounts in vars.txt'+n)
                    f.close()
                    sleep(3)
                    break
        f.close()
    elif a == 2:
        with open('vars.txt', 'ab') as g:
            while True:
                a = int(input('Enter API ID: '))
                b = str(input('Enter API Hash: '))
                c = str(input('Enter Phone Number: '))
                pickle.dump([a, b, c], g)
                ab = input('Do you want to add more accounts?[y/n]: ')
                if 'y' in ab:
                    pass
                else:
                    print('\n'+lg+'[i] Saved all accounts in vars.txt'+n)
                    g.close()
                    sleep(3)
                    break
        g.close()
    elif a == 3:
        accounts = []
        banned_accs = []
        h = open('vars.txt', 'rb')
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
        h.close()
        if len(accounts) == 0:
            print(r+'[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            for account in accounts:
                api_id = int(account[0])
                api_hash = str(account[1])
                phone = str(account[2])
                client = TelegramClient(phone, api_id, api_hash)
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        client.sign_in(phone, input('[+] Enter the code: '))
                    except PhoneNumberBannedError:
                        print(r+str(phone) + ' is banned!'+n)
                        banned_accs.append(account)
            if len(banned_accs) == 0:
                print(lg+'Congrats! No banned accounts')
                input('\nPress enter to goto main menu')
            else:
                for m in banned_accs:
                    accounts.remove(m)
                with open('vars.txt', 'wb') as k:
                    for a in accounts:
                        Id = a[0]
                        Hash = a[1]
                        Phone = a[2]
                        pickle.dump([Id, Hash, Phone], k)
                k.close()
                print(lg+'[i] All banned accounts removed'+n)
                input('\nPress enter to goto main menu')
    elif a == 4:
        display = []
        j = open('vars.txt', 'rb')
        while True:
            try:
                display.append(pickle.load(j))
            except EOFError:
                break
        j.close()
        print('API ID,  API Hash,  Phone')
        print('\n')
        for z in display:
            print(z)
        input('\nPress enter to goto main menu')

    elif a == 5:
        accs = []
        f = open('vars.txt', 'rb')
        while True:
            try:
                accs.append(pickle.load(f))
            except EOFError:
                break
        f.close()
        i = 0
        print(f'{lg}[i] Choose an account to delete')
        for acc in accs:
            print(f'{lg}[{i}] {acc}{n}')
            i += 1
        index = int(input(f'{lg}[+] Enter a choice: {n}'))
        phone = str(accs[index][2])
        session_file = phone + '.session'
        if os.name == 'nt':
            os.system(f'del {session_file}')
        else:
            os.system(f'rm {session_file}')
        del accs[index]
        f = open('vars.txt', 'wb')
        for account in accs:
            pickle.dump(account, f)
        print(f'\n{lg}[+] Account Deleted{n}')
        input(f'{lg}Press enter to goto main menu{n}')
        f.close()
