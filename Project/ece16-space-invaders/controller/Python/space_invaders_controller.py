"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
import ECE16Lib.DSP as filt
from time import sleep
import socket, pygame

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)
class PygameController:
  comms = None

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)

  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    while True:
      try:
        message = self.comms.receive_message()
        if(message != None):
          try:
            (m1,m2) = message.split(",")
          except ValueError:
            continue
          command = None
          if ((m1 is not None) and (m2 is not None)):
            m1 = int(m1)
            m2 = int(m2)
          else:
            continue
          # if message == 0:
          #   command = "FLAT"
          # if message == 1:
          #   command = "UP"
          if m2 == 1:
            mySocket.send("PAUSE".encode("UTF-8"))
          elif m2 == 2:
            mySocket.send("QUIT".encode("UTF-8"))
          elif m1 == 2:
            command = "FIRE"
          elif m1 == 3:
            command = "LEFT"
          elif m1 == 4:
            command = "RIGHT"
          elif m1 == 5:
            mySocket.send("LEFT".encode("UTF-8"))
            mySocket.send("FIRE".encode("UTF-8"))
          elif m1 == 6:
            mySocket.send("RIGHT".encode("UTF-8"))
            mySocket.send("FIRE".encode("UTF-8"))

          if command is not None:
            mySocket.send(command.encode("UTF-8"))

        server_message, _ = mySocket.recvfrom(1024)
        server_message = server_message.decode("UTF-8")
        if server_message == "SHOT":
          self.comms.send_message("shot")


      except KeyboardInterrupt:
        break

      except:
        continue

  def process(self):
    pass


if __name__== "__main__":
  serial_name = "/dev/cu.SLAB_USBtoUART"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")
