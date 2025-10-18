import serial
import time

class ArduinoController:
    def __init__(self, port='COM4', baudrate=9600):
        try:
            self.arduino = serial.Serial(port, baudrate)
            time.sleep(2)
            print(f"Arduino bağlantısı uğurlu ({port})")
        except Exception as e:
            print(f"Arduino tapılmadı və ya port bağlıdır: {e}")
            self.arduino = None

    def send_led_states(self, states):
        """
        Məsələn: states = '101' → göndərilir 'S101E' formatında
        """
        message = f"S{states}E"
        if self.arduino:
            self.arduino.write(message.encode())
            print(f"Arduinoya göndərildi: {message}")
        else:
            print(f"{states}")

    def close(self):
        if self.arduino:
            self.arduino.close()
            print("Arduino bağlantısı bağlandı.")
