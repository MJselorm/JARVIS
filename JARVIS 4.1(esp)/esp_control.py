import requests
from server_scan import esp_ip

ESP_IP = esp_ip
class ESPController():
    def __init__(self, ip):
        self.ip = ip
    def led_on(self):
        requests.get(f"http://{self.ip}/ON")

    def led_off(self):
        requests.get(f"http://{self.ip}/OFF")
    
    def red_light(self):
        requests.get(f"http://{self.ip}/RED")
    
    def blue_light(self):
        requests.get(f"http://{self.ip}/BLUE")
        
    def green_light(self):
        requests.get(f"http://{self.ip}/GREEN")
    
    def white_light(self):
        requests.get(f"http://{self.ip}/WHITE")
    
    def yellow_light(self):
        requests.get(f"http://{self.ip}/YELLOW")

if __name__ == "__main__":
    controller = ESPController(ESP_IP)
    controller.led_on()
    input("Press Enter to turn off the LED...")
    controller.led_off()