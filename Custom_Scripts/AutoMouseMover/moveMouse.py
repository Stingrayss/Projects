import pyautogui
from PIL import ImageGrab
import win32gui
import win32api
import win32con  # Import win32con for constants
import keyboard

# Enable failsafe so moving the mouse to the top-left corner stops the program
pyautogui.FAILSAFE = True

target_color = (255, 255, 255)  # White
target_color_sum = sum(target_color)
screen_region = (600, 200, 2000, 1200)  # (x1, y1, x2, y2)
area_sample = 25  # 20x20 area to check
lookup_table = {}

# Pre-calculate the color threshold
threshold = 35  # Max allowable difference from target_color_sum

def draw_border(x, x2, y, y2):
    dc = win32gui.GetDC(0)  # Get device context for the entire screen
    red_pen = win32gui.CreatePen(win32con.PS_SOLID, 2, win32api.RGB(255, 0, 0))  # Create red pen
    old_pen = win32gui.SelectObject(dc, red_pen)

    # Draw the top border
    win32gui.MoveToEx(dc, x, y)
    win32gui.LineTo(dc, x2, y)

    # Draw the right border
    win32gui.MoveToEx(dc, x2, y)
    win32gui.LineTo(dc, x2, y2)

    # Draw the bottom border
    win32gui.MoveToEx(dc, x2, y2)
    win32gui.LineTo(dc, x, y2)

    # Draw the left border
    win32gui.MoveToEx(dc, x, y2)
    win32gui.LineTo(dc, x, y)

    win32gui.SelectObject(dc, old_pen)  # Restore old pen
    win32gui.ReleaseDC(0, dc)  # Release the device context
    win32gui.DeleteObject(red_pen)  # Clean up the pen

# Function to check if a 20x20 area is fully filled with the target color
def is_area_filled_with_color(image, start_x, start_y):
    pixels = image.load()
    for x in range(area_sample):
        for y in range(area_sample):
            pixel_rgb = pixels[start_x + x, start_y + y]
            if abs(sum(pixel_rgb) - target_color_sum) > threshold:
                return False
    return True

# Function to check the screen region for a fully white 20x20 area
def find_filled_area_and_move():
    screenshot = ImageGrab.grab(bbox=screen_region)  # Capture the region (x1, y1, x2, y2)
    width, height = screenshot.size

    for x in range(0, width - area_sample, 25):  # Skip by 10 pixels for faster scanning
        for y in range(0, height - area_sample, 25):
            if (x, y) in lookup_table:
                x = x + 40
                y = y + 40
                continue
            if is_area_filled_with_color(screenshot, x, y):
                # Move the mouse to the center of the 20x20 area
                center_x = x + (area_sample // 2) + screen_region[0]  # Adjust to screen coordinates
                center_y = y + (area_sample // 2) + screen_region[1]
                win32api.SetCursorPos((center_x,center_y))
                lookup_table[(x,y)] = True

                #found_x = x + screen_region[0]
                #found_y = y + screen_region[1]

                #draw_border(found_x, found_x + area_sample, found_y, found_y + area_sample)
                return
    lookup_table.clear()

try:
    start_mouse_movement = False
    while True:
        if (keyboard.is_pressed('s')):
            start_mouse_movement = True

        if (keyboard.is_pressed('p')):
            start_mouse_movement = False

        if (keyboard.is_pressed('q')):
            raise KeyboardInterrupt

        if start_mouse_movement:
            find_filled_area_and_move()

except KeyboardInterrupt:
    print("Program terminated manually.")

#CONCLUSION
#SOFTWARE WORKS WELL, BUT THE GAME DOES NOT REGISTER THE MOUSE MOVEMENTS
#THEREFORE, THIS IS USELESS