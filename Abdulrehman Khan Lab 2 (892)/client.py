import grpc
import rover_pb2
import rover_pb2_grpc
import sys


def run_rover(rover_number):
   # Connect to the server
   channel = grpc.insecure_channel('localhost:00008')
   stub = rover_pb2_grpc.RoverControlStub(channel)


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


   # Request mine serial numbers from server
   print("Client: Requesting mine serial numbers from server")
   mine_serial_response = stub.GetMineSerialNumber(rover_pb2.MineSerialNumberRequest())
   print("Client: Received mine serial numbers from server:")
   print(mine_serial_response.mine_data)


   # Share mine PIN with the server
   for mine_data in mine_serial_response.mine_data:
       mine_serial_number, mine_name = mine_data.split(',')
       print(f"Client: Requesting PIN for {mine_data} from server")
       pin_response = stub.ShareMinePin(rover_pb2.MinePinRequest(mine_serial_number=mine_serial_number))
       print(f"Client: Received PIN for {mine_data} from server: {pin_response.mine_pin}")


   # Notify server about execution status for the rover
   print(f"Client: Notifying server about execution status for Rover {rover_number}")
   status_response = stub.NotifyExecutionStatus(rover_pb2.StatusRequest(rover_number=rover_number))
   print(f"Client: Server acknowledged execution status for Rover {rover_number}: {status_response.status_received}")


if __name__ == '__main__':
   if len(sys.argv) != 2:
       print("Usage: python client.py [rover_number]")
       sys.exit(1)
  
   rover_number = int(sys.argv[1])
   run_rover(rover_number)
