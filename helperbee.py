import os

class HelperBEE:
    def __init__(self):
        pass
    
    def get_accelerometer():
        pass

    def get_potentiometer():
        pass
    
    def get_buttons():
        pass

    def get_gestures():
        pass
    
    def get_temperature():
        pass
    
    def get_path():
        return os.getcwd() 
    
    def get_installed_apps():
        return [app for app in os.listdir(HelperBEE.get_path()+"/apps/") if app[0] != "."]