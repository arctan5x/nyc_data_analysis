import pandas as pd
import time
import ujson
import datetime
import threading

CHUNKSIZE = 10 ** 8
MORNING_TIME_START = datetime.datetime.strptime('2018-01-01 00:06:00', '%Y-%m-%d %H:%M:%S').time()
MORNING_TIME_END = datetime.datetime.strptime('2018-01-01 00:11:00', '%Y-%m-%d %H:%M:%S').time()
EVENING_TIME_START = datetime.datetime.strptime('2018-01-01 00:15:00', '%Y-%m-%d %H:%M:%S').time()
EVENING_TIME_END = datetime.datetime.strptime('2018-01-01 00:20:00', '%Y-%m-%d %H:%M:%S').time()

def get_file_list():
    # Get a local path of csv files
    file = open("data_urls.txt", "r") 
    file_list = [line[8:].strip() for line in file.readlines() if 'yellow' in line]
    file.close()
    print "Found {} csv files".format(len(file_list))
    return file_list

def write_data_as_json(data):
    file = open("pickup_dropoff_data.json", "w")
    file.write(ujson.dumps(data))
    file.close()

def determine_time_frame(time):
    # Time format looks like 2018-01-01 00:10:37
    converted_time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').time()
    if MORNING_TIME_START < converted_time and converted_time < MORNING_TIME_END:
        return 'morning'
    elif EVENING_TIME_START < converted_time and converted_time < EVENING_TIME_END:
        return 'evening'
    return 'outofrange'

def process_csv_files(file_list):
    '''
    Separate data into two time frames: morning and afternoon.
    Morning time frame is from 6am - 11am in local NYC time.
    Afternoon time frame is from 3pm - 8pm in local NYC time.
    I intend to separate two traffic heavy hours to analyze the data differently.
    We determine the time by the pickup time.
    '''
    start_time = time.time()

    data = {}
    data['morning'] = {'dropoff': {}, 'pickup': {}}
    data['evening'] = {'dropoff': {}, 'pickup': {}}

    for csv_file in file_list:
        csv_process_start = time.time()
        csv_filename = csv_file[csv_file.rfind('/')+1:]
        print "Processing {}".format(csv_filename)
        for chunk in pd.read_csv(csv_file, chunksize=CHUNKSIZE):
            print len(chunk)
            for i, row in chunk.iterrows():
                try:
                    pickup_time = row['tpep_pickup_datetime']
                except:
                    pickup_time = row['lpep_pickup_datetime']
                time_frame = determine_time_frame(pickup_time)
                if time_frame == 'outofrange':
                    continue
                else:
                    pickup_location_ID = row['PULocationID']
                    dropoff_location_ID = row['DOLocationID']
                    if pickup_location_ID in data[time_frame]['pickup']:
                        data[time_frame]['pickup'][pickup_location_ID] += int(row['passenger_count'])
                    else:
                        data[time_frame]['pickup'][pickup_location_ID] = int(row['passenger_count'])
                    if dropoff_location_ID in data[time_frame]['dropoff']:
                        data[time_frame]['dropoff'][dropoff_location_ID] += int(row['passenger_count'])
                    else:
                        data[time_frame]['dropoff'][dropoff_location_ID] = int(row['passenger_count'])
                
        csv_process_elapsed_time = time.time() - csv_process_start
        print "Processed {csv_filename} in {csv_process_elapsed_time}".format(csv_filename=csv_filename, csv_process_elapsed_time=time.strftime("%H:%M:%S", time.gmtime(csv_process_elapsed_time)))

    elapsed_time = time.time() - start_time
    print 'Time spent processing {num_files} files: {elapsed_time}'.format(num_files=len(file_list), elapsed_time=time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))
    return data

if __name__ == "__main__":
    file_list = get_file_list()
    pickup_dropoff_data = process_csv_files(file_list)
    write_data_as_json(pickup_dropoff_data)


