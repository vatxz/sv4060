import pyautogui as pg
import actions
import constants
import json
from pynput.keyboard import Listener
from pynput import keyboard    
import threading
import my_thread
from my_thread import ThreadGroup
 
    
def kill_monster():
    while actions.check_battle() == None:
        print("Matando monstruos")
        if event_th.is_set():
            return
        pg.press("space")
        while pg.locateOnScreen("imgs/redtarget.png", confidence=0.6, region=constants.REGION_BATTLE) != None:
            if event_th.is_set():
                return
            print("esperando monstruo morir")
        print("buscando munstruo")
      
def get_loot():
    loot = pg.locateAllOnScreen("imgs/battle2.PNG", confidence=0.6, region=constants.REGION_BATTLE)
    for box in loot:
       x, y = pg.center(box)
       pg.moveTo(x, y)
       pg.press("f12")

def go_to_flag(path, wait):
    flag = pg.locateOnScreen(path, confidence=0.8, region=constants.REGION_MAP)
    if flag:
        x, y = pg.center(flag)
        if event_th.is_set():
            return
        pg.moveTo(x, y)
        pg.click()
        pg.sleep(wait)

def check_player_position():
    return pg.locateOnScreen("imgs/player.png", confidence=0.6, region=constants.REGION_MAP)

def run():
    with open(f"{constants.FOLDER_NAME}/infos.json", "r") as file:
        data = json.loads(file.read())
    while not event_th.is_set():
        for item in data:
            if event_th.is_set():
                return
            kill_monster()     
            if event_th.is_set():
                return
            pg.sleep(0.5)
            get_loot()
            if event_th.is_set():
                return
            go_to_flag(item["path"], item["wait"])
            if event_th.is_set():
                return
            if check_player_position():
               kill_monster()
               if event_th.is_set():
                   return
               pg.sleep(0.5)
               get_loot()
               if event_th.is_set():
                   return
               go_to_flag(item["path"], item["wait"])
            actions.eat_food()
            actions.hole_down(item["down_hole"])
            if event_th.is_set():
                return
            actions.hole_up(item["up_hole"], f"{constants.FOLDER_NAME}/Anchfloor3.png", 130, 130)
            actions.hole_up(item["up_hole"], f"{constants.FOLDER_NAME}/Anchfloor2.png", 430, 130)

def key_code(key, th_group):
    if key == keyboard.Key.esc:
        event_th.set()
        th_group.stop()
        return False
    if key == keyboard.Key.delete:
           th_group.start()
           th_run.start()

global event_th
event_th = threading.Event()
th_run = threading.Thread(target=run)

th_full_mana = my_thread.MyThread(lambda: actions.check_status("mana", 2, *constants.POSITION_MANA_FULL, constants.COLOR_MANA, ["F6"]))
th_check_life = my_thread.MyThread(lambda: actions.check_status("vida", 1, *constants.POSITION_LIFE, constants.COLOR_GREEN_LIFE, ["F3"]))

group_thread = my_thread.ThreadGroup([th_full_mana, th_check_life])

with Listener(on_press=lambda key: key_code(key, group_thread)) as listener:
    listener.join()