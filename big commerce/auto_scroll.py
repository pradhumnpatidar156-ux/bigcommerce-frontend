import pyautogui
import time
import random
import threading

print("Human-like activity simulation started (macOS friendly)...")

def random_mouse_movement():
    screenWidth, screenHeight = pyautogui.size()
    while True:
        x = random.randint(0, screenWidth)
        y = random.randint(0, screenHeight)
        duration = random.uniform(0.5, 1.5)
        pyautogui.moveTo(x, y, duration=duration)
        time.sleep(random.uniform(1.0, 3.0))

def random_scroll():
    while True:
        scroll_amount = random.randint(-50, 50)
        pyautogui.scroll(scroll_amount)
        time.sleep(random.uniform(4, 8))

def occasional_clicks():
    while True:
        if random.random() < 0.3:
            pyautogui.click()
        time.sleep(random.uniform(10, 20))

def simulate_typing():
    while True:
        if random.random() < 0.2:
            pyautogui.typewrite(random.choice(["", "", "  "]), interval=0.2)
        time.sleep(random.uniform(20, 30))

# Start all activities in separate threads
threads = [
    threading.Thread(target=random_mouse_movement),
    threading.Thread(target=random_scroll),
    threading.Thread(target=occasional_clicks),
    threading.Thread(target=simulate_typing),
]

for thread in threads:
    thread.daemon = True
    thread.start()

# Keep the main thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopped.")
