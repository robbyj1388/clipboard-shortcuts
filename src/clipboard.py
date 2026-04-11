import time
import keyboard
import os
import threading
import platform

# CONFIGURATION
start_hotkey_str = 'alt+a'
cancel_hotkey_str = 'esc'
check_updates_interval = 1

# OS Specific Pathing
if platform.system() == "Windows":
    filepath = os.path.join(os.environ['USERPROFILE'], 'clipboard-hotkey')
else:
    filepath = os.path.expanduser('~/clipboard-hotkey')

fullpath = os.path.join(filepath, "clipboard-hotkey-history.txt")

# STATE
waiting_for_hotkey = False
processing_event = False  
clipboard_history = []

def load_history():
    global clipboard_history
    try:
        os.makedirs(filepath, exist_ok=True)
        if not os.path.exists(fullpath):
            with open(fullpath, 'w', encoding='utf-8') as f:
                f.write("Line 1\nLine 2")
        with open(fullpath, 'r', encoding='utf-8') as f:
            clipboard_history = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error: {e}")

def update_loop():
    while True:
        load_history()
        time.sleep(check_updates_interval)

def handle_events(event):
    global waiting_for_hotkey, processing_event

    if processing_event:
        return

    if keyboard.is_pressed(start_hotkey_str):
        waiting_for_hotkey = True
        return

    if event.name == cancel_hotkey_str:
        waiting_for_hotkey = False
        return

    if event.event_type == 'down' and event.name in '123456789':
        index = int(event.name) - 1
        
        if waiting_for_hotkey:
            processing_event = True # Lock
            
            if index < len(clipboard_history):
                # Wait for user to release Alt/A so they don't interfere
                while keyboard.is_pressed('alt') or keyboard.is_pressed('a'):
                    time.sleep(0.01)
                
                keyboard.write(clipboard_history[index])
            
            waiting_for_hotkey = False
            processing_event = False # Unlock
        else:
            # If not in selection mode, let the number through
            # We don't suppress the key globally, so it types normally
            pass

# STARTUP 
load_history()
threading.Thread(target=update_loop, daemon=True).start()

keyboard.on_press(handle_events)

print(f"Running on {platform.system()}. Press {start_hotkey_str} then 1-9.")
print(f"History File at: {fullpath}.")
keyboard.wait()
