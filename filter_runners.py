import json
from zipfile import ZipFile
from zipfile import ZIP_DEFLATED
from os import listdir
import os.path
import csv

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

def read_json(json_file_name):
    with open(json_file_name, 'r') as file:
        data = json.load(file)
        return data

def read_event(json_file_name, runners):
    event = read_json(json_file_name)
    event_name = event['eventName']
    print(event_name)
    for runner in event['items']:
        #print(runner)
        full_name = f'{runner["firstName"]} {runner["lastName"]}'.strip()
        #print(full_name)
        #global runners
        if full_name not in runners:
            runners[full_name] = []
        runners[full_name].append(event_name)

def read_events(list_files):
    runners = {}
    for event in list_files:
        read_event(event, runners)
    return runners

def filter_runners(runners):
    #global runners
    filtered_runners = {};
    for full_name in runners:
        events = runners[full_name]
        if(len(events)>=5):
            filtered_runners[full_name] = events
    return filtered_runners

def pepare_filtered_runners(json_file_name):
    clear_temp()
    extract_input_to_temp()
    list_files = get_list_files()
    runners = read_events(list_files)
    filtered_runners = filter_runners(runners)
    write_json(json_file_name, filtered_runners)
    
def make_filtered_runners_csv(csv_file_name, json_file_name):
    runners = read_json(json_file_name)
    len_events = 5
    header = ['Full name']
    header.extend( ['Event' for i in range(len_events)])
    with open(csv_file_name, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)

        for runner in runners:
            full_name = runner
            if full_name == 'Anonymous':
                continue
            events = runners[full_name]
            row = []
            row.append(full_name)
            len_e = len_events
            #if len(events) < len_events:
            #    len_e = len(events)
            len_e = len(events)
            for i in range(len_e):
                row.append(events[i])
            csv_writer.writerow(row)

def make_popular_events_csv(csv_file_name, json_file_name):
    runners = read_json(json_file_name)
    header = ['Event']
    events = {}
    for runner in runners:
        full_name = runner
        events_ = runners[full_name]
        for event in events_:
            if event not in events:
                events[event] = 0
            events[event] += 1
    # events table        
    header = ['Event', 'Active participants']
    with open(csv_file_name, 'w') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)
        for event in events:
            row = []
            row.append(event)
            row.append(events[event])
            csv_writer.writerow(row)




def main():
    json_file_name = 'filtered_runners.json'
    pepare_filtered_runners(json_file_name)
    csv_file_name = 'filtered_runners.csv'
    make_filtered_runners_csv(csv_file_name, json_file_name)
    csv_file_name = 'popular_filtered_events.csv'
    make_popular_events_csv(csv_file_name, json_file_name)
    
    pass


if __name__ == '__main__':
    main()