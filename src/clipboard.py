import time
import keyboard
import os
import threading
import sys
import pyperclip

waiting_for_hotkey = False
startHotkey = 'alt+a'
cancelHotkey = 'esc'
check_for_updates_time = 1

clipboard_hotkey_history = ["item1", "item2", "item3"]

filepath = os.path.expanduser('~/clipboard-hotkey/')
filename = "clipboard-hotkey-history.txt"
fullpath = os.path.join(filepath, filename)

# FUNCTIONS
def load_history():
    try:
        os.makedirs(filepath, exist_ok=True)

        # Create file if it doesn't exist
        if not os.path.exists(fullpath):
            print("No file found creating history file at:", fullpath)
            open(fullpath, 'w').close()

        with open(fullpath, 'r') as f:
            return [line.rstrip() for line in f if line.strip()]

    except Exception as e:
        print("Error loading history:", e)
        return clipboard_hotkey_history


def updateHistory(delay_in_seconds):
    global clipboard_hotkey_history

    clipboard_hotkey_history = load_history()
    last_mtime = os.path.getmtime(fullpath)

    while True:
        time.sleep(delay_in_seconds)
        try:
            new_mtime = os.path.getmtime(fullpath)

            if new_mtime != last_mtime:
                print("File changed, reloading...")
                clipboard_hotkey_history = load_history()
                last_mtime = new_mtime

        except FileNotFoundError:
            print("ERROR: File not found! Exiting...")
            sys.exit()


def setSelectHotkey(state):
    global waiting_for_hotkey
    waiting_for_hotkey = state


def onHotkey(index):
    global waiting_for_hotkey

    if waiting_for_hotkey and index < len(clipboard_hotkey_history):
        time.sleep(0.1)
        keyboard.send('backspace')

        text_to_paste = clipboard_hotkey_history[index]
        pyperclip.copy(text_to_paste)
        keyboard.send('ctrl+v')

        setSelectHotkey(False)

# def onHotkey(index):
#     global waiting_for_hotkey
# 
#     if waiting_for_hotkey and index < len(clipboard_hotkey_history):
#         time.sleep(0.1)
#         keyboard.send('backspace')
#         text_to_paste = clipboard_hotkey_history[index]
#         keyboard.write(text_to_paste, delay=0.01)
#         setSelectHotkey(False)

# Start background thread
hotkey_thread = threading.Thread(
    target=updateHistory,
    args=(check_for_updates_time,),
    daemon=True
)
hotkey_thread.start()

# Main hotkeys
keyboard.add_hotkey(startHotkey, lambda: setSelectHotkey(True))
keyboard.add_hotkey(cancelHotkey, lambda: setSelectHotkey(False))

# Register hotkeys 1–9
for i in range(9):
    keyboard.add_hotkey(str(i + 1), onHotkey, args=(i,), suppress=True)

keyboard.wait()
