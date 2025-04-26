import os
import pyautogui
from PIL import Image
#this is a file not figured out yet, tbc
def placeOnScreen(self): #captures the current mouse position.
    x, y = pyautogui.position()
    screenshot = pyautogui.screenshot(region=(x-100, y-100, 200, 200))
    return screenshot
def inputPassword(password): #this will input the password where the current mouse position is at.
    if password:
        pyautogui.typewrite(password)
        return True
    return False