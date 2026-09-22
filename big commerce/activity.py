# import pyautogui
# import time
# import random
# import threading

# # Windows-specific safety settings
# pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
# pyautogui.PAUSE = 0.1      # Small delay between PyAutoGUI calls (Windows needs this)

# print("Human-like activity simulation started (Windows)...")
# print("Move mouse to TOP-LEFT corner to emergency stop.\n")

# def random_mouse_movement():
#     screenWidth, screenHeight = pyautogui.size()
#     while True:
#         x = random.randint(50, screenWidth - 50)   # Stay away from screen edges
#         y = random.randint(50, screenHeight - 50)  # Avoid taskbar / corners
#         duration = random.uniform(0.5, 1.5)
#         try:
#             pyautogui.moveTo(x, y, duration=duration)
#         except pyautogui.FailSafeException:
#             print("FailSafe triggered — stopping.")
#             return
#         time.sleep(random.uniform(1.0, 3.0))

# def random_scroll():
#     while True:
#         scroll_amount = random.randint(-5, 5)  # Windows scroll units are smaller than macOS
#         try:
#             pyautogui.scroll(scroll_amount)
#         except pyautogui.FailSafeException:
#             return
#         time.sleep(random.uniform(4, 8))

# def occasional_clicks():
#     while True:
#         if random.random() < 0.3:
#             try:
#                 pyautogui.click()
#             except pyautogui.FailSafeException:
#                 return
#         time.sleep(random.uniform(10, 20))

# def simulate_typing():
#     while True:
#         if random.random() < 0.2:
#             try:
#                 # Use press() instead of typewrite() for better Windows compatibility
#                 pyautogui.press(random.choice(['shift', 'ctrl', 'alt']))
#             except pyautogui.FailSafeException:
#                 return
#         time.sleep(random.uniform(20, 30))

# # Start all activities in separate threads
# threads = [
#     threading.Thread(target=random_mouse_movement, daemon=True),
#     threading.Thread(target=random_scroll, daemon=True),
#     threading.Thread(target=occasional_clicks, daemon=True),
#     threading.Thread(target=simulate_typing, daemon=True),
# ]

# for thread in threads:
#     thread.start()

# # Keep the main thread alive
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     print("\nStopped.")


import pyautogui
import time
import random
import threading
import keyboard
import os
import glob
import pygetwindow as gw   # pip install pygetwindow

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

print("=" * 55)
print("  Human-like Activity Simulator - Windows")
print("=" * 55)
print("HOTKEYS:")
print("  F1       - Next Chrome tab")
print("  F2       - Previous Chrome tab")
print("  F3       - Open random file from Documents")
print("  F4       - Open File Explorer")
print("  F5       - New Chrome tab")
print("  F6       - Close current Chrome tab")
print("  F7       - Switch to next open app window")
print("  F8       - Switch to previous app window")
print("  F9       - Show Task View")
print("  F10      - Focus Chrome window")
print("  F11      - Snap window left")
print("  F12      - Snap window right")
print("  CTRL+F1  - Minimize current window")
print("  CTRL+F2  - Maximize current window")
print("  CTRL+F3  - Next virtual desktop")
print("  CTRL+F4  - Previous virtual desktop")
print("  ESC      - Stop the script")
print("=" * 55)
print("Move mouse to TOP-LEFT corner to emergency stop.\n")

running = True

# ──────────────────────────────────────────────
# Helper — focus a window by title keyword
# ──────────────────────────────────────────────

def focus_window(keyword):
    """Find and bring to front the first window whose title contains keyword."""
    keyword = keyword.lower()
    matches = [w for w in gw.getAllWindows() if keyword in w.title.lower() and w.visible]
    if matches:
        win = matches[0]
        try:
            win.restore()   # un-minimize if needed
            win.activate()
            time.sleep(0.3)
            return True
        except Exception as e:
            print(f"  Could not activate window: {e}")
    return False

def get_all_visible_windows():
    """Return all visible windows with real titles."""
    return [w for w in gw.getAllWindows()
            if w.visible and w.title.strip() and w.width > 100]

# ──────────────────────────────────────────────
# Background activity functions
# ──────────────────────────────────────────────

def random_mouse_movement():
    screenWidth, screenHeight = pyautogui.size()
    while running:
        x = random.randint(50, screenWidth - 50)
        y = random.randint(50, screenHeight - 50)
        duration = random.uniform(0.5, 1.5)
        try:
            pyautogui.moveTo(x, y, duration=duration)
        except pyautogui.FailSafeException:
            print("FailSafe triggered — stopping.")
            return
        time.sleep(random.uniform(1.0, 3.0))

def random_scroll():
    while running:
        scroll_amount = random.randint(-5, 5)
        try:
            pyautogui.scroll(scroll_amount)
        except pyautogui.FailSafeException:
            return
        time.sleep(random.uniform(4, 8))

def occasional_clicks():
    while running:
        if random.random() < 0.3:
            try:
                pyautogui.click()
            except pyautogui.FailSafeException:
                return
        time.sleep(random.uniform(10, 20))

def simulate_typing():
    while running:
        if random.random() < 0.2:
            try:
                pyautogui.press(random.choice(['shift', 'ctrl', 'alt']))
            except pyautogui.FailSafeException:
                return
        time.sleep(random.uniform(20, 30))

# ──────────────────────────────────────────────
# Chrome tab switching  ← FIXED
# ──────────────────────────────────────────────

def ensure_chrome_focused():
    """Focus Chrome before sending tab hotkeys."""
    # Try common Chrome window title patterns
    for keyword in ['chrome', 'google chrome', 'chromium']:
        if focus_window(keyword):
            print(f"  ✔ Chrome focused.")
            return True
    print("  ✘ Chrome window not found. Open Chrome first.")
    return False

def next_tab():
    print("[F1] Switching to next Chrome tab...")
    if ensure_chrome_focused():
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'tab')

def prev_tab():
    print("[F2] Switching to previous Chrome tab...")
    if ensure_chrome_focused():
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'shift', 'tab')

def new_browser_tab():
    print("[F5] Opening new Chrome tab...")
    if ensure_chrome_focused():
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 't')

def close_current_tab():
    print("[F6] Closing current Chrome tab...")
    if ensure_chrome_focused():
        time.sleep(0.2)
        pyautogui.hotkey('ctrl', 'w')

def focus_chrome():
    print("[F10] Focusing Chrome window...")
    if not ensure_chrome_focused():
        print("  Chrome not found — listing open windows:")
        for w in get_all_visible_windows():
            print(f"    → {w.title}")

# ──────────────────────────────────────────────
# Window switching  ← FIXED using pygetwindow
# ──────────────────────────────────────────────

# Track index for cycling through windows
_window_index = [0]
_window_index_lock = threading.Lock()

def next_window():
    """Cycle forward through all visible windows."""
    print("[F7] Switching to next window...")
    windows = get_all_visible_windows()
    if not windows:
        print("  No windows found.")
        return
    with _window_index_lock:
        _window_index[0] = (_window_index[0] + 1) % len(windows)
        win = windows[_window_index[0]]
    print(f"  → Switching to: {win.title[:60]}")
    try:
        win.restore()
        win.activate()
    except Exception as e:
        print(f"  Could not switch: {e}")

def prev_window():
    """Cycle backward through all visible windows."""
    print("[F8] Switching to previous window...")
    windows = get_all_visible_windows()
    if not windows:
        print("  No windows found.")
        return
    with _window_index_lock:
        _window_index[0] = (_window_index[0] - 1) % len(windows)
        win = windows[_window_index[0]]
    print(f"  → Switching to: {win.title[:60]}")
    try:
        win.restore()
        win.activate()
    except Exception as e:
        print(f"  Could not switch: {e}")

# ──────────────────────────────────────────────
# Other window controls
# ──────────────────────────────────────────────

def open_random_file():
    docs_path = os.path.join(os.path.expanduser("~"), "Documents")
    extensions = ['*.pdf', '*.txt', '*.docx', '*.xlsx', '*.png', '*.jpg']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(docs_path, ext)))
    if files:
        chosen = random.choice(files)
        print(f"[F3] Opening file: {chosen}")
        os.startfile(chosen)
    else:
        print("[F3] No files found in Documents folder.")

def open_file_explorer():
    print("[F4] Opening File Explorer...")
    os.startfile(os.path.expanduser("~"))

def task_view():
    print("[F9] Opening Task View...")
    pyautogui.hotkey('win', 'tab')

def snap_window_left():
    print("[F11] Snapping window to left...")
    pyautogui.hotkey('win', 'left')

def snap_window_right():
    print("[F12] Snapping window to right...")
    pyautogui.hotkey('win', 'right')

def minimize_window():
    print("[CTRL+F1] Minimizing window...")
    pyautogui.hotkey('win', 'down')
    time.sleep(0.1)
    pyautogui.hotkey('win', 'down')

def maximize_window():
    print("[CTRL+F2] Maximizing window...")
    pyautogui.hotkey('win', 'up')

def next_virtual_desktop():
    print("[CTRL+F3] Next virtual desktop...")
    pyautogui.hotkey('win', 'ctrl', 'right')

def prev_virtual_desktop():
    print("[CTRL+F4] Previous virtual desktop...")
    pyautogui.hotkey('win', 'ctrl', 'left')

def stop_script():
    global running
    print("\n[ESC] Stopping script...")
    running = False
    time.sleep(0.5)
    os._exit(0)

# ──────────────────────────────────────────────
# Register all hotkeys
# ──────────────────────────────────────────────

keyboard.add_hotkey('F1',      next_tab)
keyboard.add_hotkey('F2',      prev_tab)
keyboard.add_hotkey('F3',      open_random_file)
keyboard.add_hotkey('F4',      open_file_explorer)
keyboard.add_hotkey('F5',      new_browser_tab)
keyboard.add_hotkey('F6',      close_current_tab)
keyboard.add_hotkey('F7',      next_window)
keyboard.add_hotkey('F8',      prev_window)
keyboard.add_hotkey('F9',      task_view)
keyboard.add_hotkey('F10',     focus_chrome)
keyboard.add_hotkey('F11',     snap_window_left)
keyboard.add_hotkey('F12',     snap_window_right)
keyboard.add_hotkey('ctrl+F1', minimize_window)
keyboard.add_hotkey('ctrl+F2', maximize_window)
keyboard.add_hotkey('ctrl+F3', next_virtual_desktop)
keyboard.add_hotkey('ctrl+F4', prev_virtual_desktop)
keyboard.add_hotkey('esc',     stop_script)

# ──────────────────────────────────────────────
# Start background threads
# ──────────────────────────────────────────────

threads = [
    threading.Thread(target=random_mouse_movement, daemon=True),
    threading.Thread(target=random_scroll,         daemon=True),
    threading.Thread(target=occasional_clicks,     daemon=True),
    threading.Thread(target=simulate_typing,       daemon=True),
]

for thread in threads:
    thread.start()

print("Ready! Press F10 to verify Chrome is detected.\n")

try:
    while running:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped via Ctrl+C.")
    running = False