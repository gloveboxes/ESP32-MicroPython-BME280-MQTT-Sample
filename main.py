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

#upip packages - see README.md
# upip.install('micropython-umqtt.simple')
# upip.install('micropython-umqtt.robust')

client = MQTTClient("esp32-01", "192.168.1.122")
pin5 = machine.Pin(5, machine.Pin.OUT)

i2c = machine.I2C(scl=machine.Pin(22), sda=machine.Pin(21))
bme = bme280.BME280(i2c=i2c)

def initialise():
    blinkcnt = 0
    checkwifi()
    while blinkcnt < 50:
        pin5.value(blinkcnt % 2)
        blinkcnt = blinkcnt + 1
        time.sleep_ms(100)

def checkwifi():
    blinkcnt = 0
    while not sta_if.isconnected():
        time.sleep_ms(500)
        pin5.value(blinkcnt % 2)
        blinkcnt = blinkcnt + 1

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
        time.sleep(5)

initialise()

client.reconnect()

publish()
