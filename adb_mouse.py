
from pynput import keyboard
import subprocess

ADB = "adb"

# Ánh xạ phím chuột bay sang lệnh ADB
KEY_MAP = {
    keyboard.Key.up: ["shell", "input", "swipe", "540", "1400", "540", "200", "300"],
    keyboard.Key.down: ["shell", "input", "swipe", "540", "400", "540", "1600", "300"],
    keyboard.Key.enter: ["shell", "input", "tap", "540", "960"],
    keyboard.Key.page_down: ["shell", "input", "keyevent", "25"],
}

def on_press(key):
    if key == keyboard.Key.esc:
        print("Stopping...")
        return False

    if key in KEY_MAP:
        command = [ADB] + KEY_MAP[key]
        print("Executing:", command)
        subprocess.Popen(command)

    else:
        print("Unmapped key:", key)

print("Mouse ADB controller running...")
print("Press ESC to stop.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
