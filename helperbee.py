import os
from SensorBEE import SensorBEE
from WifiBEE import WifiBEE
from EmailBEE import EmailBEE

class HelperBEE:
    def __init__(self):
        self.sensors = SensorBEE()
        self.wifi = WifiBEE()
        self.email = EmailBEE()

    def get_app_path(self):
        return os.getcwd() + "/apps/"
    
    def get_bee_path(self):
        return os.getcwd()
    
    def get_installed_apps(self):
        return [app for app in os.listdir(HelperBEE.get_path()+"/apps/") if app[0] != "."]

helper = HelperBEE()