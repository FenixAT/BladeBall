# BladeBall

## Overview
BladeBall is an OpenCV-based Python bot that detects and interacts with a red ball on the screen. It uses computer vision techniques to identify the ball and automatically triggers actions in response. The bot also includes optional random movement and camera controls to enhance its functionality.

## Features
- **Red Ball Detection:** Uses OpenCV to detect a red ball on the screen and presses the 'F' key to interact with it.
- **Random Movement:** Simulates player movement by randomly pressing movement keys.
- **Camera Control:** THIS IS BROKEN, DO NOT USE!
- **GUI Interface:** Provides a user-friendly Tkinter-based interface to toggle bot features on and off.
- **Hotkeys:** Enables quick toggling of features via keyboard shortcuts.

## Installation
### Prerequisites
Ensure you have Python installed along with the following dependencies:
```sh
pip install opencv-python numpy keyboard pyautogui mss
```
if this doesn't work do:
```sh
py -m pip install opencv-python numpy keyboard pyautogui mss
```

## Usage
1. **Run the script**
   ```sh
   python BladeballAutoWithGUI.py
   ```
   or
      ```sh
      python BladeballAutoNoGUI.py
      ```
2. **Use the GUI** to toggle bot features:
   - **Bot ON/OFF (Insert Key)**: Enables or disables red ball detection.
   - **Random Movement (Home Key)**: Enables or disables random movement.
   - **Camera Up (Del Key)**: Moves the camera upwards while holding Shift.
   - **Camera Left (End Key)**: Moves the camera left while holding Shift.

## How It Works
### 1. Red Ball Detection
- Captures a portion of the screen centered around the player.
- Converts the image to HSV and applies color thresholding to detect red hues.
- Filters contours to identify circular objects (the ball).
- Presses 'F' when a valid ball is detected.

### 2. Random Movement
- Randomly selects movement keys (`W`, `A`, `S`, `D`, `Space`) and holds them for a random duration to simulate human movement.

### 3. Camera Control
- Moves the camera automatically in the specified direction using `pyautogui.moveRel()` while holding Shift.

## Contributing
Feel free to fork this repository and contribute by improving detection accuracy, adding new features, or optimizing performance.

## License
This project is licensed under the MIT License.

## Disclaimer
Use this bot responsibly and ensure it complies with the game's terms of service.
