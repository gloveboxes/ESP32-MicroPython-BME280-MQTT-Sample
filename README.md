# Streaming Data from ESP32 using MicroPython and MQTT

## Resources 

* [MicroPython and ESP32](https://github.com/micropython/micropython-esp32)
* [MicroPython](https://micropython.org/)
* [MicroPython libraries](https://github.com/micropython/micropython-lib)
* [MicroPython PiP Package Index](https://pypi.python.org/pypi?%3Aaction=search&term=micropython)
* [ESP8266 Documentation (ESP32 not documeneted yet)](http://docs.micropython.org/en/latest/esp8266/)
* [ESP32 Firmware](http://micropython.org/download/#esp32)
* [Adafruit MicroPython Resources](https://www.google.com.au/search?client=ubuntu&hs=h2P&channel=fs&q=adafruit+micropython&spell=1&sa=X&ved=0ahUKEwii1ITmhpDVAhUEXrwKHY3YDoUQvwUIIygA&biw=1221&bih=626)

### uMqtt PiP Packages

* [umqtt.simple](https://github.com/micropython/micropython-lib/tree/master/umqtt.simple)
* [umqtt.robust](https://github.com/micropython/micropython-lib/tree/master/umqtt.robust)

### Other

* [MicroPython BME280 Sensor Driver](https://github.com/catdog2/mpy_bme280_esp8266/blob/master/bme280.py)
* [NTP Library](https://stackoverflow.com/questions/12664295/ntp-client-in-python)
* [Hackster MicroPython Mqtt Project](https://www.hackster.io/bucknalla/mqtt-micropython-044e77)
* [Espressif esptool](https://github.com/espressif/esptool)
* [Mosquitto Broker](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-the-mosquitto-mqtt-messaging-broker-on-ubuntu-16-04)

## ESP32 MicroPython Firmware Flashing Process

See [Adafruit MicroPython Flasing How-to Tutorial](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/esp8266)


### Overview of ESP32 flashing process

1. Install esptool
2. Erase Flash
3. Deploy MicroPython Firmware


### Install esptool.py firmware flash tool

On Windows
```bash
pip install esptool
```

On Mac and Linux
```bash
sudo pip install esptool
```


### Erasing ESP32 flash

```bash
esptool.py --port /dev/ttyUSB0 erase_flash
```

### Flashing ESP32 MicroPython firmware

Download [ESP32 Firmware](http://micropython.org/download/#esp32) and deploy to ESP32.

```bash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash 0x0000 firmware.bin
```


## Installing Required MicroPython PIP Packages

Install the following uPip packages. You need to estabish a network connection on the ESP32 board then upip.install the umqtt packages.

```python
import network
import upip

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Wifi SSID", "Wifi password")

upip.install('micropython-umqtt.simple')
upip.install('micropython-umqtt.robust')

```



## MicroPython and Publish over MQTT

Deploy the boot.py and main.py files using the Adafruit ampy package.

See [Adafruit MicroPython Tool (ampy)](https://learn.adafruit.com/micropython-basics-load-files-and-run-code/install-ampy) for information on copying files to the ESP32.

```bash
pip install adafruit-ampy

ampy --port /dev/ttyUSB0 put boot.py
ampy --port /dev/ttyUSB0 put main.py
```

```python
# boot.py

import network
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect("Wifi SSID", "Wifi password")
```



```python
# main.py

from umqtt.robust import MQTTClient
import machine
import utime as time
import gc
import bme280


# Wifi connect established in the boot.py file. Uncomment if needed
# import network
# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect("NCW", "malolos5459")

client = MQTTClient("esp32-01", "192.168.1.122")
pin5 = machine.Pin(5, machine.Pin.OUT)

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)

def checkwifi():
    while not sta_if.isconnected():
        time.sleep_ms(500)
        print(".")
        sta_if.connect()

def publish():
    count = 1
    while True:
        pin5.value(0)
        checkwifi()
        v = bme.values
        msg = b'{"MsgId":%u,"Mem":%u,"Celsius":%s,"Pressure":%s,"Humidity":%s}' % (count, gc.mem_free(), v[0][:-1], v[1][:-3], v[2][:-1])
        client.publish(b"home/weather", msg)
        pin5.value(1)
        count = count + 1
        time.sleep(20)

client.reconnect()

publish()
```

## Connecting to ESP32 with Putty

Install Putty for your platform. Connect at 115200 baud rate

See [Adafruit Serial REPL Tutorial](https://learn.adafruit.com/micropython-basics-how-to-load-micropython-on-a-board/serial-terminal).
