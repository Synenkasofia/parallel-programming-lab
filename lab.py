import threading
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from functools import reduce

# --- Оголошення функцій (спочатку тільки логіка) ---

counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100000):
        counter += 1

def increment_with_lock():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1

def run_test(target_func):
    global counter
    counter = 0
    t1 = threading.Thread(target=target_func)
    t2 = threading.Thread(target=target_func)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(f"Результат ({target_func.__name__}): {counter}")

def increment_func(x): 
    return x + 1

def parallel_map(func, data):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(func, data))

def heavy_task(x):
    total = 0
    for i in range(5_000_000): 
        total += i * x
    return total

def pipeline(data, steps):
    for step in steps:
        data = step(data)
    return data

def safe_risky(x):
    try:
        if x == 0: raise ValueError
        return 10 / x
    except Exception:
        return None

def safe_parallel_map(func, data):
    with ThreadPoolExecutor() as ex:
        return [r for r in ex.map(func, data) if r is not None]

def fetch_data(x):
    time.sleep(0.5) 
    return x

# --- Головний блок запуску (ТУТ МАЄ БУТИ ВСЕ, ЩО ВИВОДИТЬСЯ) ---

if __name__ == "__main__":
    
    print("--- Завдання 1 & 2 (Race Condition) ---")
    for i in range(3):
        run_test(increment) 
    run_test(increment_with_lock) 

    print("\n--- Завдання 4, 5, 6 (Parallel Map) ---")
    data_large = range(100_000)
    start = time.time()
    res1 = list(map(lambda x: x**2, data_large))
    print(f"Звичайний map: {time.time() - start:.4f}s")

    start = time.time()
    res2 = parallel_map(lambda x: x**2, data_large)
    print(f"Parallel map: {time.time() - start:.4f}s")

    print("\n--- Завдання 7 (CPU-bound) ---")
    x_val = 10
    
    start = time.time()
    heavy_task(x_val); heavy_task(x_val)
    print(f"Послідовно: {time.time() - start:.4f}s")

    start = time.time()
    with ThreadPoolExecutor() as ex:
        list(ex.map(heavy_task, [x_val, x_val]))
    print(f"Threads (ThreadPool): {time.time() - start:.4f}s")

    start = time.time()
    with ProcessPoolExecutor() as ex:
        results = list(ex.map(heavy_task, [x_val, x_val]))
        print(f"Результати процесів: {results}")
    print(f"Processes (ProcessPool): {time.time() - start:.4f}s")

    print("\n--- Завдання 11 (Pipeline) ---")
    transactions = range(1, 1001)
    steps = [
        lambda d: filter(lambda x: x > 500, d),
        lambda d: map(lambda x: x * 1.1, d),
        sum
    ]
    print(f"Результат транзакцій: {pipeline(transactions, steps)}")

    print("\n--- Завдання 12 (API Simulation) ---")
    data_to_fetch = range(10)
    
    start = time.time()
    [fetch_data(x) for x in data_to_fetch]
    print(f"Послідовне завантаження: {time.time() - start:.2f}s")

    start = time.time()
    parallel_map(fetch_data, data_to_fetch)
    print(f"Паралельне завантаження: {time.time() - start:.2f}s")