import subprocess
import time

"""Credit to Atto Atlas for help"""

class WifiBEE():

    def get_all_ssids(block=True):
        ssid_list = []

        command = ["sudo", "iw", "wlan0", "scan"]

        while block:
            try:
                raw_network_data = subprocess.check_output(command)
                break
            except subprocess.CalledProcessError:
                time.sleep(0.5)

        print(raw_network_data)
        ssid_split = raw_network_data.split(b"SSID: ")
        del ssid_split[0]

        for ssid_string in ssid_split:
            ssid = ssid_string.split(b"\n")[0]

            ssid_list.append(ssid.decode())

        return ssid_list
