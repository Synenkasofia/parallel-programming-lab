import threading
import time

counter = 0

def increment():
    global counter
    for _ in range(100000):
        temp = counter
        time.sleep(0.00001)
        counter = temp + 1

for i in range(5):
    counter = 0

    t1 = threading.Thread(target=increment)
    t2 = threading.Thread(target=increment)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Спроба {i+1}: {counter}")




    # =========================
# Завдання 2: Lock
# =========================

counter = 0
lock = threading.Lock()

def increment_lock():
    global counter
    for _ in range(100000):
        with lock:
            temp = counter
            time.sleep(0.00001)
            counter = temp + 1

for i in range(5):
    counter = 0

    t1 = threading.Thread(target=increment_lock)
    t2 = threading.Thread(target=increment_lock)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"[LOCK] Спроба {i+1}: {counter}")