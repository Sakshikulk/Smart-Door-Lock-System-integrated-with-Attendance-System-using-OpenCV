import pyfirmata2
from pyfirmata2 import SERVO    
PORT = "COM7"

pin = 8
board = pyfirmata2.Arduino('COM7')



board.digital[pin].mode = SERVO

def rotateServo(pin, angle):
    # board.digital[pin].write(0)
    board.digital[pin].write(angle)
    # board.digital[pin].write(angle)

