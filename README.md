ESP-WeatherStation
------------------
Super simple micropython project for exploring sensor loops on the ESP8266 and ESP32.

Hardware
--------
* esp-8266
* bme-280 - temperature + pressure + humidity sensor (or bmp-280 - inferior substitute, temperature+pressure only)

Wiring
------
* 3.3V -> VCC
* GND -> GND
* D1 -> SCL
* D2 -> SDA
* D0 -> RST (both pins on esp-8266)
* VCC -> CSB -> SDO (all pins on bme-280)

Note
----
BME-280 uses I2C to communicate. If you have 4-pin devince you will need to
alter the address in the code to 0x76. If you have 6-pin device like me, wire
a jumper between VCC and the two opposite pins (CSB and SDO) in order to
configure for I2C address 0x77.

Quickstart
----------
* Copy all files to esp-8266 using [ampy](https://github.com/pycampers/ampy) `ampy put *`
* Use `minicom -D /dev/ttyUSB0 -b 115200 -8` or similar to interact with shell
* Ctrl-C during the mainloop to break to console and avoid deep-sleep
* Ctrl-D from console to restart the sensor loop
* you must quit `minicom` to use `ampy`
