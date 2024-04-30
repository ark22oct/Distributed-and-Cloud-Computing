import requests
import json
from threading import Thread, Lock
from time import perf_counter

class RoverController:
   def __init__(self):
       self.rover_status = "Active"
       self.rover_direction = 'South'
       self.rover_position = [0, 0]
       self.lock = Lock()  # Add a lock for synchronization

   def fetch_rover_moves(self, number):
       response = requests.get(f'https://coe892.reev.dev/lab1/rover/{number}')
       data = response.text
       parsed_json = json.loads(data)
       moves = parsed_json['data']['moves']
      #print(f"Number: {number}, Moves from API: {moves}")
       return parsed_json['data']['moves']

   def move_forward(self, path):
       try:
           # Acquire lock before modifying shared data
           with self.lock:
               if self.rover_direction == 'North':
                   if self.rover_position[1] == 0:
                       return
                   if path[self.rover_position[1] - 1][self.rover_position[0]] == '1':
                       self.rover_status = "Dead"
                       return self.rover_status
                   self.rover_position[1] -= 1
                   path[self.rover_position[1]][self.rover_position[0]] = "*"
               elif self.rover_direction == 'South':
                   if self.rover_position[1] == rows - 1:
                       return
                   if path[self.rover_position[1] + 1][self.rover_position[0]] == '1':
                       self.rover_status = "Dead"
                       return self.rover_status
                   self.rover_position[1] += 1
                   path[self.rover_position[1]][self.rover_position[0]] = "*"
               elif self.rover_direction == 'East':
                   if self.rover_position[0] == columns - 1:
                       return
                   if path[self.rover_position[1]][self.rover_position[0] + 1] == '1':
                       self.rover_status = "Dead"
                       return self.rover_status
                   self.rover_position[0] += 1
                   path[self.rover_position[1]][self.rover_position[0]] = "*"
               elif self.rover_direction == 'West':
                   if self.rover_position[0] == 0:
                       return
                   if path[self.rover_position[1]][self.rover_position[0] - 1] == '1':
                       self.rover_status = "Dead"
                       return self.rover_status
                   self.rover_position[0] -= 1
                   path[self.rover_position[1]][self.rover_position[0]] = "*"
       except IndexError:
           print("Index out of range")

   def turn_left(self):
       if self.rover_direction == 'North':
           return 'West'
       elif self.rover_direction == 'East':
           return 'North'
       elif self.rover_direction == 'South':
           return 'East'
       elif self.rover_direction == 'West':
           return 'South'

   def turn_right(self):
       if self.rover_direction == 'North':
           return 'East'
       elif self.rover_direction == 'East':
           return 'South'
       elif self.rover_direction == 'South':
           return 'West'
       elif self.rover_direction == 'West':
           return 'North'

   def check_mine(self, path):
       if path[self.rover_position[1]][self.rover_position[0]] == '1':
           pass #print("Mine detected, start digging!")
       elif path[self.rover_position[1]][self.rover_position[0]] != '1':
           pass #print("No mine detected!")
       else:
           pass

   def initiate_rover_traversal(self, rover_number):
       self.rover_status = "Active"
       self.rover_direction = 'South'
       self.rover_position = [0, 0]

       # Create a new instance of the path for each rover traversal
       path = [row[:] for row in self.initial_path]

       with open(f"path_{rover_number}.txt", "w+") as file:
           with self.lock:
               path[0][0] = "*"
           moves = self.fetch_rover_moves(rover_number)

           for move in moves:
               if move == 'M':
                   result = self.move_forward(path)
                   if result == "Dead":
                       self.rover_status = "Dead"
                       break
               elif move == 'L':
                   self.rover_direction = self.turn_left()
               elif move == 'R':
                   self.rover_direction = self.turn_right()
               elif move == 'D':
                    self.check_mine(path)

           with self.lock:
               for row in path:
                   file.write(" ".join(row) + "\n")

if __name__ == "__main__":
   start_time = perf_counter()

   rover_controller = RoverController()

   with open("map.txt", "r") as file:
       rows_and_columns = file.readline().split()
       rows = int(rows_and_columns[0])
       columns = int(rows_and_columns[1])

       rover_controller.initial_path = [line.split() for line in file]

   rover_controller.initial_path[0][0] = "*"

   for i in range(1, 11, 1):
       rover_controller.initiate_rover_traversal(i)
       print("Completed " + str(i) + " traversal")

   end_time = perf_counter()

   print(f'SEQUENTIAL EXECUTION COMPLETED: {end_time - start_time:0.2f} SECOND(S) TO COMPLETE!')

   seq_done = 1

   def create_array_thr():
       with open("map.txt", "r") as file:
           global rows, columns
           path = [line.split() for line in file]

   def thr2():
       rover_controller.rover_status = "Active"
       rover_controller.rover_direction = 'South'
       rover_controller.rover_position = [0, 0]
       rover_controller.initial_path[0][0] = "*"

       for i in range(1, 11, 1):
           rover_controller.initiate_rover_traversal(i)

   if seq_done == 1:
       user_input = input("NOW DO YOU WISH TO RUN THE MULTITHREADED EXECUTION? (y/n): ")
       if user_input == 'y':
           start_time = perf_counter()

           t1 = Thread(target=create_array_thr)
           t2 = Thread(target=thr2)

           t1.start()
           t2.start()

           t1.join()
           t2.join()

           end_time = perf_counter()

           print(f'MULTITHREADED EXECUTION COMPLETED: {end_time - start_time:0.2f} SECOND(S) TO COMPLETE!')