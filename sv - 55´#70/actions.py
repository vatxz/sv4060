import time
import pyautogui as pg
import constants
import keyboard

def eat_food():
    pg.press("F8")
    pg.press("F9")
    print("comiendo comida..")
   
def hole_down(should_down):
    if should_down:
       box = pg.locateOnScreen("imgs/barraverde.png", confidence=0.6)
       if box:
           x, y = pg.center(box)
           pg.sleep(1)
           pg.press("space")
           pg.sleep(2)
           pg.press("f4")
           pg.sleep(4)
           pg.press("f4")


def hole_up(should_up, img_anchor, plus_x, plus_y):
    if should_up:
       box = pg.locateOnScreen(img_anchor, confidence=0.5)
       if box:
           x, y = pg.center(box)
           pg.moveTo(x, y)
           pg.click()
           pg.sleep(5)

def check_status(name, delay, x, y, rgb, button_names):
  print(f"checando {name}...")
  pg.sleep(delay)
  if pg.pixelMatchesColor(x, y, rgb):
      for button in button_names:
          pg.press(button)
          print(F"Pressed  {button}")
          time.sleep(0.2)

def check_battle():
    return pg.locateOnScreen("imgs/battle2.png", region=constants.REGION_BATTLE)
       
    
