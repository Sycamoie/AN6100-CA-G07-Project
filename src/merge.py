import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# Sort the in files and the out files inside the directory,
# returns a tuple of the list of in_file and out_file
def in_out_sort(path):
    in_file = []
    out_file = []
    for dirpath, dirname, filename in os.walk(path):
        for file in filename:
            if file[0:2] == 'IN':
                in_file.append(file)
            elif file[0:2] == 'OT':
                out_file.append(file)
        return in_file, out_file


# trasnform the files inside the list into a list of dataframe
def get_dataframe_list(filenamelist):
    df_list = []
    for file in filenamelist:
        df_list.append(pd.read_csv(file))
    return df_list


# transformed the column into a datetime object based on the format sepcified
def get_dateime_object(dataframe, column, format):
    if format.upper() == 'YMD':
        dtSeries = dataframe[column].map(
            lambda x: datetime.strptime(x, '%Y-%m-%d'))
    elif format.upper() == 'HM':
        dtSeries = dataframe[column].map(
            lambda x: datetime.strptime(x, '%H:%M'))
    return dtSeries


def get_duration(dtSeries1, dtSeries2):
    return dtSeries2-dtSeries1


# procedure to merge the data
# assuming the file is inside the directory
in_file, out_file = in_out_sort('INOUT')

# change the working directory to 'INNOT
os.chdir('INOUT')

# tansform both the in file and out file into a dataframe, append them to a list
df_in_list = get_dataframe_list(in_file)
df_out_list = get_dataframe_list(out_file)

# concatenate the list of dataframes into a single dataframe for both in and out
df_in = pd.concat(df_in_list, axis=0)
df_out = pd.concat(df_out_list, axis=0)

# merge the two dataframes into a single dataframe
df_merge = pd.merge(df_in, df_out, left_on='NRIC', right_on='NRIC')

# get datetime object for both time columns
dt1 = get_dateime_object(df_merge, 'Date_x', 'YMD')
dt2 = get_dateime_object(df_merge, 'TimeIn', 'HM')
dt3 = get_dateime_object(df_merge, 'Date_y', 'YMD')
dt4 = get_dateime_object(df_merge, 'TimeOut', 'HM')

# get time deltas
dur_day = get_duration(dt1, dt4)
dur_hour = get_duration(dt2, dt3)

# get the total timedelta, and transform the result into a series a minutes
total_dur = dur_day+dur_hour
total_dur = total_dur.map(lambda x: x.seconds//60)

# add the series to the dataframe
df_merge['StayMinsDuration'] = total_dur

# drop the NRIC colum
del df_merge["NRIC"]
del df_merge['Date_y']

# rename the columns
df_merge.rename(columns={'Date_x': 'Date', 'TimeIn': 'In Time', 'GateIn': 'In Gate',
                         'PCIn': 'In PC', 'GateOut': 'OutGate', 'TimeOut': 'Out Time',
                         'PCOut': 'Out PC'}, inplace=True)

# reindex the columns to in the same order as the example
df_merge = df_merge.reindex(columns=['Date', 'In Time', 'In Gate', 'In PC', 'ContactNo',
                                     'Out Time', 'Out PC', 'StayMinsDuration'])

# output the result into a csv file
df_merge.to_csv('merged_output.csv')
