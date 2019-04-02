import subprocess
import urllib.parse
import time

"""Credit to Atto Atlas for help"""

class WifiBEE():

    def get_all_ssids(block=True):
        ssids = []

        cmd = ["sudo", "iw", "wlan0", "scan"]

        return ["SSID1", "SSID2", "SSID3"]
        while block:
            try:
                network_data = subprocess.check_output(cmd)
                break
            except subprocess.CalledProcessError:
                time.sleep(0.5)

        ssid_split = network_data.split(b"SSID: ")
        del ssid_split[0]

        for ssid_string in ssid_split:
            ssid = ssid_string.split(b"\n")[0]

            ssids.append(ssid.decode())

        return ssids
        

    def get_current_ssid(self, block=True):
        command = ['iwgetid', '-r']
        try:
            
            while block:
                try:
                    connection_data = subprocess.check_output(command)
                    break
                except subprocess.CalledProcessError:
                    time.sleep(0.5)

            return self.from_hex_unicode_rep(connection_data)[:-1]
        except Exception as e:
            print(e)
            return "DummySSID"

    def from_hex_unicode_rep(self, ssid):
        ssid = ssid.decode('unicode-escape')
        ssid = ssid.encode('latin-1').decode('utf8')
        return urllib.parse.unquote(ssid)

    def mobile_connect(self, ssid, password):
        cmd = ["wpa_cli", "-i", "wlan0", "reconfigure"]
        str_to_write = '\n#mobile_connect\nnetwork={\n\tssid="%s"\n\tpsk="%s"\n\tpriority=2\n}' % (ssid, password)

        print(str_to_write)

        with open("/etc/wpa_supplicant/wpa_supplicant.conf", 'a') as fil:
            fil.write(str_to_write)

        time.sleep(2)

        update_wlan_config = subprocess.Popen(cmd)
        update_wlan_config.communicate()

        return