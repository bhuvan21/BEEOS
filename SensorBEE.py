import serial
import threading
import queue

class SensorBEE():
    def __init__(self, dev_node="ttyACM0"):
        self.dev_node = "/dev/" + dev_node
        try:
            self.ser = serial.Serial(self.dev_node)
        except serial.serialutil.SerialException:
            print("Not running on Pi?")
    
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
    
    def get_split_values(self):
        return [x for x in self.get_raw().split(":") if x != ""]
    
    def get_option_button(self):
        return int(self.get_split_values()[0])
    
    def get_home_button(self):
        return int(self.get_split_values()[2])
    
    def get_back_button(self):
        return int(self.get_split_values()[1])
    
    def get_volume_slider(self):
        return int(self.get_split_values()[3])

    def get_temperature(self):
        return float(self.get_split_values()[4])
    
    def get_raw_accel_x(self):
        return int(self.get_split_values()[5])

    def get_raw_accel_y(self):
        return int(self.get_split_values()[6])

    def get_raw_accel_z(self):
        return int(self.get_split_values()[7])

    def get_accel_x(self):
        return float(self.get_split_values()[8])

    def get_accel_y(self):
        return float(self.get_split_values()[9])

    def get_accel_z(self):
        return float(self.get_split_values()[10])

    def get_proximity(self):
        return int(self.get_split_values()[11])
    
class SmartSensorBee():
    def __init__(self, dev_node="ttyACM0"):
        self.sensorbee = SensorBEE(dev_node=dev_node)
        self.queue = queue.Queue()
        self.thread = threading.Thread(None, self.refresh)
        self.thread.setDaemon(True)
        self.thread.start()

    def refresh(self):
        self.queue.put(self.sensorbee.get_split_values())
        self.refresh()
    
    def get_split_values(self):
        reading = 0
        while True:
            try:
                reading = self.queue.get(block=False)
            except queue.Empty:
                break
        return reading