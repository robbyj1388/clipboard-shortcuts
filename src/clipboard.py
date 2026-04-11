import time
import keyboard
import os
import threading
import platform

# CONFIGURATION 
start_hotkey_str = 'alt+a'
cancel_hotkey_str = 'esc'

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
        if not os.path.exists(fullpath):
            os.makedirs(filepath, exist_ok=True)
            with open(fullpath, 'w', encoding='utf-8') as f:
                f.write("Line 1\nLine 2")
        with open(fullpath, 'r', encoding='utf-8') as f:
            clipboard_history = [line.strip() for line in f if line.strip()]
    except Exception: pass

def handle_events(event):
    global waiting_for_hotkey, processing_event

    if processing_event or event.event_type == 'up':
        return

    # Detect Start Hotkey
    if keyboard.is_pressed(start_hotkey_str):
        waiting_for_hotkey = True
        return

    # Detect Selection
    if waiting_for_hotkey and event.name in '123456789':
        index = int(event.name) - 1
        waiting_for_hotkey = False # Turn off state immediately
        
        if index < len(clipboard_history):
            processing_event = True
            
            while keyboard.is_pressed('alt') or keyboard.is_pressed('a') or keyboard.is_pressed(event.name):
                time.sleep(0.01)
            
            # Remove the number '1' that was just typed
            keyboard.send('backspace') 
            
            # Type the text at hardware speed
            text_to_type = clipboard_history[index]
            keyboard.write(text_to_type, delay=0) 
            
            processing_event = False
        return

    # 3. Detect Cancel
    if event.name == cancel_hotkey_str:
        waiting_for_hotkey = False

# STARTUP 
load_history()
# Watcher thread for file changes
def watch_file():
    last_mtime = 0
    while True:
        try:
            mtime = os.path.getmtime(fullpath)
            if mtime != last_mtime:
                load_history()
                last_mtime = mtime
        except: pass
        time.sleep(1)

threading.Thread(target=watch_file, daemon=True).start()

keyboard.hook(handle_events)
print(f"Ready. Press {start_hotkey_str} then 1-9.")
keyboard.wait()
