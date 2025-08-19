import secrets
import string
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from stdiomask import getpass
import json
import pyperclip


DATA_FILE = "vault.enc"
SALT_FILE = 'salt.bin'
LOCALES_DIR = "locales"

LANGUAGES = {
    'ru': {'name': 'Русский', 'file': 'ru.json'},
    'en': {'name': 'English', 'file': 'en.json'}
}

current_language = None


def select_languages():
    print('Выберите язык | Select Languages\n')
    languages = list(LANGUAGES.items())
    while True:
        for i, (code, lang) in enumerate(languages, start=1):
                print(f'{i}: {lang.get("name")}')
        try:
            choice = int(input('> ')) - 1
            return languages[choice][1].get('file')
        except Exception as e:
            print(e)
            print("\nНеверный выбор. Попробуйте снова / Invalid choice. Try again\n")


def load_language(file):
    with open(f'locales/{file}', 'r') as f:
        return json.load(f)


def initialization():
    if not os.path.exists(DATA_FILE):
        print(current_language.get('initialization_start_message'))
        master_password = getpass(prompt=current_language.get('master_password_prompt'), mask='*')
        salt = secrets.token_bytes(32)
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)
        key = PBKDF2(master_password, salt, dkLen=32, count=100000)
        vault = {}
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(json.dumps(vault).encode(), AES.block_size))
        with open(DATA_FILE, 'wb') as f:
            f.write(cipher.iv + ct_bytes)
        print(current_language.get('initialization_storage_create'))
    else:
        print(current_language.get('initialization_storage_created'))


def load_vault():
    master_password = getpass(current_language.get('master_password_prompt'), mask='*')
    with open(SALT_FILE, 'rb') as f:
        salt = f.read()
    key = PBKDF2(master_password, salt, dkLen=32, count=100000)
    with open(DATA_FILE, 'rb') as f:
        data = f.read()
        IV = data[:16]
        CT = data[16:]
    try:
        cypher = AES.new(key, AES.MODE_CBC, IV)
        pt = unpad(cypher.decrypt(CT), AES.block_size)
        q = json.loads(pt.decode())
        if q:
            keys = list(q.keys())
            print(current_language.get('load_service_prompt'))
            for i in range(len(keys)):
                print(f'{i+1}: {keys[i]}')
            i = int(input('\n>'))-1
            print(current_language.get('service_prompt'), ''.join([keys[i]]))
            print(current_language.get('login_prompt'), q[keys[i]].get('login'))
            print(current_language.get('password_prompt'), q[keys[i]].get('password'))
            return
        else:
            print(current_language.get('load_vault_no_password'))
    except Exception as e:
        print(e)
        print(current_language.get('wrong_password'))
        return
    

def get_service_name():
    while True:
        service = input(current_language.get('service_prompt'))
        if service.strip():
            return service.strip()
        print(current_language.get('service_empty_error'))

def get_login():
    while True:
        login = input(current_language.get('login_prompt'))
        if login.strip():
            return login.strip()
        print(current_language.get('login_empty_error'))

def get_password_length():
    while True:
        try:
            length = int(input(current_language.get('password_length_prompt')))
            if length >= 8:
                return length
            print(current_language.get('password_length_error'))
        except ValueError:
            print(current_language.get('password_length_invalid'))


def add_password():
    try:
        master_password = getpass(current_language.get('master_password_prompt'), mask='*')
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()
        key = PBKDF2(master_password, salt, dkLen=32, count=100000)
        
        with open(DATA_FILE, 'rb') as f:
            data = f.read()
            iv = data[:16]
            ct = data[16:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        vault = json.loads(pt.decode())
        
    except:
        print(current_language.get('wrong_password'))
        return
    
    while True:
        print("\n" + current_language.get('add_password_menu'))
        print("1. " + current_language.get('enter_service'))
        print("2. " + current_language.get('enter_login')) 
        print("3. " + current_language.get('set_password_length'))
        print("4. " + current_language.get('save_and_exit'))
        print("0. " + current_language.get('cancel'))
        
        choice = input("\n> ")
        
        if choice == '1':
            service = get_service_name()
        elif choice == '2':
            login = get_login()
        elif choice == '3':
            password_length = get_password_length()
            password = generate_password(password_length)
        elif choice == '4':
            if 'service' not in locals() or 'login' not in locals() or 'password' not in locals():
                print(current_language.get('fields_not_filled'))
                continue
            else:
                print(current_language.get('confirm_details'))
                print(current_language.get('service_prompt'), service)
                print(current_language.get('login_prompt'), login)
                print(current_language.get('password_length_prompt_details'), len(password))
                print(current_language.get('confirm_save'))
                confirm_save = input('> ')
            if confirm_save == 'y':
                vault[service] = {'login': login, 'password': password}
                
                cipher = AES.new(key, AES.MODE_CBC)
                ct_bytes = cipher.encrypt(pad(json.dumps(vault).encode(), AES.block_size))
                with open(DATA_FILE, 'wb') as f:
                    f.write(cipher.iv + ct_bytes)
                pyperclip.copy(password)
                print(current_language.get('password_saved'))
                return
            else:
                continue
            
        elif choice == '0':
            print(current_language.get('operation_cancelled'))
            return
        else:
            print(current_language.get('invalid_choice'))
    

def generate_password(password_length=50):
    password = []
    for _ in range(password_length):
        password += secrets.choice(string.ascii_letters+'0123456789!@#$%*&-_=+/?.,')
    for i in range(password_length-1, 0, -1):
        j = secrets.randbelow(password_length)
        password[i], password[j] = password[j], password[i]
    password = ''.join(password)
    return password
        
        
def main():
    global current_language
    with open('logo.txt', 'r') as f:
        print(f.read())
    
    current_language = load_language(select_languages())

    initialization()
    
    choice = None
    while choice != '0':
        print(current_language.get('main_menu_choice'))
        choice = input('> ')
        if choice == '1':
            load_vault()
        elif choice == '2':
            add_password()
        elif choice == '0':
            print(current_language.get('exit_message'))
        else:
            print(current_language.get('main_menu_error'))


if __name__ == "__main__":
    main()
