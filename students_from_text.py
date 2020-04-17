import json
import argparse
import os
import re

parser = argparse.ArgumentParser(description='Converts Raw Text File of Directory to a list of students.')
parser.add_argument('--path', type=str, nargs='?',
                    help='path to raw text file')
args = parser.parse_args()
path = args.path

students = {}
email_list = []

clusters = ['WQN', 'WQS', 'ABB', 'FLG', 'PKN']

with open(path, 'r', encoding='utf-8') as f:
    raw_content = f.readlines()

cleaned_content = [i.rstrip('\n') for i in raw_content if ',' in i]
for i in cleaned_content:
    student_info = {}
    info_list = i.split(' ')
    student_info['email'] = info_list[-1]
    email_list.append(info_list[-1])
    living_location_str = ''
    name = i.split(',')[1].split(' ')[1] + ' ' + i.split(',')[0]
    #print(name)
    for i in range(len(info_list)-2, 0, -1):
        if info_list[i] in clusters:
            student_info['cluster'] = info_list[i]
            student_info['enter_year'] = info_list[i-1]
            student_info['class'] = info_list[i-3]
            student_info['blue_card'] = info_list[i-4]
            break
        living_location_str = info_list[i] + ' ' + living_location_str
    student_info['living_location'] = living_location_str
    students[name] = student_info

#print(students)
with open('students.json', 'w') as f:
    json.dump(students, f)

with open('emails.csv', 'w') as f:
    for email in email_list:
        f.write('%s\n' % email)
