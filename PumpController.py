from gpiozero import Motor

class PumpController:
    def __init__(self,input_pin1: int = 18, input_pin2: int = 16) -> None:

        self.pump = Motor(
            forward = input_pin1,
            backward = input_pin2,
            pwm = True
        )
    print("Der Motor wurde initialisiert!")

    def set_speed(self,speed:int) -> None:

        if not isinstance(speed,int) or not 0 <= speed <= 100:
            raise ValueError("Geschwindigkeit muss höher als 0 sein!")

        if speed == 0:
            self.stop()
        else:
            self.pump.forward(speed = speed/100)
            print(f'Status: Pumpe wurde gestartet. Geschwindigkeit: {speed}%')

    def stop(self) -> None:
        self.pump.stop()
        print("Pumpe wurde ausgeschaltet!")

    def close(self) -> None:
        self.pump.close()
