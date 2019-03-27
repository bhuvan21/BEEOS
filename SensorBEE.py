import serial


class SensorBEE():
    def __init__(self, dev_node="ttyACM0"):
        self.dev_node = "/dev/" + dev_node
        self.ser = serial.Serial(self.dev_node, 0.01)
    
    def get_raw(self):
        total = ""
        read = 1
        self.ser.write(b"1")
        while True:
            read = self.ser.read()
            if read != b"":
                total += read
            else:
                break
        
        return total

