import asyncio
import os
import sys
import platform
import json
import random
import time
import datetime
import uuid
from nakacmdline import cmdlinetxtcolors as c
from nakacmdline import people as p
from nakacmdline import battlePhases as bp

if not os.path.exists('assets/users'):
    os.mkdir('assets')
    os.mkdir('assets/users')

slash = '/'

stamina_points = float(100.0)

battle_xp = 0

points = 0

deposit = 0

luck = 10

sign_in_id = None

charlimit = 16

enhanced_arrows = 0

healing_aura = 0

healing_aura_stock = 50

iron_sword = 0

iron_sword_durability = 0

logout_dialogue = 1

silver_sword = 0
silver_sword_durability = 0

bow = 0
bow_durability = 0
arrows = 0

tipped_arrows = 0

def sign_in_function():
    global battle_xp
    global username
    global sign_in_id
    global charlimit
    global points
    global deposit
    global enhanced_arrows
    global healing_aura
    global healing_aura_stock
    global iron_sword
    global iron_sword_durability
    global stamina_points
    global silver_sword
    global silver_sword_durability
    global tipped_arrows
    global bow
    global bow_durability
    global arrows
    sign_in_option = input("Choose (1. Sign-in | 2. Sign-up): ")
    if int(sign_in_option) == 1:
        sign_in_id = input("[Sign-in] | Enter sign-in ID: ")
        if not os.path.exists('assets/users/{}/sign_in_data.json'.format(sign_in_id)):
            print("{0}ERROR: This account isn't a registered user!, feel free to claim!{1}".format(c.tcolors.yellow, c.tcolors.reset))
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
                    file.close()



    elif int(sign_in_option) == 2:
        sign_in_id = input("[Sign-up] | Create unique sign-in ID: ")
        if len(sign_in_id) > charlimit:
            print('{0}ERROR: Your sign-in ID cannot exceed over {1} character(s)!{2}'.format(c.tcolors.red, charlimit, c.tcolors.reset))
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

            UUID = uuid.uuid4()
            userID = str(UUID)

            sign_in_data = {
                "username": username,
                "password": password,
                "sign-in ID": sign_in_id,
                "user ID": userID
                }

            with open('assets/users/{}/sign_in_data.json'.format(sign_in_id), 'w+') as file:
                json.dump(sign_in_data, file, indent = 4, sort_keys = True)

                print(f"\n{c.tcolors.cyan}???: A newcomer?{c.tcolors.reset}\n")
                time.sleep(3)
                print(f"\n{c.tcolors.cyan}???: You\'re probably new to the command line, at least this one.\n\n???: Before I let you go, do not forget about slash commands, they are available every time you sign-in. I will not overwhelm you with all the details, I will help along the way.{c.tcolors.reset}\n")
                time.sleep(7)
                print(f"\n{c.tcolors.cyan}???: When you load in your data from a save file, you take damage and lose stamina points. Use the slash command, find \'shop\' and find the Healing Aura.\n???: Use it to regain some stamina points.{c.tcolors.reset}\n")
                time.sleep(5)
                print(f"\n{c.tcolors.green}[Guide obtained: Luaren]\n{c.tcolors.reset}")
                time.sleep(10)
                print(f"{c.tcolors.red}NOTICE: If your stamina points drop to 0, you will no longer be able to sign into your make-shift account!{c.tcolors.reset}")
    


sign_in_function()



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
    points = points + 500
    print('You have received', points, 'bonus points!')

def reward():
    global points
    global luck

    if luck <= 0:
        print('Your ran out of luck, {}...'.format(username))
    else:
        lucky_points = random.randint(20, 80)
        luck = luck - 1
        points = points + lucky_points

        print('Your point balance is now {0}, {1}.'.format(points, username))

def depos():
    global points
    global deposit
    deposit_in_bank = input("How much would you like to deposit?\n{}: ".format(username))

    if int(deposit_in_bank) > points:
        print('\n{0}ERROR: You cannot deposit more than what you have!{1}\nYour point balance is: {2}\n'.format(c.tcolors.red, c.tcolors.reset, points))
    elif int(deposit_in_bank) < 1:
        print('\n{0}ERROR: You cannot deposit any points below 1!{1}\nYour point balance is: {2}\n'.format(c.tcolors.red, c.tcolors.reset, points))
    else:
        deposit = deposit + int(deposit_in_bank)
        points = points - int(deposit_in_bank)

        print('\nPoint balance: {0}\nDeposited: {1}\n'.format(points, deposit))

def withdraw():
    global points
    global deposit

    withdraw_from_bank = input("How much would you like to withdraw?\nYour deposited points: {0}\n{1}: ".format(deposit, username))

    if int(withdraw_from_bank) > deposit:
        print('\n{0}ERROR: You cannot withdraw more than you have deposited!{1}\n'.format(c.tcolors.red, c.tcolors.reset))
    elif int(withdraw_from_bank) < 1:
        print('\n{0}ERROR: You cannot withdraw points less than 1.{1}\n'.format(c.tcolors.red, c.tcolors.reset))
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
            points = points + 1000
            print('You have received extra points!\nYour new total is points is: {}'.format(points))

            used_code = {}

            with open('giftcode.json', 'w+') as file:
                json.dump(used_code, file)
        elif code != jsonData['code']:
            print('This is not a valid gift code!')

def command_help():
    print('\nAvailable commands:\n{0}balance - Check your point balance and deposited points.\n{0}battle - begin battling for experience!\n{0}claim - Claim 50 points.\n{0}deposit - Deposit your points.\n{0}gift - Enter a gift code to receive some points.\n{0}inventory - View your inventory.\n{0}load - Load your saved data (data is based on username).\n{0}logout - Closes the program.\n{0}uuid - View your unique ID.\n{0}uun - Update your username.\n{0}purchase - Purchase an item.\n{0}save - Save your data (data is based on sign-in ID).\n{0}shop - View a list of items in the shop.\n{0}update_slash - Updates the current slash command. | NOTE: When you update the prefix, do not forget it!\n{0}update_password - Update your current password to a new password.\n{0}use - Use any items in your inventory.\n{0}withdraw - Withdraw your points.\n'.format(slash))

def save_data():
    if not os.path.exists('assets/users/{}'.format(sign_in_id)):
        # Create a save path.
        print('\nUse the save command again to save your progress, {}.\n'.format(username))
        os.mkdir('assets/users/{}'.format(sign_in_id))
    elif os.path.exists('assets/users/{}'.format(sign_in_id)):
        # If save path exists, save current data.
        jsonData = {
            "arrows": arrows,
            "battle xp": battle_xp,
            "bow": bow,
            "bow durability": bow_durability,
            "enhanced arrows": enhanced_arrows,
            "healing aura": healing_aura,
            "healing aura stock": healing_aura_stock,
            "iron sword": iron_sword,
            "iron sword durability": iron_sword_durability,
            "logout dialogue": logout_dialogue,
            "username": username,
            "points": points,
            "deposit": deposit,
            "luck": luck,
            "silver sword": silver_sword,
            "silver sword durability": silver_sword_durability,
            "slash command prefix": slash,
            "stamina points": stamina_points,
            "tipped arrows": tipped_arrows
            }

        with open('assets/users/{}/save_data.json'.format(sign_in_id), 'w+') as file:
            json.dump(jsonData, file, indent = 4)
            print('\nYour data has been saved, {}!\n'.format(username))

def load_data():
    global arrows
    global battle_xp
    global bow
    global bow_durability
    global enhanced_arrows
    global healing_aura
    global healing_aura_stock
    global iron_sword
    global iron_sword_durability
    global username
    global points
    global deposit
    global luck
    global slash
    global sign_in_id
    global stamina_points
    global silver_sword
    global silver_sword_durability
    global tipped_arrows
    global logout_dialogue
    # If save path does not exist, load data cannot be found and an error message is displayed.
    if not os.path.exists('assets/users/{}'.format(sign_in_id)):
        print('\nERROR: Saved data for ({}) is nowhere to be found in this program.\n'.format(username))
    elif os.path.exists('assets/users/{}'.format(sign_in_id)):
        # If save path exists and has data, all data will be loaded (Depending on the username).
        with open('assets/users/{}/save_data.json'.format(sign_in_id), 'r+') as file:
            data = json.load(file)

            damage = random.uniform(10, 25)

            arrows = data['arrows']
            battle_xp = data['battle xp']
            bow = data['bow']
            bow_durability = data['bow durability']
            enhanced_arrows = data['enhanced arrows']
            healing_aura = data['healing aura']
            healing_aura_stock = data['healing aura stock']
            iron_sword = data['iron sword']
            iron_sword_durability = data['iron sword durability']
            logout_dialogue = data['logout dialogue']
            username = data['username']
            points = data['points']
            deposit = data['deposit']
            luck = data['luck']
            silver_sword = data['silver sword']
            silver_sword_durability = data['silver sword durability']
            slash = data['slash command prefix']
            stamina_points = data['stamina points'] - damage
            tipped_arrows = data['tipped arrows']

            if stamina_points <= 0:
                print('{0}ERROR: You no longer have enough stamina points to load in your data.{1}\nStamina points: {2}%'.format(c.tcolors.red, c.tcolors.reset, stamina_points))
                exit()
            elif not stamina_points <= 0:
                print('\n{0}All your data has been loaded, {1}!{2}\n'.format(c.tcolors.green, username, c.tcolors.reset))

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
    global arrows
    global battle_xp
    global bow
    global bow_durability
    global enhanced_arrows
    global healing_aura
    global healing_aura_stock
    global iron_sword
    global iron_sword_durability
    global username
    global points
    global deposit
    global luck
    global slash
    global sign_in_id
    global stamina_points
    global tipped_arrows
    global logout_dialogue
    confirm_logout = input("\n{0}Make sure all your progress is saved!\nAre you sure you want to log out?\n(1. Yes | 2. No): {1}".format(c.tcolors.grey, c.tcolors.reset))
    if int(confirm_logout) == 1:
        if logout_dialogue >= 1:
            logout_dialogue = logout_dialogue - 1

            print('{0}{1}: I will not repeat myself, SAVE ALL YOUR DATA BEFORE LOGGGING OUT. I just cannot stress myself enough about that.\n\nNOTICE: If you have not saved your data yet, save it now and then use the logout command again.{2}\n\n'.format(c.tcolors.cyan, p.npc.lauren, c.tcolors.reset))
        elif logout_dialogue <= 0:
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
                    "arrows": json_saveData['arrows'],
                    "battle xp": json_saveData['battle xp'],
                    "bow": json_saveData['bow'],
                    "bow durability": json_saveData['bow durability'],
                    "enhanced arrows": json_saveData['enhanced arrows'],
                    "healing aura": json_saveData['healing aura'],
                    "healing aura stock": json_saveData['healing aura stock'],
                    "iron sword": json_saveData['iron sword'],
                    "iron sword durability": json_saveData['iron sword durability'],
                    "logout dialogue": json_saveData['logout dialogue'],
                    "username": new_username,
                    "deposit": json_saveData['deposit'],
                    "points": json_saveData['points'],
                    "luck": json_saveData['luck'],
                    "silver sword": json_saveData['silver sword'],
                    "silver sword durability": json_saveData['silver sword durability'],
                    "slash command prefix": json_saveData['slash command prefix'],
                    "stamina points": json_saveData['stamina points'],
                    "tipped arrows": json_saveData['tipped arrows']
                }

                with open('assets/users/{}/save_data.json'.format(sign_in_id), 'w+') as file:
                    json.dump(new_save_data, file, indent = 4, sort_keys = True)
                    file.close()

                    print('Username updated sucessfully! (2/2)')
        elif confirm_password != jsonData['password']:
            print('ERROR: Password is incorrect.')

def shop():
    print('Items:\n\n1. Healing Aura | [75]\n2. Iron sword | [150]\n3. Silver sword | [250]\n4. Bow [400]\n5. Arrows (regular) [50]\n6. Arrows (Enhanced) [100]\n7. Tipped arrows (Poison) [200]\n')

def purchase():
    global arrows
    global bow
    global bow_durability
    global enhanced_arrows
    global healing_aura
    global healing_aura_stock
    global iron_sword
    global iron_sword_durability
    global points
    global username
    global silver_sword
    global silver_sword_durability
    global tipped_arrows
    purchase_command_line = input("Know the item you want to purchase.\nPurchase item: ")
    if int(purchase_command_line) == 1:
        item = "Healing Aura"
        if healing_aura_stock < 1:
            print('\n{0}ERROR: This item is out of stock!{1}'.format(c.tcolors.red, c.tcolors.reset))
        elif points < 75:
            print('\n{0}ERROR: You do not have a sufficient amount of funds!{1}\n'.format(c.tcolors.red, c.tcolors.reset))
        elif not healing_aura_stock < 1 and not points < 75:
            healing_aura_stock = healing_aura_stock - 1
            healing_aura = healing_aura + 1
            points = points - 75

            print('-75 points!\nThank you for your purchase, {0}!\n+1 {1}'.format(username, item))
    elif int(purchase_command_line) == 2:
        item_iron_sword = "Iron sword"
        if points < 150:
            print('\n{0}ERROR: You do not have enough points to purchase this item.{1}\n | [{2}]'.format(c.tcolors.red, c.tcolors.reset, item_iron_sword))
        elif iron_sword > 0:
            print('\n{0}ERROR: You already have this item.{1}\n | [{2}]'.format(c.tcolors.red, c.tcolors.reset, item_iron_sword))
        elif not points < 150 and not iron_sword > 0:
            iron_sword = iron_sword + 1
            iron_sword_durability = iron_sword_durability + 1000
            points = points - 150

            print('-150 points!\nThank you for your purchase, {0}!\n+1 {1}'.format(username, item_iron_sword))
    elif int(purchase_command_line) == 3:
        item_silver_sword = 'Silver sword'
        if points < 250:
            print('\n{0}ERROR: You do not have a sufficient amount of points for this purchase.\nItem: {1}{2}\n'.format(c.tcolors.red, item_silver_sword, c.tcolors.reset))
        elif silver_sword > 0:
            print('\n{0}ERROR: You already have this item!\nItem: {1}{2}\n'.format(c.tcolors.red, item_silver_sword, c.tcolors.reset))
        elif not points < 250 and not silver_sword > 0:
            silver_sword = silver_sword + 1
            silver_sword_durability = silver_sword_durability + 2000
            points = points - 250

            print('-250 points!\nThank you for your purchase, {0}!\n+1 {1}'.format(username, item_silver_sword))
    elif int(purchase_command_line) == 4:
        item_bow = 'Bow'
        if points < 400:
            print('\n{0}ERROR: You do not have a sufficient amount of points for this purchase.\nItem: {1}{2}\n'.format(c.tcolors.red, item_bow, c.tcolors.reset))
        elif bow > 0:
            print('\n{0}ERROR: You already have this item!\nItem: {1}{2}\n'.format(c.tcolors.red, item_bow, c.tcolors.reset))
        elif not points < 400 and not bow > 0:
            bow = bow + 1
            bow_durability = bow_durability + 3000
            points = points - 400

            print('-400 points!\nThank you for your purchase, {0}!\n+1 {1}'.format(username, item_bow))
    elif int(purchase_command_line) == 5:
        item_arrows = 'Arrows'
        if points < 50:
            print('\n{0}ERROR: You do not have a sufficient amount of points for this purchase.\nItem: {1}{2}\n'.format(c.tcolors.red, item_arrows, c.tcolors.reset))
        elif not points < 400:
            arrows = arrows + 16
            points = points - 50

            print('-50 points!\nThank you for your purchase, {0}!\n+16 {1}'.format(username, item_arrows))
    elif int(purchase_command_line) == 6:
        en_arrows = 'Enhanced arrows'
        if points < 100:
            print('\n{0}ERROR: You do not have a sufficient amount of points for this purchase.\nItem: {1}{2}\n'.format(c.tcolors.red, en_arrows, c.tcolors.reset))
        elif not points < 100:
            enhanced_arrows = enhanced_arrows + 16
            points = points - 100

            print('-100 points!\nThank you for your purchase, {0}!\n+16 {1}'.format(username, en_arrows))
    elif int(purchase_command_line) == 7:
        item_tipped_arrows = 'Tipped arrows'
        if points < 250:
            print('\n{0}ERROR: You do not have a sufficient amount of points for this item.\nItem: {1}{2}\n'.format(c.tcolors.red, item_tipped_arrows, c.tcolors.reset))
        elif not points < 250:
            tipped_arrows = tipped_arrows + 16
            points = points - 250

            print('-250 points!\nThank you for your purchase, {0}!\n+16 {1}'.format(username, item_tipped_arrows))


    else:
        pass

def inventory():
    global arrows
    global bow
    global enhanced_arrows
    global healing_aura
    global iron_sword
    global iron_sword_durability
    global stamina_points
    global silver_sword
    global silver_sword_durability
    global tipped_arrows
    print('Inventory:\n\nHealing Aura: {0}\nIron sword: {1} [{2}]\nSilver sword: {3} [{4}]\nBow: {5} [{6}]\nArrows [Regular]: {7}\nArrows [Enhanced]: {8}\nTipped arrows [Poison]: {9}\n'.format(healing_aura, iron_sword, iron_sword_durability, silver_sword, silver_sword_durability, bow, bow_durability, arrows, enhanced_arrows, tipped_arrows))

def use_item():
    global healing_aura
    global stamina_points
    select_item = input("Select an item you would like to use (Remember the numbers next to the items).\nSelect item: ")
    if int(select_item) == 1:
        if stamina_points >= 100:
            print('ERROR: Your stamina is already maxed out!')
        elif healing_aura <= 0:
            print('You have no Healing Aura!')
        elif not stamina_points >= 100:
            healing_aura = healing_aura - 1
        
            random_heal = random.randint(15, 20)

            stamina_points = stamina_points + random_heal

            if stamina_points >= 100:
                stamina_points = 100
                print('Your stamina has been replinished to {}%!'.format(stamina_points))

def battleOptions():
    print(f"\n1. Training | Train against {p.npc.lauren}. [Recommended level: 16]\n2. Quit battle.\n3. Ruins Haven - Fight low-level thieves.\nMore options coming soon.\n")

def naka_battle_quotes():
    laurenBattleQuotes = random.choice([
        "I cannot allow myself to fall here!",
        "Just you wait!",
        "I will try not to disappoint you!",
        "Now it's my turn!",
        "I'll make this quick!",
        "I won't ask you to forgive me!",
        "I have no remorse!",
        "I will not hold back!",
        "This is as easy as it gets!"
    ])

    print('{0}{3}: {2} {1}'.format(c.tcolors.cyan, laurenBattleQuotes, c.tcolors.reset, p.npc.lauren))


def battle():
    global arrows
    global battle_xp
    global bow
    global bow_durability
    global enhanced_arrows
    global slash
    global points
    global username
    global iron_sword
    global iron_sword_durability
    global silver_sword
    global silver_sword_durability
    global tipped_arrows

    battleOptions()
    select = input("\nSelect a battle option!\n\n{}: ".format(username))

    if int(select) == 1:
        print('\n{0}{2}: Wanting to train against me, huh? Very well then, suppose i cannot back down now.{1}\n'.format(c.tcolors.cyan, c.tcolors.reset, p.npc.lauren))

        training_hp = 100
        naka_hp = 100

        print('\nYour health points as of now render for this session, as soon as your health points drop to 0%, that is game!\n')

        def training_laurenHP():
            global battle_xp
            global points
            nonlocal training_hp
            nonlocal naka_hp
            if naka_hp <= 0:
                time.sleep(3)
                print('{0}{1}: I guess you have bested me...well done.{2}'.format(c.tcolors.cyan, p.npc.lauren, c.tcolors.reset))

                training_bonus = 75
                points = points + training_bonus
                time.sleep(3)
                print('You have won against {0}!\n+{1} points!'.format(p.npc.lauren, training_bonus))
            elif not naka_hp <= 0:
                time.sleep(3)

                # Lauren's battle quotes.
                naka_battle_quotes()
                pavedEdge_damage = random.randint(15, 30)
                time.sleep(2)
                training_hp = training_hp - pavedEdge_damage
                if pavedEdge_damage >= 20:
                    print('{0}{1}CRITICAL HIT!{2}'.format(c.tcolors.red, c.tcolors.bold, c.tcolors.reset))
                elif not pavedEdge_damage >= 20:
                    pass

                print('{0}{1} attacked you using Paved Edge!\nDamage dealt: {2}%{3}'.format(c.tcolors.grey, p.npc.lauren, pavedEdge_damage, c.tcolors.reset))

        while training_hp > 0:
            if naka_hp <= 0:
                break
            elif not naka_hp <= 0:
                bp.player()
                training_prompt = input("1. Attack [Weapon: Iron sword]\n2. Forfeit\n3. Attack [Weapon: Silver sword]\n4. Attack [Weapon: Bow]\n\n[{0}%] | {1}\n[{2}%] | {3}: ".format(naka_hp, p.npc.lauren, training_hp, username))

                if int(training_prompt) == 1:
                    if iron_sword > 0:
                        point_gain = random.randint(10, 25)
                        iron_sword_damage = random.randint(5, 10)
                        iron_sword_durability_loss = random.randint(10, 25)

                        naka_hp = naka_hp - iron_sword_damage
                        iron_sword_durability = iron_sword_durability - iron_sword_durability_loss
                        battle_xp = battle_xp + 5
                        points = points + point_gain

                        print('{0}You attacked {1} using an iron sword!\Lauren\'s health points: {2}\n+{3} points!{4}'.format(c.tcolors.yellow, p.npc.lauren, naka_hp, point_gain, c.tcolors.reset))

                        # Enemy phase.
                        bp.enemy()
                        training_laurenHP()



                    elif not iron_sword > 0:
                        print('{0}ERROR: There are no available iron swords in your inventory. Purchase some from the shop!{1}'.format(c.tcolors.red, c.tcolors.reset))
                elif int(training_prompt) == 2:
                    print('Training cancelled!')
                    break
                elif int(training_prompt) == 3:
                    if silver_sword > 0:
                        # pavedEdge_damage = random.randint(15, 30)
                        point_gain = random.randint(10, 25)
                        silver_sword_damage = random.randint(10, 16)
                        silver_sword_durability_loss = random.randint(15, 25)

                        naka_hp = naka_hp - silver_sword_damage
                        silver_sword_durability = silver_sword_durability - silver_sword_durability_loss
                        battle_xp = battle_xp + 5
                        points = points + point_gain

                        print('{0}You attacked Lauren using a silver sword!\Luaren\'s health points: {1}\n+{2} points!{3}'.format(c.tcolors.yellow, naka_hp, point_gain, c.tcolors.reset))

                        # Enemy phase.
                        bp.enemy()
                        training_laurenHP()

                elif int(training_prompt) == 4:
                    if bow <= 0:
                        print('{0}ERROR: You do not own a bow yet!{1}'.format(c.tcolors.red, c.tcolors.reset))
                    elif not bow <= 0:
                        arrow_type = input("1. Regular\n2. Enhanced\n3. Tipped [Poison]\n\nSelect arrow type: ")
                        if int(arrow_type) == 1:
                            if arrows <= 0:
                                print('{0}ERROR: You do not have any arrows (regular)!{1}'.format(c.tcolors.red, c.tcolors.reset))
                            elif not arrows <= 0:
                                # pavedEdge_damage = random.randint(15, 30)
                                point_gain = random.randint(12, 25)
                                arrow_damage = random.randint(7, 14)
                                bow_durability_loss = random.randint(15, 25)
                                arrows = arrows - 1

                                naka_hp = naka_hp - arrow_damage
                                bow_durability = bow_durability - bow_durability_loss
                                battle_xp = battle_xp + 5
                                points = points + point_gain

                                print('{0}You attacked Lauren using a bow [Regular arrows]!\Lauren\'s health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, naka_hp, point_gain, c.tcolors.reset))

                                # Enemy phase
                                bp.enemy()
                                training_laurenHP()
                        elif int(arrow_type) == 2:
                            if enhanced_arrows <= 0:
                                print('{0}ERROR: You do not have any enhanced arrows!{1}'.format(c.tcolors.red, c.tcolors.reset))
                            elif not enhanced_arrows <= 0:
                                # pavedEdge_damage = random.randint(15, 30)
                                point_gain = random.randint(14, 25)
                                enhanced_arrow_damage = random.randint(12, 20)
                                bow_durability_loss = random.randint(15, 25)
                                enhanced_arrows = enhanced_arrows - 1

                                naka_hp = naka_hp - enhanced_arrow_damage
                                bow_durability = bow_durability - bow_durability_loss
                                battle_xp = battle_xp + 5
                                points = points + point_gain

                                print('{0}You attacked Lauren using a bow [Enhanced arrows]!\Lauren\'s health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, naka_hp, point_gain, c.tcolors.reset))

                                # Enemy phase.
                                bp.enemy()
                                training_laurenHP()
                        elif int(arrow_type) == 3:
                            if tipped_arrows <= 0:
                                 print('{0}ERROR: You do not have any tipped arrows!{1}'.format(c.tcolors.red, c.tcolors.reset))
                            elif not tipped_arrows <= 0:
                                # Player phase
                                point_gain = random.randint(14, 25)
                                tipped_arrow_damage = random.randint(10, 20)
                                bow_durability_loss = random.randint(15, 25)
                                tipped_arrows = tipped_arrows - 1
                                poison = random.randint(5, 10)

                                naka_hp = naka_hp - tipped_arrow_damage - poison
                                bow_durability = bow_durability - bow_durability_loss
                                battle_xp = battle_xp + 5
                                points = points + point_gain

                                print('{0}You attacked Lauren using a bow [Poison-tipped arrows]!\Lauren\'s health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, naka_hp, point_gain, c.tcolors.reset))

                                # Enemy phase.
                                bp.enemy()
                                training_laurenHP()

        
        if training_hp <= 0:
            print('\nTraining finished!\n\nYour total experience now: {}\n'.format(battle_xp))
        elif training_hp > 0 and naka_hp <= 0:
            print('\nTraining finished!')



    elif int(select) == 2:
        print('{0}Lauren: So, not starting quite yet?{1}'.format(c.tcolors.cyan, c.tcolors.reset))
    elif int(select) == 3:
        confirm_battle = input("You will be fighting low-level theives out in rich and disbandoned area. Continue?\n\n(1. Yes | 2. No): ")
        if int(confirm_battle) == 1:

            userHP = 100
            thiefOneHP = 100
            thiefTwoHP = 100
            thiefThreeHP = 100

            while userHP > 0:
                if thiefOneHP <= 0 and thiefTwoHP <= 0 and thiefThreeHP <= 0:
                    print('All targets have been defeated!')
                    break
                elif thiefOneHP > 0 and thiefTwoHP > 0 and thiefThreeHP > 0:
                    bp.player()
                    chooseTarget = input(f"\nChoose your target:\n\n1. Thief [{thiefOneHP}%]\n2. Thief [{thiefTwoHP}%]\n3. Thief [{thiefThreeHP}%]\n\n{username}: ")

                    if int(chooseTarget) == 1:
                        focusTarget = thiefOneHP
                    elif int(chooseTarget) == 2:
                        focusTarget = thiefTwoHP
                    elif int(chooseTarget) == 3:
                        focusTarget = thiefThreeHP
                    
                    attackPrompt = input("\n1. Attack [sword-based]\n2. Forfeit\n3. Attack [bow-based]\n\n[{0}%] | {1}\n[{2}%] | {3}: ".format(thiefOneHP, p.npc.thief, userHP, username))

                    if int(attackPrompt) == 1:
                        selectSword = input("1. Iron sword\n2. Silver sword\n\nSelect sword: ")
                        if int(selectSword) == 1:
                            if iron_sword > 0:
                                point_gain = random.randint(5, 7)
                                iron_sword_damage = random.randint(15, 20)
                                iron_sword_durability_loss = random.randint(10, 20)

                                focusTarget = focusTarget - iron_sword_damage
                                iron_sword_durability = iron_sword_durability - iron_sword_durability_loss
                                battle_xp = battle_xp + 5
                                points = points + point_gain

                                print('{0}You attacked {1} using an iron sword!\Lauren\'s health points: {2}\n+{3} points!{4}'.format(c.tcolors.yellow, p.npc.thief, focusTarget, point_gain, c.tcolors.reset))

                                time.sleep(3)
                                if focusTarget <= 0:
                                    print(f'{c.tcolors.redHighlight} This target has been defeated! {c.tcolors.reset}\nThief 1: [{thiefOneHP}%]')
                                elif not focusTarget <= 0:
                                    damage = random.randint(3, 5)
                                    userHP = userHP - damage

                                    print(f'{c.tcolors.grey}A thief attacked you with a wooden plank.\nDamage dealt: {damage}%{c.tcolors.reset}')

                                    # End of battle.
                            elif int(selectSword) == 2:
                                if silver_sword > 0:
                                    point_gain = random.randint(5, 7)
                                    silver_sword_damage = random.randint(15, 20)
                                    iron_sword_durability_loss = random.randint(10, 20)

                                    focusTarget = focusTarget - silver_sword_damage
                                    silver_sword_durability = silver_sword_durability - silver_sword_durability_loss
                                    battle_xp = battle_xp + 5
                                    points = points + point_gain

                                    print('{0}You attacked {1} using an iron sword!\Lauren\'s health points: {2}\n+{3} points!{4}'.format(c.tcolors.yellow, p.npc.thief, focusTarget, point_gain, c.tcolors.reset))

                                    time.sleep(3)
                                    if focusTarget <= 0:
                                        print(f'{c.tcolors.redHighlight} This target has been defeated! {c.tcolors.reset}\nThief 1: [{thiefOneHP}%]')
                                    elif not focusTarget <= 0:
                                        damage = random.randint(3, 5)
                                        userHP = userHP - damage

                                        print(f'{c.tcolors.grey}A thief attacked you with a wooden plank.\nDamage dealt: {damage}%{c.tcolors.reset}')

                                        # End of battle.
                    elif int(attackPrompt) == 3:
                        if bow <= 0:
                            print('{0}ERROR: You do not own a bow yet!{1}'.format(c.tcolors.red, c.tcolors.reset))
                        elif not bow <= 0:
                            arrow_type = input("1. Regular\n2. Enhanced\n3. Tipped [Poison]\n\nSelect arrow type: ")
                            if int(arrow_type) == 1:
                                if arrows <= 0:
                                    print('{0}ERROR: You do not have any arrows (regular)!{1}'.format(c.tcolors.red, c.tcolors.reset))
                                elif not arrows <= 0:
                                    # pavedEdge_damage = random.randint(15, 30)
                                    point_gain = random.randint(12, 25)
                                    arrow_damage = random.randint(7, 14)
                                    bow_durability_loss = random.randint(15, 25)
                                    arrows = arrows - 1

                                    focusTarget = focusTarget - arrow_damage
                                    bow_durability = bow_durability - bow_durability_loss
                                    battle_xp = battle_xp + 5
                                    points = points + point_gain

                                    print('{0}You attacked a thief using a bow [Regular arrows]!\Their health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, focusTarget, point_gain, c.tcolors.reset))

                                    # Enemy phase.
                                    time.sleep(3)
                                    if focusTarget <= 0:
                                        print(f'{c.tcolors.redHighlight} This target has been defeated! {c.tcolors.reset}\nThief 1: [{thiefOneHP}%]')
                                    elif not focusTarget <= 0:
                                        damage = random.randint(3, 5)
                                        userHP = userHP - damage

                                        print(f'{c.tcolors.grey}A thief attacked you with a wooden plank.\nDamage dealt: {damage}%{c.tcolors.reset}')

                                        # End of battle phase.
                            elif int(arrow_type) == 2:
                                if enhanced_arrows <= 0:
                                        print('{0}ERROR: You do not have any enhanced arrows!{1}'.format(c.tcolors.red, c.tcolors.reset))
                                elif not enhanced_arrows <= 0:
                                    # pavedEdge_damage = random.randint(15, 30)
                                    point_gain = random.randint(14, 25)
                                    enhanced_arrow_damage = random.randint(12, 20)
                                    bow_durability_loss = random.randint(15, 25)
                                    enhanced_arrows = enhanced_arrows - 1

                                    focusTarget = focusTarget - enhanced_arrow_damage
                                    bow_durability = bow_durability - bow_durability_loss
                                    battle_xp = battle_xp + 5
                                    points = points + point_gain

                                    print('{0}You attacked a thief using a bow [Enhanced arrows]!\Their health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, focusTarget, point_gain, c.tcolors.reset))

                                    # Enemy phase.
                                    time.sleep(3)

                                    if focusTarget <= 0:
                                        print(f'{c.tcolors.redHighlight} This target has been defeated! {c.tcolors.reset}\nThief 1: [{thiefOneHP}%]')
                                    elif not focusTarget <= 0:
                                        damage = random.randint(3, 5)
                                        userHP = userHP - damage

                                        print(f'{c.tcolors.grey}A thief attacked you with a wooden plank.\nDamage dealt: {damage}%{c.tcolors.reset}')

                                        # End of battle phase.
                            elif int(arrow_type) == 3:
                                if tipped_arrows <= 0:
                                    print('{0}ERROR: You do not have any tipped arrows!{1}'.format(c.tcolors.red, c.tcolors.reset))
                                elif not tipped_arrows <= 0:
                                    # pavedEdge_damage = random.randint(15, 30)
                                    point_gain = random.randint(14, 25)
                                    tipped_arrow_damage = random.randint(10, 20)
                                    bow_durability_loss = random.randint(15, 25)
                                    tipped_arrows = tipped_arrows - 1
                                    poison = random.randint(5, 10)

                                    focusTarget = focusTarget - tipped_arrow_damage - poison
                                    bow_durability = bow_durability - bow_durability_loss
                                    battle_xp = battle_xp + 5
                                    points = points + point_gain

                                    print('{0}You attacked Lauren using a bow [Poison-tipped arrows]!\Lauren\'s health points: {1}%\n+{2} points!{3}'.format(c.tcolors.yellow, focusTarget, point_gain, c.tcolors.reset))

                                    # Enemy phase.
                                    time.sleep(3)
                                    if focusTarget <= 0:
                                        print(f'{c.tcolors.redHighlight} This target has been defeated! {c.tcolors.reset}\nThief 1: [{thiefOneHP}%]')
                                    elif not focusTarget <= 0:
                                        damage = random.randint(3, 5)
                                        userHP = userHP - damage

                                        print(f'{c.tcolors.grey}A thief attacked you with a wooden plank.\nDamage dealt: {damage}%{c.tcolors.reset}')

                                        # End of battle phrase
        elif int(confirm_battle) == 2:
            print(f'{p.npc.lauren}: {c.tcolors.cyan}Very well then, take more time to prepare.{c.tcolors.reset}')



def console():
    global username
    global points
    global deposit
    global luck
    global slash
    global sign_in_id
    global stamina_points
    global iron_sword
    global iron_sword_durability
    while True:

        if iron_sword_durability <= 0:
            if iron_sword > 0:
                iron_sword = 0
                iron_sword_durability = 0
            elif iron_sword_durability > 0:
                pass
        terminal = input(f"[{stamina_points}%] | {username}: ")

        if terminal == slash:
            print('\nThis is the only command prefix. Slash commands are availabe in this script.\nType \"{}help\" to see all available commands.\n'.format(slash))
        elif terminal == slash + 'help':
            # Displays available commands.
            command_help()
        elif terminal == slash + 'battle':
            # Prompts battle options.
            battle()
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
            # Purchase items.
            purchase()
        elif terminal == slash + 'shop':
            shop()
        elif terminal == slash + 'update_slash':
            # Updates the slash command prefix.
            update_slash_command()
        elif terminal == slash + 'update_password':
            # Update user password.
            update_password()
        elif terminal == slash + 'uuid':
            # Dislay user ID.
            my_id()
        elif terminal == slash + 'uun':
            # Update username.
            uun()
        elif terminal == slash + 'inventory':
            inventory()
        elif terminal == slash + 'use':
            use_item()




initiateProgram()
bonusPoints = input("\nYour point balance (PB) is {}. Would you like to claim bonus points?\n(1. Yes | 2. No): ".format(points))
if int(bonusPoints) == 1:
    bonus_points()
elif int(bonusPoints) == 2:
    print('\nYou declined the bonus points, your point balance is {}.'.format(points))

console()