import pytesseract 
import os
from PIL import Image
import json
import re
import argparse

parser = argparse.ArgumentParser(description='Converts PDF of Directory to a list of students.')
parser.add_argument('--path', type=str, nargs='?',
                    help='path to image folder')
args = parser.parse_args()
path = args.path

students = {}

for f in os.listdir(path):
    if os.path.isfile(os.path.join(path, f)) and f != '.DS_Store':
        file = Image.open(os.path.join(path, f))
        for i in range(6):
            crop_window = file.crop((360, 200+250*i, 650, 400+250*i))
            text = pytesseract.image_to_string(crop_window)
            print(text.split('\n'))
            info_list = list(filter(str, text.split('\n')))
            if (info_list):
                student_info = {}
                name = re.sub(u'\u201c', '"', info_list[0])
                name = re.sub(u'\u201d', '"', name) 
                offset = 0
                try:
                    student_info['enter_year'] = info_list[2+offset].split(' ')[3] 
                except IndexError:
                    offset=1
                    student_info['enter_year'] = info_list[2+offset].split(' ')[3]

                student_info['location'] = info_list[1+offset]
                student_info['blue_card'] = info_list[2+offset].split(' ')[0]
                student_info['class'] = info_list[2+offset].split(' ')[1]
                student_info['cluster'] = info_list[3+offset].split(' ')[0]
                student_info['living_location'] = ' '.join(info_list[3+offset].split(' ')[1:-1])
                if student_info['living_location'] == 'Will Hall Carriage':
                    offset+=1
                student_info['email'] = info_list[4+offset].replace(" ", "")
                students[name] = student_info

        #yes i know this is shitty code do i care?
        
        for i in range(6):
            crop_window = file.crop((910, 200+250*i, 1200, 400+250*i))
            text = pytesseract.image_to_string(crop_window)
            print(text.split('\n'))
            info_list = list(filter(str, text.split('\n')))
            if (info_list):
                student_info = {}
                name = re.sub(u'\u201c', '"', info_list[0])
                name = re.sub(u'\u201d', '"', name) 
                offset = 0
                try:
                    student_info['enter_year'] = info_list[2+offset].split(' ')[3] 
                except IndexError:
                    offset=1
                    student_info['enter_year'] = info_list[2+offset].split(' ')[3]
                student_info['location'] = info_list[1+offset]
                student_info['blue_card'] = info_list[2+offset].split(' ')[0]
                student_info['class'] = info_list[2+offset].split(' ')[1]
                student_info['cluster'] = info_list[3+offset].split(' ')[0]
                student_info['living_location'] = ' '.join(info_list[3+offset].split(' ')[1:-1])
                if student_info['living_location'] == 'Will Hall Carriage':
                    offset+=1
                student_info['email'] = info_list[4+offset].replace(" ", "")
                students[name] = student_info

print(students)
with open('students.json', 'w') as f:
    json.dump(students, f)
