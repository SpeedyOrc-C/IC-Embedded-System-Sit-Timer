import requests
import time
import smbus2

# Sensor and I2C configuration
DEVICE_ADDRESS = 0x48
REG_CONVERSION = 0x00
REG_CONFIG = 0x01
CONFIG = 0xC383

def read_flex_sensor() -> int:
    bus = smbus2.SMBus(1)
    try:
        config_msb = (CONFIG >> 8) & 0xFF
        config_lsb = CONFIG & 0xFF
        bus.write_i2c_block_data(DEVICE_ADDRESS, REG_CONFIG, [config_msb, config_lsb])
        time.sleep(0.1)
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, REG_CONVERSION, 2)
        raw_adc = (data[0] << 8) | data[1]
        if raw_adc > 32767:
            raw_adc -= 65536
        return raw_adc
    finally:
        bus.close()
        
if __name__ == '__main__':
    while True:
        flex_value = read_flex_sensor()
        print(f'Flex sensor value: {flex_value}')
        time.sleep(1)