import qrcode
import tkinter as tk
from PIL import ImageTk, ImageDraw, ImageFont
import time

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# 此处设置时间 单位:s
time = int(config.get('Settings', 'time'))
# 此处设置字体大小
fontSize = int(config.get('Settings', 'fontSize'))
# 此处设置颜色1
color1 = config.get('Settings', 'color1')
# 此处设置颜色2
color2 = config.get('Settings', 'color2')


def modify_qrcode(qr_img, text_to_add, color):
    img = qr_img.copy()
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 20)
    draw.text((10, 10), text_to_add, font=font, fill=color)
    return img


def update_image():
    global current_data_index
    # print(data_list[current_data_index])

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_list[current_data_index])
    # qr = qrcode.make(data_list[current_data_index])
    color = [color1, color2]
    img = qr.make_image(fill_color=color[current_data_index % 2])
    modified_img = modify_qrcode(img, data_list[current_data_index], color[current_data_index % 2])
    tk_modified_img = ImageTk.PhotoImage(modified_img)

    label.config(image=tk_modified_img)
    label.image = tk_modified_img

    current_data_index = current_data_index + 1

    root.after(time * 1000, update_image)


root = tk.Tk()
root.title("Real-time QR Code")

inn = open("in.txt", 'r', encoding='utf-8')
cnt = 0
data_list = []
while True:
    data = inn.readline()
    data = data.strip()
    if not data:
        break
    cnt += 1
    data_list.append(data)

current_data_index = 0

original_data = "Initial Data"
original_qr = qrcode.make(original_data)
tk_original_img = ImageTk.PhotoImage(original_qr)

label = tk.Label(root, image=tk_original_img)
label.pack()

update_image()

root.mainloop()
