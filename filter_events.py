import json
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from os import listdir
import os.path
import csv

def read_json(json_file_name):
    with open(json_file_name, 'r') as file:
        data = json.load(file)
        return data

def write_json(jsonFileName, data):
    with open(jsonFileName, 'w') as file:
        json.dump(data, file, ensure_ascii=False, allow_nan=False)

def file_extract(inp_file_name):
    with ZipFile(inp_file_name, 'r') as zf:
        zf.extractall('temp')

def extract_input_to_temp():
    list_files = os.listdir('input/')
    for file_name in list_files:
        if(file_name.split(".")[-1] == 'zip'):
            file_extract(f'input/{file_name}')

def get_list_files():
    list_files = os.listdir('temp/')
    new_list = []
    for file_name in list_files:
        new_list.append(f'temp/{file_name}')
    return new_list

def clear_temp():
    dir = 'temp'
    if os.path.exists(dir):
        list_files = os.listdir(dir)
        for file in list_files:
            file_path = os.path.join(dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(dir)

def read_event(json_file_name, events):
    event = read_json(json_file_name)
    event_name = event['eventName']
    print(event_name)
    event_ = {}
    for runner in event['items']:
        age = runner['age']
        gender = runner['gender']
        #print(runner)

        if 'ages' not in event_:
            event_['ages'] = {}

        if age :
            if age not in event_['ages']:
                event_['ages'][age] = 0
            event_['ages'][age] += 1

        if 'genders' not in event_:
            event_['genders'] = {}

        if gender:
            if gender not in event_['genders']:
                event_['genders'][gender] = 0
            event_['genders'][gender] += 1
        events[event_name] = event_

def read_events(list_files):
    events = {}
    for event in list_files:
        read_event(event, events)
    return events

def pepare_filtered_events(json_file_name):
    clear_temp()
    extract_input_to_temp()
    list_files = get_list_files()
    events = read_events(list_files)
    write_json(json_file_name, events)

def get_age_set(events):
    ages_set = set()
    for event in events:
        ages = events[event]['ages']
        for age in ages:
            ages_set.add(age)
    ages_set = list(ages_set)
    int_ages = [int(i) for i in ages_set ]
    return sorted(int_ages)

def make_events_age_csv(csv_file_name, json_file_name):
    events = read_json(json_file_name)
    header = ['Event']
    ages = get_age_set(events)
    header.extend( [str(i)+' years old' for i in ages])
    #print(header)
    with open(csv_file_name, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        for event in events:
            row = []
            row.append(event)
            for age in ages:
                if(str(age) not in events[event]['ages']):
                    row.append(0)
                else:
                    row.append(events[event]['ages'][str(age)])
            csv_writer.writerow(row)

def make_events_gender_csv(csv_file_name, json_file_name):
    events = read_json(json_file_name)
    header = ['Event']
    events_ = {}
    genders = ['M', 'F']
    header.extend(genders)
    #print(header)
    with open(csv_file_name, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        for event in events:
            row = []
            row.append(event)
            for gender in genders:
                if(gender not in events[event]['genders']):
                    row.append(0)
                else:
                    row.append(events[event]['genders'][gender])
            csv_writer.writerow(row)


def main():
    json_file_name = 'events.json'
    pepare_filtered_events(json_file_name)
    csv_file_name = 'events_age.csv'
    make_events_age_csv(csv_file_name, json_file_name)
    csv_file_name = 'events_gender.csv'
    make_events_gender_csv(csv_file_name, json_file_name)
    
    pass


if __name__ == '__main__':
    main()