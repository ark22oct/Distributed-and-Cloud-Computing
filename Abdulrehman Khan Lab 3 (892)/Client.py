import grpc
import rover_pb2
import rover_pb2_grpc
import sys
import json
import pika


def run_rover(rover_number):
   # Connect to the gRPC server
   channel = grpc.insecure_channel('localhost:00008')
   stub = rover_pb2_grpc.RoverControlStub(channel)


   # Connect to RabbitMQ server
   connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
   channel_rabbit = connection.channel()


   # Request map data from server
   print("Client: Requesting map data from server")
   map_response = stub.GetMap(rover_pb2.MapRequest())
   print("Client: Received map data from server:")
   print(map_response.map_data)


   # Request commands for the rover from the server
   print(f"Client: Requesting commands for Rover {rover_number} from server")
   command_response = stub.GetCommands(rover_pb2.CommandRequest(rover_number=rover_number))
   print(f"Client: Received commands for Rover {rover_number} from server:")
   print(command_response.commands)


   # Explore the map and detect mines
   print("Client: Exploring the map and detecting mines")
   moves = command_response.commands
   for i, row in enumerate(map_response.map_data):
       for j, cell in enumerate(row):
           if cell == '1':
               print(f"Client: Found mine at coordinates ({i}, {j})")
               # Retrieve mine's serial number
               mine_serial_response = stub.GetMineSerialNumber(rover_pb2.MineSerialNumberRequest())
               for mine_data in mine_serial_response.mine_data:
                   mine_serial_number, mine_name = mine_data.split(',')
                   print(f"Client: Retrieved serial number for mine {mine_name}: {mine_serial_number}")
                   # Publish mine info to Demine-Queue channel
                   print("Client: Publishing mine info to Demine-Queue channel")
                   channel_rabbit.basic_publish(exchange='', routing_key='Demine-Queue', body=f"Mine_ID: {mine_name}, Coordinates: ({i}, {j}), Serial Number: {mine_serial_number}")
                   print("Client: Published mine info")


   # Notify server about execution status for the rover
   print(f"Client: Notifying server about execution status for Rover {rover_number}")
   status_response = stub.NotifyExecutionStatus(rover_pb2.StatusRequest(rover_number=rover_number))
   print(f"Client: Server acknowledged execution status for Rover {rover_number}: {status_response.status_received}")


   # Close RabbitMQ connection
   connection.close()


if __name__ == '__main__':
   if len(sys.argv) != 2:
       print("Usage: python client.py [rover_number]")
       sys.exit(1)
  
   rover_number = int(sys.argv[1])
   run_rover(rover_number)


