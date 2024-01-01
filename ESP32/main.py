import network
import utime
import ntptime
import time
from datetime import datetime

from machine import Pin, SoftI2C
from time import sleep
import ssd1306

import dht
import machine
from time import sleep
import network

import onewire, ds18x20
import urequests


middleware_url = 'http://192.168.31.18:6000/send_data'


ds_pin = Pin(19)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


d = dht.DHT11(machine.Pin(4))


# 创建i2c对象
i2c = SoftI2C(scl=Pin(5), sda=Pin(18))

# 宽度高度
oled_width = 128
oled_height = 32#64 

# 创建oled屏幕对象
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)



sta_if = network.WLAN(network.STA_IF)  # 配置wifi模式为station
if not sta_if.isconnected():   # 判断有无连接
    print('connecting to network...')
    sta_if.active(True)        # 激活wifi接口
    sta_if.connect('FQ_3', '1223334444@')  # 连接现有wifi网络，需要替换为已知的热点名称和密码
    while not sta_if.isconnected():
        utime.sleep(1)   # 未连接上就等待一下，直到连接成功
print('network config:', sta_if.ifconfig())  # 输出当前wifi网络给自己分配的网络参数


def read_ds_sensor():
    roms = ds_sensor.scan()
    print('发现设备: ', roms)
    ds_sensor.convert_temp()
    for rom in roms:
        temp = ds_sensor.read_temp(rom)
        if isinstance(temp, float):
            temp = round(temp, 2)
            return temp
    # return 0  # 这里删除，那么默认此函数在没有获取到温度的时候返回为默认值None，调用处判断即可



def send_data_to_middleware(temp, moisture):
    data = {'temp': temp, 'moisture': moisture}
    headers = {'Content-Type': 'application/json'}
    try:
        response = urequests.post(middleware_url, json=data, headers=headers)
        print(response.text)
    except Exception as e:
        print('Error sending data:', e)




while True:
    d.measure()
    data1 = "%sRH" % (d.humidity())
    data2= str(read_ds_sensor())
    print(data1)
    print(data2)
   
    
    # 时间元组
    time_tuple = time.localtime()
    # 将时间元组转换为秒数
    timestamp = utime.mktime(time_tuple)
    # 使用时间戳创建时间结构体
    time_struct = utime.localtime(timestamp)
    # 格式化时间字符串
    formatted_time = "{:04d}-{:02d}-{:02d}-{:02d}:{:02d}:{:02d}".format(
        time_struct[0], time_struct[1], time_struct[2], time_struct[3], time_struct[4], time_struct[5]
    )
    print(formatted_time)
    oled.fill(0);
    oled.show();
    oled.text(formatted_time, 0, 0)
    oled.text('Humi:', 0, 10)
    oled.text(data1, 50, 10)
    oled.text('Temp:', 0, 20)
    oled.text(data2, 50, 20)
    oled.show()
    send_data_to_middleware(data2, data1)
    sleep(5)
    
