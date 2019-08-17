try:
    from secrets import WIFI_SSID, WIFI_KEY, STATSD_HOST
except ImportError:
    WIFI_SSID = 'exmaple'
    WIFI_KEY  = 'MaplesAreFun!'
    STATSD_HOST = '10.1.2.3'

STATSD_PORT = 8125
I2C_ADDRESS = 0x77  # 0x76 if SD0 is grounded
STATION_ALIAS = 'main'

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_KEY)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

# legacy tested method for bmp280
def bmp280_get_sensor_values():
    from machine import I2C, Pin
    from bmp280 import BMP280
    bus = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    bmp = BMP280(bus, addr=I2C_ADDRESS)
    return bmp.temperature, bmp.pressure, None

# i think this one works on both sensors
# assumes SCL -> D1 Pin(5) and SDA -> D2 Pin(4)
# temperature, pressure, humidity
def bme280_get_sensor_values()
    from machine import I2C, Pin
    import bme280_float
    bus = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
    bme = bme280_float.BME280(i2c=bus, address=I2C_ADDRESS)
    return bme.read_compensated_data()

def send_gauge(name, value, port=STATSD_PORT, host=STATSD_HOST):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(name + ":" + str(value) + "|g", (host, port))

def do_sleep(stime):
    import machine

    # configure RTC.ALARM0 to be able to wake the device
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # set RTC.ALARM0 to fire after 10 seconds (waking the device)
    rtc.alarm(rtc.ALARM0, stime * 1000)

    # put the device to sleep
    print("entering deep sleep for %s seconds" % stime)
    machine.deepsleep()

# For debugging, it's handy to run set_sleep_time(5) to make the loop very short
# For production, it's handy to run set_sleep_time(120) to save battery and reduce traffic
def set_sleep_time(stime):
    with open('sleep_time', 'w') as out:
        out.write(str(stime))
def get_sleep_time():
    try:
        with open('sleep_time', 'r') as inp:
            return int(inp.read())
    except Exception:
        print("Warning: sleep time unconfigured")
        return 10

def main():
    import time

    INHG_TO_PA = 3386.39
    do_connect()
    t, p, h = bme280_get_sensor_values()
    p_hg = p / INHG_TO_PA
    print("Temp : %.2f C" % t)
    print("Press: %.2f Pa" % p)
    print("Press: %.2f in Hg" % p_hg)
    print("Humidity: %.2f %%" % h)
    send_gauge('espws.main.temperature', t)
    send_gauge('espws.main.pressure', p_hg)
    send_gauge('espws.main.humidity', h)
    time.sleep(2)

    do_sleep(get_sleep_time())

if __name__ == '__main__':
    main()
