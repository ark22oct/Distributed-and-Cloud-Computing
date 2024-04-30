import requests

BASE_URL = "http://localhost:8000"

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            get_map()
        elif choice == "2":
            update_map()
        elif choice == "3":
            get_mines()
        elif choice == "4":
            get_mine_by_id()
        elif choice == "5":
            create_mine()
        elif choice == "6":
            update_mine()
        elif choice == "7":
            delete_mine()
        elif choice == "8":
            get_rovers()
        elif choice == "9":
            get_rover_by_id()
        elif choice == "10":
            create_rover()
        elif choice == "11":
            send_commands_to_rover()
        elif choice == "12":
            dispatch_rover()
        elif choice == "13":
            delete_rover()
        elif choice == "0":
            break
        else:
            print("Invalid choice")


def print_menu():
    print("\nMap Endpoints:")
    print("1. Get Map")
    print("2. Update Map")

    print("\nMines Endpoints:")
    print("3. Get Mines")
    print("4. Get Mine by ID")
    print("5. Create Mine")
    print("6. Update Mine")
    print("7. Delete Mine")

    print("\nRover Endpoints:")
    print("8. Get Rovers")
    print("9. Get Rover by ID")
    print("10. Create Rover")
    print("11. Send Commands to Rover")
    print("12. Dispatch Rover")
    print("13. Delete Rover")

    print("\n0. Exit")


def create_mine():
    x = int(input("Enter X coordinate: "))
    y = int(input("Enter Y coordinate: "))
    serial = input("Enter serial number: ")
    response = requests.post(f"{BASE_URL}/mines", json={"x": x, "y": y, "serial": serial})
    print(response.json())

def get_mines():
    response = requests.get(f"{BASE_URL}/mines")
    print(response.json())

def get_mine_by_id():
    mine_id = input("Enter mine ID: ")
    response = requests.get(f"{BASE_URL}/mines/{mine_id}")
    print(response.json())

def create_rover():
    commands = input("Enter commands: ")
    response = requests.post(f"{BASE_URL}/rovers", json={"commands": commands})
    print(response.json())

def get_rovers():
    response = requests.get(f"{BASE_URL}/rovers")
    print(response.json())

def get_rover_by_id():
    rover_id = input("Enter rover ID: ")
    response = requests.get(f"{BASE_URL}/rovers/{rover_id}")
    print(response.json())

def send_commands_to_rover():
    rover_id = input("Enter rover ID: ")
    commands = input("Enter commands: ")
    response = requests.post(f"{BASE_URL}/rovers/{rover_id}", json={"commands": commands})
    print(response.json())

def dispatch_rover():
    rover_id = input("Enter rover ID: ")
    response = requests.post(f"{BASE_URL}/rovers/{rover_id}/dispatch")
    print(response.json())

def get_map():
    response = requests.get(f"{BASE_URL}/map")
    print(response.json())

def update_map():
    print("Enter the new dimensions of the map (rows and columns):")
    rows = int(input("Enter number of rows: "))
    cols = int(input("Enter number of columns: "))
    
    print("Enter the new map:")
    new_map = []
    for _ in range(rows):
        row = input(f"Enter row {_ + 1} (comma-separated values): ")
        new_map.append([int(num) for num in row.split(",")])
    
    response = requests.put(f"{BASE_URL}/map", json=new_map)
    print(response.json())

def delete_rover():
    rover_id = input("Enter rover ID to delete: ")
    response = requests.delete(f"{BASE_URL}/rovers/{rover_id}")
    print(response.json())

def update_mine():
    mine_id = input("Enter mine ID to update: ")
    x = input("Enter X coordinate (optional, leave blank to keep unchanged): ")
    y = input("Enter Y coordinate (optional, leave blank to keep unchanged): ")
    serial = input("Enter serial number (optional, leave blank to keep unchanged): ")
    
    data = {}
    if x:
        data["x"] = int(x)
    if y:
        data["y"] = int(y)
    if serial:
        data["serial"] = serial

    response = requests.put(f"{BASE_URL}/mines/{mine_id}", json=data)
    print(response.json())

def delete_mine():
    mine_id = input("Enter mine ID to delete: ")
    response = requests.delete(f"{BASE_URL}/mines/{mine_id}")
    print(response.json())

if __name__ == "__main__":
    main()