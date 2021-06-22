import os
import time
import numpy as np
import pandas as pd
from zipfile import ZipFile

# --------------------------------------------------------------------

start_time = time.time()

# --------------------------------------------------------------------
print("\n")
print("Enter the date for the GTFS you are working on.\n")

# get date for feed under construction
date_for_feed = str(input("Use the following format (YYYYMMDD): "))

# set workspace
path_to_gtfs_workspace = r'C:\Users\miguelf.PARTNC\OneDrive - Piedmont Authority Regional Transportation\Desktop\GTFS Workspace'
path_to_folder = path_to_gtfs_workspace + "\PART_" + date_for_feed

# change working directory
os.chdir(path_to_folder)

# --------------------------------------------------------------------

# set variable for zipped gtfs feed
gtfs_zip = "gtfs.zip"

# read in zipped gtfs feed
files = ZipFile(gtfs_zip)

# create dataframes from text files
trips = pd.read_csv(files.open("trips.txt"), sep=',')
stop_times = pd.read_csv(files.open("stop_times.txt"), sep=',')
stops = pd.read_csv(files.open("stops.txt"), sep=',')

# --------------------------------------------------------------------

# sort stop_times by trip_id
stop_times.sort_values(by=['trip_id', 'stop_sequence'], inplace=True)

# create lists for values from stop_times.txt
trip_ids = stop_times['trip_id']
stop_ids = stop_times['stop_id']
stop_sequences = stop_times['stop_sequence']
departure_times = stop_times['departure_time']
time_points = stop_times['timepoint']

# create dataframe from lists
apc_working = pd.DataFrame(list(zip(trip_ids, stop_ids, stop_sequences, departure_times, time_points)),
                           columns=['trip_id', 'stop_id', 'stop_sequence', 'departure_time', 'timepoint'])

# merge data from stops.txt
apc_working = apc_working.merge(
    stops[['stop_id', 'stop_code', 'stop_name', 'stop_lat', 'stop_lon']], how='left', on='stop_id'
)

# merge data from trips.txt
apc_working = apc_working.merge(
    trips[['trip_id', 'route_id', 'direction_id', 'block_id', 'service_id', 'shape_id']], how='left', on='trip_id'
)

# create NODE_ID column and fill it with stop_name if it is a time point
apc_working['NODE_ID'] = np.where(apc_working['timepoint'] == 1, apc_working['stop_name'], "")

# remove whitespace, parentheses, hyphens, and truncate the stop name
apc_working['NODE_ID'] = apc_working['NODE_ID'].str.replace(" ", "")
apc_working['NODE_ID'] = apc_working['NODE_ID'].str.replace("-", "")
apc_working['NODE_ID'] = apc_working['NODE_ID'].replace('\(|\)', '', regex=True)
apc_working['NODE_ID'] = apc_working['NODE_ID'].str[:18]

# remove nan values from departure time column
apc_working['departure_time'].replace(np.nan, "", regex=True, inplace=True)

# --------------------------------------------------------------------

# create final dataframe and reorder columns
apc_final = apc_working[[
    'trip_id', 'route_id', 'stop_id', 'stop_code', 'stop_name', 'stop_sequence', 'stop_lat', 'stop_lon',
    'direction_id', 'block_id', 'departure_time', 'service_id', 'shape_id', 'timepoint', 'NODE_ID'
]]

# --------------------------------------------------------------------

# set file name prefix
prefix = "testing_PART_reference_"

# write final dataframe to excel
apc_final.to_excel(excel_writer=prefix + date_for_feed + ".xlsx", sheet_name='Final', index=False)

print("\nAPC reference file successfully created from GTFS...")
print("--- %s seconds ---" % (time.time() - start_time))
