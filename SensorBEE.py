import serial


class SensorBEE():
    def __init__(self, dev_node="ttyACM0"):
        self.dev_node = "/dev/" + dev_node
        self.ser = serial.Serial(self.dev_node)
    
    def get_raw(self):
        total = ""
        self.ser.write(b"1")
        colon_count = 0
        while colon_count < 12:
            read = self.ser.read().decode("utf-8") 
            if read == ":":
                colon_count += 1
            total += read
        
        return total

