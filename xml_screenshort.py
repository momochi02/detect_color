import os
import cv2
import xml.etree.ElementTree as ET
import subprocess
from collections import Counter

# from humanfriendly.terminal import output
from hex_color import *
from setup_function import *

import testmate
d = testmate.connect()


# === Lấy XML và ảnh từ thiết bị ===


#
# def get_ui_xml_and_screenshot():
#     run_adb('shell screencap -p /sdcard/screen.png')
#     run_adb(f'pull /sdcard/screen.png {images_dir}/screen.png')
#     xml_txt = d.dump_hierarchy()
#     with open(f"{xmls}/window_dump.xmls", "w", encoding="utf-8") as f:
#         f.write(xml_txt)
#     print("Đã lấy ảnh và XML từ thiết bị.")




# === Chuyển [x1,y1][x2,y2] thành tuple ===
def parse_bounds(bounds_str):
    bounds_str = bounds_str.replace('[', '').replace(']', ',')
    x1, y1, x2, y2 = map(int, bounds_str.strip(',').split(','))
    return (x1, y1), (x2, y2)
count =0


color_code="unKnwon"
# === Vẽ box và text ===
def annotate_image(xml_file, image_file, output_file=f'{output}/screen_annotated.png'):
    image = cv2.imread(image_file)
    tree = ET.parse(xml_file)
    root = tree.getroot()
    count =0
    for node in root.iter('node'):
        resourceID  = node.attrib.get('resourceId', '').strip()
        class_name = node.attrib.get('class', '').strip()
        text = node.attrib.get('text', '').strip()
        bounds = node.attrib.get('bounds', '')
        if  not bounds or ( not text and 'status_bar_contents' in resourceID or 'left_clock_container' in resourceID):
            print("Continue")
            continue
        # if (text or "Button" in class_name or "ImageView" in class_name) and bounds:
        if text and bounds:
            pt1, pt2 = parse_bounds(bounds)
            # Crop ảnh và lưu
            crop = image[pt1[1]:pt2[1], pt1[0]:pt2[0]]
            label = text if text else class_name
            crop_filename = f"{crop_dir}/crop_{count:03}_{label.replace('/', '_')}.png"
            cv2.imwrite(crop_filename, crop)
            # Check color on image croped
            # print(f"crop_filename {crop_filename}")
            bg_color, text_color=GetColor().extract_colors(crop_filename)
            print("Background color:", bg_color)
            print("Text color:", text_color)

            # Vẽ box, color_code

            cv2.rectangle(image, pt1, pt2, (0, 0, 0), 2)
            cv2.putText(image, text + ": " + bg_color + text_color, (pt1[0], pt1[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 225), 2)


            count += 1




    cv2.imwrite(output_file, image)
    print(f"Đã lưu ảnh khoanh vùng: {output_file}")
    print(f"Đã crop và lưu {count} ảnh vào thư mục: {crop_dir}")

 # === Chạy toàn bộ ===
# get_ui_xml_and_screenshot()

annotate_image(f'{xmls}/window_dump.xml', f'{images_dir}/screen.png')


