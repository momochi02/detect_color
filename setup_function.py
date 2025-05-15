import os
import subprocess
import shlex
from path import *
def run_adb(command_line, shell=False):
    """
    Chạy lệnh adb từ một chuỗi lệnh đầy đủ.
    Tự động tách lệnh bằng shlex (hỗ trợ dấu ngoặc kép).

    Ví dụ:
    run_adb('pull "/sdcard/My Folder/file.txt" "C:/Users/Me/Desktop/"')
    """
    if isinstance(command_line, str):
        cmd_parts = shlex.split(command_line)
    else:
        raise ValueError("Lệnh phải là một chuỗi.")

    if cmd_parts[0] != 'adb':
        cmd_parts.insert(0, 'adb')

    try:
        print(f"cmd_parts {cmd_parts}")
        result = subprocess.run(cmd_parts, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True, shell=shell, check=True)
        if result.stdout.strip():
            print(result.stdout.strip())
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ADB ERROR] Lệnh thất bại: {' '.join(cmd_parts)}")
        print(e.stderr.strip())
        return None
def capture_and_pull(self):
    run_adb('pull "/sdcard/My Folder/screen.png" "C:/Users/Me/Desktop/Test Folder/"')
    run_adb('shell screencap -p "/sdcard/screen.png"')
    run_adb('shell uiautomator dump "/sdcard/window_dump.xmls"')

# images_dir = "D:/2_AI/Detect_color/downloads/images"
# xmls =r'D:/2_AI/Detect_color/download/xmls'
# output = 'D:/2_AI/Detect_color/output'
# crop_dir = 'D:/2_AI/Detect_color/crop_image'

def create_dir(log_path):
    path_dir =log_path
    if os.path.isfile(log_path):
        path_dir = os.path.dirname(log_path)
    elif os.path.isdir(log_path):
        path_dir = os.path.abspath(log_path)
    if not os.path.exists(log_path):
        os.makedirs(path_dir, exist_ok=True)

create_dir(output)
create_dir(crop_dir)