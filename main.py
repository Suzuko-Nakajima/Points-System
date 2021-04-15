import asyncio
import os
import sys
import platform
import json
import time
import datetime

if not os.path.exists('assets/users'):
    os.mkdir('assets')
    os.mkdir('assets/users')

slash = '/'

points = 0

deposit = 0

luck = 3

sign_in_id = None

charlimit = 16

healing_aura = 0

healing_aura_stock = 10

def sign_in_function():
    global username
    global sign_in_id
    global charlimit
    sign_in_option = input("Choose (1. Sign-in | 2. Sign-up): ")
    if int(sign_in_option) == 1:
        sign_in_id = input("[Sign-in] | Enter sign-in ID: ")
        if not os.path.exists('assets/users/{}/sign_in_data.json'.format(sign_in_id)):
            print("ERROR: This account isn't a registered user!, feel free to claim!")
            exit()
        elif os.path.exists('assets/users/{}/sign_in_data.json'.format(sign_in_id)):
            pass
        with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'r+') as file:
            jsonData = json.load(file)

            if sign_in_id != jsonData['sign-in ID']:
                print('ERROR: Invalid login.')
                exit()
            elif sign_in_id == jsonData['sign-in ID']:
                username = jsonData['username']
                password = input("[Sign-in - {}] | Enter password: ".format(jsonData['username']))
                if password != jsonData['password']:
                    print('ERROR: Invalid password!')
                    exit()
                elif password == jsonData['password']:
                    print("Welcome back, {}!".format(jsonData['username']))
    elif int(sign_in_option) == 2:
        sign_in_id = input("[Sign-up] | Create unique sign-in ID: ")
        if len(sign_in_id) > charlimit:
            print('ERROR: Your sign-in ID cannot exceed over {} character(s).'.format(charlimit))
            exit()
        elif len(sign_in_id) <= charlimit:
            username = input("[Sign-up] | Choose username: ")
            password = input("[Sign-up - {}] | Enter password: ".format(username))

            if not os.path.exists('assets/users/{}'.format(sign_in_id)):
                os.mkdir('assets/users/{}'.format(sign_in_id))
            elif os.path.exists('assets/users/{}'.format(sign_in_id)):
                print('ERROR: Sign-in ID already exists. Please create a different sign-in ID.')
                exit()

            with open('assets/users/{}/save_data.json'.format(sign_in_id), 'x') as file:
                file.close()

            sign_in_data = {
                "username": username,
                "password": password,
                "sign-in ID": sign_in_id,
                "user ID": id(sign_in_id)
                }

            with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'w+') as file:
                json.dump(sign_in_data, file, indent = 4, sort_keys = True)
    


sign_in_function()



gift_codes = ["S19N"]

if not os.path.exists('assets/users'):
    os.mkdir('assets/users')
elif os.path.exists('assets/users'):
    pass


def initiateProgram():
    progress = 0
    for i in range(100):
        progress = progress + 1 * 20
        print('Loading...' + str(progress) + '%')
        time.sleep(.04)

        if progress >= 100:
            break

def bonus_points():
    global points
    points = points + 100
    print('You have received', points, 'bonus points!')

def reward():
    global points
    global luck

    if luck <= 0:
        print('Your ran out of luck, {}...'.format(username))
    else:
        luck = luck - 1
        points = points + 50

        print('Your point balance is now {0}, {1}.'.format(points, username))

def depos():
    global points
    global deposit
    deposit_in_bank = input("How much would you like to deposit?\n{}: ".format(username))

    if int(deposit_in_bank) > points:
        print('\nERROR: You cannot deposit more than what you have!\nYour point balance is: {}\n'.format(points))
    elif int(deposit_in_bank) < 1:
        print('\nERROR: You cannot deposit any points below 1!\nYour point balance is: {}\n'.format(points))
    else:
        deposit = deposit + int(deposit_in_bank)
        points = points - int(deposit_in_bank)

        print('\nPoint balance: {0}\nDeposited: {1}\n'.format(points, deposit))

def withdraw():
    global points
    global deposit

    withdraw_from_bank = input("How much would you like to withdraw?\nYour deposited points: {0}\n{1}: ".format(deposit, username))

    if int(withdraw_from_bank) > deposit:
        print('\nERROR: You cannot withdraw more than you have deposited!\n')
    elif int(withdraw_from_bank) < 1:
        print('\nERROR: You cannot withdraw points less than 1.\n')
    else:
        points = points + int(withdraw_from_bank)
        deposit = deposit - int(withdraw_from_bank)
        print('\nYour current point balance: {0}\nYour deposited points: {1}\n'.format(points, deposit))

def gift_code():
    global username
    global points
    code = input("Enter gift code.\n{}: ".format(username))

    with open('giftcode.json', 'r+') as file:
        jsonData = json.load(file)

        if code == jsonData['code']:
            points = points + 750
            print('You have received extra points!\nYour new total is points is: {}'.format(points))

            used_code = {}

            with open('giftcode.json', 'w+') as file:
                json.dump(used_code, file)
        elif code != jsonData['code']:
            print('This is not a valid gift code!')
def command_help():
    print('\nAvailable commands:\n{0}balance - Check your point balance and deposited points.\n{0}claim - Claim 50 points.\n{0}deposit - Deposit your points.\n{0}gift - Enter a gift code to receive some points.\n{0}load - Load your saved data (data is based on username).\n{0}logout - Closes the program.\n{0}uuid - View your unique ID.\n{0}uun - Update your username.\n{0}purchase - Purchase an item.\n{0}save - Save your data (data is based on username).\n{0}shop - View a list of items in the shop.\n{0}update_slash - Updates the current slash command. | NOTE: When you update the prefix, do not forget it!\n{0}update_password - Update your current password to a new password.\n{0}withdraw - Withdraw your points.\n'.format(slash))

def save_data():
    if not os.path.exists('assets/users/{}'.format(sign_in_id)):
        # Create a save path.
        print('\nUse the save command again to save your progress, {}.\n'.format(username))
        os.mkdir('assets/users/{}'.format(sign_in_id))
    elif os.path.exists('assets/users/{}'.format(sign_in_id)):
        # If save path exists, save current data.
        jsonData = {
            "healing aura": healing_aura,
            "healing aura stock": healing_aura_stock,
            "username": username,
            "points": points,
            "deposit": deposit,
            "luck": luck,
            "slash command prefix": slash
            }

        with open('assets/users/{}/save_data.json'.format(sign_in_id), 'w+') as file:
            json.dump(jsonData, file, indent = 4)
            print('\nYour data has been saved, {}!\n'.format(username))

def load_data():
    global healing_aura
    global healing_aura_stock
    global username
    global points
    global deposit
    global luck
    global slash
    global sign_in_id
    # If save path does not exist, load data cannot be found and an error message is displayed.
    if not os.path.exists('assets/users/{}'.format(sign_in_id)):
        print('\nERROR: Saved data for ({}) is nowhere to be found in this program.\n'.format(username))
    elif os.path.exists('assets/users/{}'.format(sign_in_id)):
        # If save path exists and has data, all data will be loaded (Depending on the username).
        with open('assets/users/{}/save_data.json'.format(sign_in_id), 'r+') as file:
            data = json.load(file)

            healing_aura = data['healing aura']
            healing_aura_stock = data['healing aura stock']
            username = data['username']
            points = data['points']
            deposit = data['deposit']
            luck = data['luck']
            slash = data['slash command prefix']

            print('\nAll your data has been loaded, {}!\n'.format(username))

            file.close()

def update_slash_command():
    global slash
    new_slash = input("Enter your prefered command prefix.\nExample: /\nNew prefix | {}: ".format(username))
    confirm_new_slash = input("Are you sure you want '{0}' to be your new prefix? Once this change is made, you must not forget it.\n(1. Yes | 2. No) | {1}: ".format(new_slash, username))
    if int(confirm_new_slash) == 1:
        slash = new_slash
        print('Your slash command prefix has been updated to: {}'.format(slash))
    elif int(confirm_new_slash) == 2:
        print('Operation cancelled. Your current prefix is: {}'.format(slash))

def update_password():
    confirm_current_password = input("Enter your current password: ")
    with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'r+') as file:
        jsonData = json.load(file)

        userID = jsonData['user ID']
                
        if confirm_current_password == jsonData['password']:
            new_password = input("Enter new password: ")

            with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'w+') as file:

                    
                updated_password = {
                    "username": username,
                    "password": new_password,
                    "sign-in ID": sign_in_id,
                    "user ID": userID
                    }

                json.dump(updated_password, file, indent = 4, sort_keys = True)

                print('Your password has been updated!\nNew password: {}'.format(new_password))
        elif confirm_current_password != jsonData['password']:
            print('ERROR: Password does not match!')

def logout():
    confirm_logout = input("\nMake sure all your progress is saved!\nAre you sure you want to log out?\n(1. Yes | 2. No): ")
    if int(confirm_logout) == 1:
        print('Logging out...')
        exit()
    elif int(confirm_logout) == 2:
        print('Logout cancelled.')
    elif int(confirm_logout) != 1 or int(confirm_logout) != 2:
        print('This not a valid option, you only have two.')
    else:
        print('Unknown error.')

def my_id():
    with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'r+') as file:
        my_data = json.load(file)

        print('Your unique user ID is:', my_data['user ID'])
        file.close()

def uun():
    global sign_in_id
    global username
    confirm_password = input("Enter password to proceed: ")
    with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'r+') as file:
        jsonData = json.load(file) 
        if confirm_password == jsonData['password']:
            new_username = input("[{}] | Enter new username: ".format(username))

            new_data = {
                "username": new_username,
                "password": jsonData['password'],
                "user ID": jsonData['user ID'],
                "sign-in ID": jsonData['sign-in ID']
            }

            with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'w+') as file:
                json.dump(new_data, file, indent = 4, sort_keys = True)
            print('Finished! (1/2)')
            file.close()

            with open('assets/users/{}/save_data.json'.format(sign_in_id), 'r+') as file:
                json_saveData = json.load(file)

                new_save_data = {
                    "username": new_username,
                    "deposit": json_saveData['deposit'],
                    "points": json_saveData['points'],
                    "luck": json_saveData['luck'],
                    "slash command prefix": json_saveData['slash command prefix']
                }

                with open('assets/users/{}/save_data.json'.format(sign_in_id), 'w+') as file:
                    json.dump(new_save_data, file, indent = 4, sort_keys = True)
                    file.close()

                    print('Username updated sucessfully! (2/2)')
        elif confirm_password != jsonData['password']:
            print('ERROR: Password is incorrect.')

def shop():
    print('Items:\n\n1. Healing Aura')

def purchase():
    global healing_aura
    global healing_aura_stock
    global points
    global username
    purchase_command_line = input("Know the item you want to purchase.\nPurchase item: ")
    if int(purchase_command_line) == 1:
        item = "Healing Aura"
        if healing_aura_stock < 1:
            print('ERROR: This item is out of stock!')
        elif points < 75:
            print('ERROR: You do not have a sufficient amount of funds!')
        elif not healing_aura_stock < 1 and not points < 75:
            healing_aura_stock = healing_aura_stock - 1
            healing_aura = healing_aura + 1
            points = points - 75

            print('-75 points!\nThank you for your purchase, {0}!\n+1 {1}'.format(username, item))

    else:
        pass



def console():
    global username
    global points
    global deposit
    global luck
    global slash
    global sign_in_id
    while True:
        terminal = input(username + ": ")

        if terminal == slash:
            print('\nThis is the only command prefix. Slash commands are availabe in this script.\nType \"{}help\" to see all available commands.\n'.format(slash))
        elif terminal == slash + 'help':
            # Displays available commands.
            command_help()
        elif terminal == slash + 'claim':
            # Claims a reward, limited to three.
            reward()
        elif terminal == slash + 'balance':
            print('\nYour total point balance is: {0}\nYour deposited points: {1}\n'.format(points, deposit))
        elif terminal == slash + 'deposit':
            depos()
        elif terminal == slash + 'withdraw':
            withdraw()
        elif terminal == slash + 'save':
            # Save the current data.
            save_data()

        elif terminal == slash + 'load':
            # Load the current data.
            load_data()
        elif terminal == slash + 'gift':
            gift_code()
        elif terminal == slash + 'logout':
            # Closes the program.
            logout()
        elif terminal == slash + 'purchase':
            purchase()
        elif terminal == slash + 'shop':
            shop()
        elif terminal == slash + 'update_slash':
            # Updates the slash command prefix.
            update_slash_command()
        elif terminal == slash + 'update_password':
            update_password()
        elif terminal == slash + 'uuid':
            my_id()
        elif terminal == slash + 'uun':
            uun()




initiateProgram()
bp = input("\nYour point balance (PB) is {}. Would you like to claim bonus points?\n(1. Yes | 2. No): ".format(points))
if int(bp) == 1:
    bonus_points()
elif int(bp) == 2:
    print('\nYou declined the bonus points, your point balance is {}.'.format(points))

console()