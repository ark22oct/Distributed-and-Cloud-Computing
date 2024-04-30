import pika
import sys
import hashlib


class Deminer:
   def __init__(self, deminer_number):
       self.deminer_number = deminer_number
       self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
       self.channel = self.connection.channel()
       self.channel.queue_declare(queue='Demine-Queue')
       self.channel.exchange_declare(exchange='Defused-Mines', exchange_type='fanout')


   def start_listening_for_tasks(self):
       self.channel.basic_consume(queue='Demine-Queue', on_message_callback=self.handle_task, auto_ack=True)
       print(f"Deminer {self.deminer_number} started.")
       print("Subscribed to Demine-Queue channel.")
       print(f"Deminer {self.deminer_number} listening for tasks")
       self.channel.start_consuming()


   def handle_task(self, ch, method, properties, body):
       task = body.decode()
       if task == "END":
           print(f"Deminer {self.deminer_number} has completed all tasks.")
           ch.stop_consuming()  # Stop consuming messages from the queue
       else:
           mine_info = task.split(', ')
           if len(mine_info) >= 3:  # Ensure that mine_info contains enough elements
               mine_id = mine_info[0].split(': ')[1]
               serial_number = mine_info[-1].split(': ')[1]  # Extract serial number from the last element
              
               print(f"Deminer {self.deminer_number} received task:", task)
               print("Mine ID:", mine_id)
               print("Serial Number:", serial_number)
              
               # Demining logic
               pin = self.generate_mine_pin(serial_number)
               print(f"Deminer {self.deminer_number} generated PIN for mine {mine_id}: {pin}")
              
               # Publish the mine's PIN to the RabbitMQ exchange for ground control
               self.publish_pin(mine_id, pin)
              
           else:
               print("Invalid mine task format:", task)


   def publish_pin(self, mine_id, pin):
       # Publish the PIN to the RabbitMQ exchange for ground control
       self.channel.basic_publish(exchange='Defused-Mines', routing_key='', body=f"Mine_ID: {mine_id}, PIN: {pin}")
       print(f"Published PIN of the mine {mine_id} on the Defused-Mines channel.")


   def generate_mine_pin(self, mine_serial_number):
       prefix = "SNOW"
       temporary_mine_key = prefix + mine_serial_number
       for i in range(1000000):
           pin_attempt = temporary_mine_key + str(i)
           hashed_pin = hashlib.sha256(pin_attempt.encode()).hexdigest()
           if hashed_pin.startswith("00000"):
               return pin_attempt
       return "No valid PIN found"


if __name__ == '__main__':
   if len(sys.argv) != 2:
       print("Usage: python deminer.py [deminer_number]")
       sys.exit(1)


   deminer_number = int(sys.argv[1])
   deminer = Deminer(deminer_number)
   deminer.start_listening_for_tasks()