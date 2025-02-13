import cv2
import numpy as np
import keyboard
import pyautogui
import mss
import time
import threading
import tkinter as tk
from tkinter import ttk

# Global toggles
bot_active = False
random_movement_active = False
camera_up_active = False
camera_left_active = False

# Function to detect red ball
def detect_red_ball(center_x, center_y, radius):
    global bot_active
    with mss.mss() as sct:
        while True:
            if not bot_active:
                time.sleep(0.1)
                continue

            monitor = {"top": center_y - radius, "left": center_x - radius, "width": 2 * radius, "height": 2 * radius}
            screen = np.array(sct.grab(monitor))
            hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)

            lower_red1, upper_red1 = np.array([0, 100, 50]), np.array([10, 255, 255])
            lower_red2, upper_red2 = np.array([160, 100, 50]), np.array([180, 255, 255])
            mask = cv2.bitwise_or(cv2.inRange(hsv, lower_red1, upper_red1), cv2.inRange(hsv, lower_red2, upper_red2))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h < 300:
                    continue

                perimeter = cv2.arcLength(contour, True)
                area = cv2.contourArea(contour)
                circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
                if circularity < 0.6:
                    continue

                keyboard.press_and_release('f')
                print("F Pressed")
                break

            time.sleep(0.005)

# Function for random movement
def random_movement():
    while True:
        if bot_active and random_movement_active:
            key = np.random.choice(['w', 'a', 's', 'd', 'space'])
            keyboard.press(key)
            time.sleep(np.random.uniform(0.5, 1.5))  # Hold the key for movement
            keyboard.release(key)
        time.sleep(np.random.uniform(0.2, 0.4))  # Short delay before pressing again

# Function for moving the camera
def move_camera():
    global camera_up_active, camera_left_active
    while True:
        if not bot_active:
            time.sleep(0.1)
            continue

        if camera_up_active:
            pyautogui.keyDown('shift')
            pyautogui.moveRel(0, -500, duration=0.05)  # Fast upwards movement

        elif camera_left_active:
            pyautogui.keyDown('shift')
            pyautogui.moveRel(-500, 0, duration=0.05)  # Fast left movement

        time.sleep(0.02)

# GUI Setup
root = tk.Tk()
root.title("Red Ball Detector Bot")
root.geometry("400x400")
root.configure(bg="#121212")
root.attributes('-topmost', 1)  # Keeps the GUI always on top

# Styling
style = ttk.Style()
style.configure("TCheckbutton", background="#121212", foreground="white", font=("Arial", 12))
style.configure("TButton", background="#333", foreground="white", font=("Arial", 12))

# Toggle state dictionary
toggle_vars = {
    "bot": tk.BooleanVar(),
    "random_movement": tk.BooleanVar(),
    "camera_up": tk.BooleanVar(),
    "camera_left": tk.BooleanVar()
}

# Function to update toggle states
def update_toggle(var):
    global bot_active, random_movement_active, camera_up_active, camera_left_active

    state = toggle_vars[var].get()

    if var == "bot":
        bot_active = state
    elif var == "random_movement":
        random_movement_active = state
    elif var in ["camera_up", "camera_left"]:
        # Ensure only one camera mode is active at a time
        toggle_vars["camera_up"].set(False)
        toggle_vars["camera_left"].set(False)
        camera_up_active = camera_left_active = False

        if state:
            toggle_vars[var].set(True)
            if var == "camera_up":
                camera_up_active = True
            elif var == "camera_left":
                camera_left_active = True

    print(f"{var} set to {state}")

# Function to toggle state via hotkeys
def toggle_hotkey(var):
    toggle_vars[var].set(not toggle_vars[var].get())
    update_toggle(var)

# Create toggle buttons with hotkeys
toggles = [
    ("Bot ON/OFF", "bot", "Insert"),
    ("Random Movement", "random_movement", "Home"),
    ("Auto Move Camera Up (Shift-Lock)", "camera_up", "Del"),
    ("Auto Move Camera Left (Shift-Lock)", "camera_left", "End")
]

for i, (label, var, hotkey) in enumerate(toggles):
    chk = ttk.Checkbutton(root, text=f"{label} ({hotkey})", style="TCheckbutton",
                          variable=toggle_vars[var], command=lambda v=var: update_toggle(v))
    chk.grid(row=i, column=0, sticky="w", padx=10, pady=5)

    # Bind hotkeys
    keyboard.add_hotkey(hotkey, lambda v=var: toggle_hotkey(v))

# Start Bot Threads
screen_width, screen_height = 1920, 1080
center_x, center_y = screen_width // 2, screen_height // 2
radius = 250

threading.Thread(target=detect_red_ball, args=(center_x, center_y, radius), daemon=True).start()
threading.Thread(target=random_movement, daemon=True).start()
threading.Thread(target=move_camera, daemon=True).start()

root.mainloop()
