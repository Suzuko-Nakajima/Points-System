import asyncio

class color():
    red = '\033[101m'
    blue = '\033[104m'
    reset = '\033[0m'

def player():
        print(f'{color.blue}BEGIN PLAYER PHASE!{color.reset}')
def enemy():
        print(f'{color.red}BEGIN ENEMY PHASE!{color.reset}')