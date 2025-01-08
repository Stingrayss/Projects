import pyautogui
from PIL import ImageGrab
import win32api
import keyboard

# Enable failsafe so moving the mouse to the top-left corner stops the program
pyautogui.FAILSAFE = True
screen_region = (600, 200, 2000, 1200)  # (x1, y1, x2, y2)

# Function to check the screen region for a fully white 20x20 area
def find_filled_area_and_move():
    screenshot = ImageGrab.grab(bbox=screen_region)  # Capture the region (x1, y1, x2, y2)
    width, height = screenshot.size

    for x in range(0, width, 15):
        for y in range(0, height, 15):
            win32api.SetCursorPos((x + screen_region[0],y + screen_region[1]))


try:
    #qlast_screenshot_time = time.time()
    while True:
        if (keyboard.is_pressed('q')):
            raise KeyboardInterrupt

        find_filled_area_and_move()
        
except KeyboardInterrupt:
    print("Program terminated manually.")
