import machine, time
import lvgl as lv
import os
import fs_driver
from st7789 import St7789, ST77XX_PORTRAIT, ST7789_WRCACE  # 假设文件名存为 st77xx.py
# 硬件 SPI
spi=machine.SPI(
    2,
    baudrate=8_000_000,
    polarity=0,
    phase=0,
    sck=machine.Pin(12,machine.Pin.OUT),
    mosi=machine.Pin(11,machine.Pin.OUT),
    miso=None
)

cs  = 10    # 片选 CS
dc  = 8    # 数据/命令 DC
rst = 9   # 复位 RST
bl  = machine.Pin(7, machine.Pin.OUT)   # 直接当普通输出脚
bl.value(1)   # 开背光

# 创建屏对象：分辨率 240x240，横屏，BGR 常见为 True（很多 ST7789 模块用 BGR）
tft = St7789(
    res=(240,240),
    cs=cs, dc=dc, rst=rst, bl=None,
    spi=spi,
    rot=ST77XX_PORTRAIT,
    bgr=False
)
tft.apply_rotation(0) #屏幕旋转控制 0 1 2 3 
tft.write_register(ST7789_WRCACE, b"\x00")
def rgb565(r,g,b): return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
tft.clear(rgb565(255,255,255))


import time
print("LVGL", lv.version_major(), lv.version_minor(), lv.version_patch())
scr = lv.obj()
bar = lv.bar(scr)
bar.set_size(200, 20)
bar.align(lv.ALIGN.CENTER, 0, 0)
bar.set_value(0, 0)

label = lv.label(scr)
label.align(lv.ALIGN.CENTER, 0, 30)
lv.screen_load(scr)

for i in range(101):
    bar.set_value(i, 1)
    label.set_text("Progress: {}%".format(i))
    time.sleep_ms(50)



