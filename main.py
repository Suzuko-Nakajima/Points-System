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

claim_luck = 3

def sign_in_function():
    global username
    sign_in_option = input("Choose (1. Sign-in | 2. Sign-up): ")
    if int(sign_in_option) == 1:
        username = input("[Sign-in] | Enter username: ")
        with open('assets/users/{}/sign_in_data.json'.format(username), 'r+') as file:
            jsonData = json.load(file)

            if username != jsonData['username']:
                print('ERROR: Invalid username.')
                exit()
            elif username == jsonData['username']:
                password = input("[Sign-in - {}] | Enter password: ".format(username))
                if password != jsonData['password']:
                    print('ERROR: Invalid password!')
                    exit()
                elif password == jsonData['password']:
                    print("Welcome back, {}!".format(username))
    elif int(sign_in_option) == 2:
        username = input("[Sign-up] | Enter username: ")
        password = input("[Sign-up - {}] | Enter password: ".format(username))

        if not os.path.exists('assets/users/{}'.format(username)):
            os.mkdir('assets/users/{}'.format(username))
        elif os.path.exists('assets/users/{}'.format(username)):
            pass

        with open('assets/users/{}/save_data.json'.format(username), 'x') as file:
            file.close()

        sign_in_data = {
            "username": username,
            "password": password,
            "user ID": id(username)
            }

        with open('assets/users/{}/sign_in_data.json'.format(username), 'w+') as file:
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
    global claim_luck

    if claim_luck <= 0:
        print('Your ran out of luck, {}...'.format(username))
    else:
        claim_luck = claim_luck - 1
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
    print('\nAvailable commands:\n{0}balance - Check your point balance and deposited points.\n{1}claim - Claim 50 points.\n{2}deposit - Deposit your points.\n{3}gift - Enter a gift code to receive some points.\n{4}load - Load your saved data (data is based on username).\n{5}logout - Closes the program.\n{6}save - Save your data (data is based on username).\n{7}update_slash - Updates the current slash command. | NOTE: When you update the prefix, do not forget it!\n{8}update_password - Update your current password to a new password.\n{9}withdraw - Withdraw your points.\n'.format(slash, slash, slash, slash, slash, slash, slash, slash, slash, slash))


def console():
    global username
    global points
    global deposit
    global claim_luck
    global slash
    while True:
        terminal = input(username + ": ")

        if terminal == slash:
            print('\nThis is the only command prefix. Slash commands are availabe in this script.\nType \"/help\" to see all available commands.\n')
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
            if not os.path.exists('assets/users/{}'.format(username)):
                # Create a save path.
                print('\nUse the save command again to save your progress, {}.\n'.format(username))
                os.mkdir('assets/users/{}'.format(username))
            elif os.path.exists('assets/users/{}'.format(username)):
                # If save path exists, save current data.
                jsonData = {
                    "username": username,
                    "points": points,
                    "deposit": deposit,
                    "claim luck": claim_luck,
                    "slash command prefix": slash
                    }

                with open('assets/users/{}/save_data.json'.format(username), 'w+') as file:
                    json.dump(jsonData, file, indent = 4)
                    print('\nYour data has been saved, {}!\n'.format(username))

        elif terminal == slash + 'load':
            # If save path does not exist, load data cannot be found and an error message is displayed.
            if not os.path.exists('assets/users/{}'.format(username)):
                print('\nERROR: Saved data for ({}) is nowhere to be found in this program.\n'.format(username))
            elif os.path.exists('assets/users/{}'.format(username)):
                # If save path exists and has data, all data will be loaded (Depending on the username).
                with open('assets/users/{}/save_data.json'.format(username), 'r+') as file:
                    data = json.load(file)

                    username = data['username']
                    points = data['points']
                    deposit = data['deposit']
                    claim_luck = data['claim luck']
                    slash = data['slash command prefix']

                    print('\nAll your data has been loaded, {}!\n'.format(username))
        elif terminal == slash + 'gift':
            gift_code()
        elif terminal == slash + 'logout':
            # Closes the program.
            print('Logging out...')
            exit()
        elif terminal == slash + 'update_slash':
            new_slash = input("Enter your prefered command prefix.\nExample: /\nNew prefix | {}: ".format(username))
            confirm_new_slash = input("Are you sure you want '{0}' to be your new prefix? Once this change is made, you must not forget it.\n(1. Yes | 2. No) | {1}: ".format(new_slash, username))
            if int(confirm_new_slash) == 1:
                slash = new_slash
                print('Your slash command prefix has been updated to: {}'.format(slash))
            elif int(confirm_new_slash) == 2:
                print('Operation cancelled. Your current prefix is: {}'.format(slash))
        elif terminal == slash + 'update_password':
            confirm_current_password = input("Enter your current password: ")
            with open('assets/users/{}/sign_in_data.json'.format(username), 'r+') as file:
                jsonData = json.load(file)

                userID = jsonData['user ID']
                
                if confirm_current_password == jsonData['password']:
                    new_password = input("Enter new password: ")

                    with open('assets/users/{}/sign_in_data.json'.format(username), 'w+') as file:

                    
                        updated_password = {
                            "username": username,
                            "password": new_password,
                            "user ID": userID
                        }

                        json.dump(updated_password, file, indent = 4, sort_keys = True)

                    print('Your password has been updated!\nNew password: {}'.format(new_password))
                elif confirm_current_password != jsonData['password']:
                    print('ERROR: Password does not match!')



initiate = input("Ready to start the program?\n(1. Yes | 2. No): ")
if int(initiate) == 1:
    initiateProgram()
    bp = input("\nYour point balance (PB) is {}. Would you like to claim bonus points?\n(1. Yes | 2. No): ".format(points))
    if int(bp) == 1:
        bonus_points()
    elif int(bp) == 2:
        print('\nYou declined the bonus points, your point balance is {}.'.format(points))

    console()
elif int(initiate) == 2:
    print('Cancelled.')