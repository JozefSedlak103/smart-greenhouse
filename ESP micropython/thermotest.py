from machine import ADC, Pin
import time

class LDRthermo:
    def __init__(self, pin, min_value=0, max_value=100):
        if min_value >= max_value:
            raise Exception('Min value is greater or equal to max value')
        # initialize ADC (analog to digital conversion)
        self.adc = ADC(Pin(pin))
        # set 11dB input attenuation (voltage range roughly 0.0v - 3.6v)
        self.adc.atten(ADC.ATTN_11DB)
        self.min_value = min_value
        self.max_value = max_value
    def read(self):
        return self.adc.read()
    def value(self):
        return (self.max_value - self.min_value) * self.read() / 4095

def get_temperature():
    ldr = LDRthermo(33) 
    value = ldr.value()/1.8
    if value < 10:
        value += 10
    elif value > 30:
        value -= 10
    return value


