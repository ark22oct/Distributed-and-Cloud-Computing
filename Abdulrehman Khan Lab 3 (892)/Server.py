import hashlib
from concurrent import futures
import time
import grpc
import rover_pb2
import rover_pb2_grpc
import requests
import pika


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class RoverControl(rover_pb2_grpc.RoverControlServicer):
   def __init__(self):
       self.map_data = []
       with open('map.txt', 'r') as f:
           for line in f:
               self.map_data.append(list(line.strip()))


       # Connect to RabbitMQ server
       self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
       self.channel = self.connection.channel()


       # Declare the queue for receiving demining tasks
       self.channel.queue_declare(queue='Demine-Queue')
      
       # Declare the exchange for publishing defused mines
       self.channel.exchange_declare(exchange='Defused-Mines', exchange_type='fanout')

       print("Ground Control Server started.")
       print("Subscribed to Defused-Mines channel.")


   def GetMap(self, request, context):
       # Send current map data to the client
       print(f"\n(Server) Received request for map, retrieving...")
       return rover_pb2.MapResponse(map_data=[''.join(row) for row in self.map_data])


   def GetCommands(self, request, context):
       rover_number = request.rover_number
       url = f'https://coe892.reev.dev/lab1/rover/{rover_number}'
       response = requests.get(url)
       commands = response.json()['data']['moves']
       print(f"\n(Server) Received request for commands, retrieving...")
       return rover_pb2.CommandResponse(commands=commands)


   def GetMineSerialNumber(self, request, context):
       with open('mines.txt', 'r') as f:
           mine_data = [line.strip() for line in f.readlines()]
       print(f"\n(Server) Received request for serial numbers, retrieving...")
       return rover_pb2.MineSerialNumberResponse(mine_data=mine_data)

   def ShareMinePin(self, request, context):
       mine_serial_number = request.mine_serial_number
       print(f"\n(Server) Received request for PIN for mine {mine_serial_number}")
       self.publish_mine_data_to_deminer(mine_serial_number)
       return rover_pb2.MinePinResponse()


   def publish_mine_data_to_deminer(self, mine_serial_number):
       # Publish the mine serial number to the RabbitMQ queue
       self.channel.basic_publish(exchange='', routing_key='Demine-Queue', body=mine_serial_number)
       print(f"(Server) Published mine serial number {mine_serial_number} to Demine-Queue")


   def NotifyExecutionStatus(self, request, context):
       rover_number = request.rover_number
       # Update path and write to file
       with open('path.txt', 'a') as f:
           f.write(f'Rover {rover_number} traversed:\n')
           for row in self.map_data:
               f.write(''.join(row) + '\n')
           f.write('\n')
       print(f"\n(Server) Received execution status for Rover {rover_number}")
       return rover_pb2.ExecutionStatusResponse(status_received=True)


def serve():
   server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
   rover_pb2_grpc.add_RoverControlServicer_to_server(RoverControl(), server)
   server.add_insecure_port('[::]:00008')
   server.start()
   print("Server listening on [::]:00008")
   try:
       while True:
           time.sleep(_ONE_DAY_IN_SECONDS)
   except KeyboardInterrupt:
       server.stop(0)


if __name__ == '__main__':
   serve()
