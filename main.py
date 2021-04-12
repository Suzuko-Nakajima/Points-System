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


username = input("Enter username: ")

if not os.path.exists('assets/users'):
    os.mkdir('assets/users')
elif os.path.exists('assets/users'):
    pass


def initiateProgram():
    progress = 0
    for i in range(100):
        progress = progress + 1 * 10
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


def console():
    global username
    global deposit
    global points
    global claim_luck
    while True:
        terminal = input(username + ": ")

        if terminal == slash:
            print('This is the only command prefix. Slash commands are availabe in this script.\nType \"/help\" to see all available commands.')
        elif terminal == slash + 'help':
            print('\nAvailable commands:\n/balance - Check your point balance and deposited points.\n/claim - Claim 50 points.\n/deposit - Deposit your points.\n/load - Load your saved data (data is based on username).\n/logout - Closes the program.\n/save - Save your data (data is based on username).\n/withdraw - Withdraw your points.\n')
        elif terminal == slash + 'claim':
            reward()
        elif terminal == slash + 'balance':
            print('Your total point balance is: {0}\nYour deposited points: {1}'.format(points, deposit))
        elif terminal == slash + 'deposit':
            depos()
        elif terminal == slash + 'withdraw':
            withdraw()
        elif terminal == slash + 'save':
            if not os.path.exists('assets/users/{}'.format(username)):
                print('Use the save command again to save your progress, {}.'.format(username))
                os.mkdir('assets/users/{}'.format(username))
            elif os.path.exists('assets/users/{}'.format(username)):
                jsonData = {
                    "username": username,
                    "points": points,
                    "deposit": deposit,
                    "claim luck": claim_luck
                    }

                with open('assets/users/{}/save_data.json'.format(username), 'w+') as file:
                    json.dump(jsonData, file, indent = 4)
                    print('Your data has been saved, {}!'.format(username))

        elif terminal == slash + 'load':
            with open('assets/users/{}/save_data.json'.format(username), 'r+') as file:
                data = json.load(file)

                username = data['username']
                points = data['points']
                deposit = data['deposit']
                claim_luck = data['claim luck']

            print('All your data has been loaded, {}!'.format(username))
        elif terminal == slash + 'logout':
            print('Logging out...')
            exit()



initiate = input("Ready to start the program?\n(1. Yes | 2. No): ")
if int(initiate) == 1:
    initiateProgram()
    bp = input("Your point balance (PB) is {}. Would you like to claim bonus points?\n(1. Yes | 2. No): ".format(points))
    if int(bp) == 1:
        bonus_points()
    elif int(bp) == 2:
        print('You declined the bonus points, your point balance is {}.'.format(points))

    console()
elif int(initiate) == 2:
    print('Cancelled.')