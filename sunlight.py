try:
    from secrets import WIFI_SSID, WIFI_KEY, SUNLIGHT_HOST
except ImportError:
    WIFI_SSID = 'exmaple'
    WIFI_KEY  = 'MaplesAreFun!'
    SUNLIGHT_HOST = '10.1.2.3'

SUNLIGHT_PORT = 4004
sleep_time = 100

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

def setup_pwm():
    import machine
    p12 = machine.Pin(12, mode=machine.Pin.OUT)
    pwm12 = machine.PWM(p12)
    pwm12.freq(1000)
    pwm12.duty(0)
    return pwm12

def get_setpoint():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SUNLIGHT_HOST, SUNLIGHT_PORT))
    sock.send(b"?\n")
    data = sock.recv(128)
    start, end, ramp_time, sleep_time = [int(x.strip()) for x in data.decode().strip().split(',')]
    return start, end, ramp_time, sleep_time

def do_ramp(pwm, start, end, ramp_time):
    import time

    if end == start:
        pwm.duty(start)
        time.sleep(ramp_time)
    else:
        step_time = abs(int(ramp_time * 1000 / (end - start)))
        for duty in range(start, end, -1 if end < start else 1):
            pwm.duty(duty)
            time.sleep_ms(step_time)

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

def main():
    import time

    pwm = setup_pwm()
    do_connect()

    sleep_time = 10
    while True:
        try:
            start, end, ramp_time, sleep_time = get_setpoint()
            print("do ramp", start, end, ramp_time)
            do_ramp(pwm, start, end, ramp_time)
            print("sleep", sleep_time)
            if sleep_time > 10 and (end == 0 or end == 1024):
                if end == 0:
                    pin = pwm.pin
                    pwm.deinit()
                    pin.off()
                elif end == 1024:
                    pin = pwm.pin
                    pwm.deinit()
                    pin.on()
                do_sleep(sleep_time)
            else:
                time.sleep(sleep_time)
        except Exception as e:
            print("err", e)
            time.sleep(sleep_time)
            continue


if __name__ == '__main__':
    main()
