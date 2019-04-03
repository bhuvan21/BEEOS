import os
from SensorBEE import SensorBEE
from WifiBEE import WifiBEE
from EmailBEE import EmailBEE

class HelperBEE:
    def __init__(self):
        self.sensors = SensorBEE()
        self.wifi = WifiBEE()
        self.email = EmailBEE()
        os.system("gpio -g mode 19 pwm")
        self.set_display_brightness(255)
        self.brightness = 255

    def get_app_path(self):
        return os.getcwd() + "/apps/"
    
    def get_bee_path(self):
        return os.getcwd()
    
    def get_installed_apps(self):
        return [app for app in os.listdir(HelperBEE.get_path()+"/apps/") if app[0] != "."]
    
    def sleep_display(self):
        os.system("DISPLAY=:0.0 xset dpms force off")
    
    def hard_sleep_display(self):
        os.system("gpio -g pwm 19 0")
    
    def hard_wake_display(self):
        os.system("gpio -g pwm 19 {}".format(val))

    def wake_display(self):
        os.system("DISPLAY=:0.0 xset dpms force on")
    
    def set_display_brightness(self, val):
        if not(0 <= val <= 255):
            return
        os.system("gpio -g pwm 19 {}".format(25 + (val/255.0*75)))
        self.brightness = val


helper = HelperBEE()