import hashlib
from threading import Thread, Lock
from time import perf_counter

# Global variables
mines = []

# Locks for thread safety
lock = Lock()

# Function to find valid PIN for a mine
def find_valid_pin(mine):
    if not mine:
        return
    try:
        serial_number = mine.split(",")
        # print(serial_number)
    except ValueError:
        print(f"Error: Invalid format in mines.txt for line '{mine}'")
        return

    prefix = "SNOW"  # Arbitrary prefix for the PIN
    temporary_mine_key = prefix + serial_number
    pin_found = False

    # Brute force to find a valid PIN
    for i in range(1000000):
        pin_attempt = temporary_mine_key + str(i)
        # print(pin_attempt)
        hashed_pin = hashlib.sha256(pin_attempt.encode()).hexdigest()
        # print(hashed_pin)

        if hashed_pin.startswith("00000"):
            # print(hashed_pin)
            with lock:
                mines.append((mine, pin_attempt))
            pin_found = True
            break

    if not pin_found:
        with lock:
            mines.append((mine, "No valid PIN found"))

# Sequential approach
def sequential_disarm_mines():
    global mines
    start_time = perf_counter()

    with open("mines.txt", "r") as f:
        for line in f:
            find_valid_pin(line.strip())

    end_time = perf_counter()
    print(f'SEQUENTIAL DISARMING COMPLETED: {end_time - start_time:.2f} SECOND(S) TO COMPLETE!')
    print(mines)

# Multithreaded approach
def threaded_disarm_mines():
    global mines
    start_time = perf_counter()

    with open("mines.txt", "r") as f:
        lines = f.readlines()

    threads = []
    for line in lines:
        t = Thread(target=find_valid_pin, args=(line.strip(),))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = perf_counter()
    print(f'MULTITHREADED DISARMING COMPLETED: {end_time - start_time:.2f} SECOND(S) TO COMPLETE!')
    print(mines)

if __name__ == "__main__":
    sequential_disarm_mines()
    user_input = input("NOW DO YOU WISH TO RUN THE MULTITHREADED EXECUTION? (y/n): ")
    if user_input.lower() == 'y':
        threaded_disarm_mines()