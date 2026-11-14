from pynput import keyboard
import subprocess

ADB = "adb"
HOLD_X = "950"
HOLD_Y = "1070"

# Ánh xạ phím chuột bay sang lệnh ADB
KEY_MAP = {
    keyboard.Key.up: ["shell", "input", "swipe", "540", "1400", "540", "200", "300"],
    keyboard.Key.down: ["shell", "input", "swipe", "540", "400", "540", "1600", "300"],
    keyboard.Key.enter: ["shell", "input", "tap", "540", "960"],
    keyboard.Key.page_down: ["shell", "input", "keyevent", "25"],
}

hold_active = False
right_pressed = False


def on_press(key):
    global hold_active, right_pressed

    if key == keyboard.Key.esc:
        print("Stopping...")
        if hold_active:
            subprocess.run([ADB, "shell", "input", "motionevent", "UP", HOLD_X, HOLD_Y])
            hold_active = False
        return False

    if key == keyboard.Key.right:
        # Bỏ qua sự kiện lặp khi giữ phím, chỉ toggle một lần mỗi lần nhấn.
        if right_pressed:
            return
        right_pressed = True

        action = "DOWN" if not hold_active else "UP"
        command = [ADB, "shell", "input", "motionevent", action, HOLD_X, HOLD_Y]
        print("Executing:", command)
        subprocess.run(command)
        hold_active = not hold_active
        return

    if key in KEY_MAP:
        command = [ADB] + KEY_MAP[key]
        print("Executing:", command)
        subprocess.Popen(command)

    else:
        print("Unmapped key:", key)


def on_release(key):
    global right_pressed
    if key == keyboard.Key.right:
        right_pressed = False


print("Mouse ADB controller running...")
print("Press ESC to stop.")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
