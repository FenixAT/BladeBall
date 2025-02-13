import cv2
import numpy as np
import keyboard
import mss
import time
import threading

def detect_red_ball(center_x, center_y, radius):
    with mss.mss() as sct:
        while True:
            screen = np.array(sct.grab(sct.monitors[1]))  
            hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            
            # red color in HSV
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 | mask2  # Combine both masks
            
            # Ball finder lol
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                image_center_x, image_center_y = x + w // 2, y + h // 2
                
                
                if w * h < 500:  
                    continue
                
                perimeter = cv2.arcLength(contour, True)
                area = cv2.contourArea(contour)
                circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
                if circularity < 0.7:  # Higher threshold to ensure it's a ball
                    continue  # Skip if not circular
                
                if (image_center_x - center_x) ** 2 + (image_center_y - center_y) ** 2 <= radius ** 2:
                    keyboard.press('f')
                    keyboard.release('f')
                    print("F")
                    break  # Stop checking after detecting one
            
            time.sleep(0.001)  

def main():
    screen_width, screen_height = 1920, 1080  # Adjust if needed
    center_x, center_y = screen_width // 2, screen_height // 2
    radius = 250  # 500x500px search area thingy :)

    thread = threading.Thread(target=detect_red_ball, args=(center_x, center_y, radius))
    thread.daemon = True
    thread.start()

    while True:
        time.sleep(1)  

if __name__ == "__main__":
    main()
