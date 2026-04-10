import keyboard, time

waiting_for_hotkey = False
startHotkey = 'alt+a'
cancelHotkey = 'esc'

# FUNCTIONS
def setSelectHotkey(boolean):
    global waiting_for_hotkey 
    waiting_for_hotkey = boolean

def onHotkey(number):
    global waiting_for_hotkey
    if waiting_for_hotkey and number < len(clipboard_hotkey_history):
        # Add a tiny pause so your finger can leave the key
        time.sleep(0.1) 
        text_to_paste = clipboard_hotkey_history[number]
        keyboard.write(text_to_paste, delay=0.01)
        # Reset the state so numbers go back to normal
        setSelectHotkey(False)

# GET HISTORY
try:
    with open('clipboard-hotkey-history.txt', 'r') as f:
        clipboard_hotkey_history = [line.rstrip() for line in f]
    print("Loaded history:", clipboard_hotkey_history)
except FileNotFoundError:
    clipboard_hotkey_history = ["item1", "item2", "item3"]
    print("File not found, using defaults:", clipboard_hotkey_history)

# ALLOW HOTKEYS 1-9
keyboard.add_hotkey(startHotkey, lambda: setSelectHotkey(True))
keyboard.add_hotkey(cancelHotkey, lambda: setSelectHotkey(False))

# SETUP 1-9 AS HOTKEYS
for i in range(len(clipboard_hotkey_history)):
    if i < 9: # Only map 1-9
        keyboard.add_hotkey(str(i+1), onHotkey, args=(i,))

keyboard.wait()
