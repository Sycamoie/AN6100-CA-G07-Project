# -*- coding: utf-8 -*-

# Description
# This is part of 20S1 AN6100 group project 01

import os
import numpy as np
import pandas as pd
from datetime import datetime


# This file is used for the merge functionality of the application
# To use the functions, import and call the merge_file() function
# the parameters are the path of the directory storing the in and out
# csv file and the name for the csv output file

# data storage dir
in_dir = './INOUT'
# output file
out_file = './merged_output.csv'

# Sort the in files and the out files inside the directory,
# returns a tuple of the list of in_file and out_file
def in_out_sort():
    in_file = []
    out_file = []
    for file in os.listdir(in_dir):
        if file[0:2] == 'IN':
            in_file.append(f"{in_dir}/{file}")
        elif file[0:2] == 'OT':
            out_file.append(f"{in_dir}/{file}")
    return in_file, out_file


# transform both the in file and out file into a dataframe,
# append them to a list
def construct_dataframe():
    # assuming the file is inside the directory
    in_file, out_file = in_out_sort()
    df_in_list = [pd.read_csv(file) for file in in_file]
    df_out_list = [pd.read_csv(file) for file in out_file]
    return df_in_list, df_out_list


# perform a concatenation and merge between two list of dfs
def concat_n_merge(df_in_list, df_out_list, key):
    # concatenate the list of dataframes into a single dataframe for both in and out
    df_in = pd.concat(df_in_list, axis=0)
    df_out = pd.concat(df_out_list, axis=0)
    # merge the two dataframes into a single dataframe
    df_merge = pd.merge(df_in, df_out, left_on=key, right_on=key)
    return df_merge


# transformed the column into a datetime Series based on the format specified
def get_datetime_series(dataframe, column, _format):
    if _format.upper() == 'YMD':
        dt_series = dataframe[column].map(
            lambda x: datetime.strptime(x, '%Y-%m-%d'))
    elif _format.upper() == 'HM':
        dt_series = dataframe[column].map(
            lambda x: datetime.strptime(x, '%H:%M'))
    else:
        return None
    return dt_series


# get a list of datetime Series from a a column dictionary
# with kv-pair being column name and formats
def get_datetime_list(dataframe, column_dict):
    dt_list = [get_datetime_series(dataframe, col_name, _format)
               for col_name, _format in column_dict.items()]
    return dt_list


# transform two datetime theories, dts1 in YMD format, dts2 in
# HM format into a single datetime series in DTMHM format
def combineDtSeries(dt_series1, dt_series2):
    dt_series = pd.Series(np.zeros(len(dt_series1)))

    for i in range(len(dt_series1)):
        dt_series[i] = datetime.combine(datetime.date(dt_series1[i]), datetime.time(dt_series2[i]))

    return dt_series


def get_total_durmins(dtlist):
    dt_in = combineDtSeries(dtlist[0], dtlist[1])
    dt_out = combineDtSeries(dtlist[2], dtlist[3])
    dt_dur = dt_out-dt_in
    # get the total timedelta, and transform the result into a series a minutes
    total_dur_mins = dt_dur.map(lambda x: x.days*24*60+x.seconds//60)
    return total_dur_mins


# used to output a merge file in csv format
# into the root folder as merged_output.csv
def merge_file():
    try:
        columns_dictionary = {'Date_x': 'YMD', 'TimeIn': 'HM', 'Date_y': 'YMD', 'TimeOut': 'HM'}

        # construct the dataframe list and unpack the in df and out df
        df_in_list, df_out_list = construct_dataframe()
        # merge the two dfs into a single df using NRIC number
        df_merge = concat_n_merge(df_in_list, df_out_list, 'NRIC')

        # data manipulation on arrival and leave date, get a list of datetime objects
        dt_list = get_datetime_list(df_merge, columns_dictionary)

        # get a Series of duration in minutes
        total_dur = get_total_durmins(dt_list)
        # add the series to the dataframe
        df_merge['StayMinsDuration'] = total_dur

        # drop the NRIC and Date_y column
        del df_merge["NRIC"]
        del df_merge['Date_y']

        # rename the columns
        df_merge.rename(columns={'Date_x': 'Date', 'TimeIn': 'InTime', 'GateIn': 'InGate',
                                 'PCIn': 'InPC', 'GateOut': 'OutGate', 'TimeOut': 'OutTime',
                                 'PCOut': 'OutPC'}, inplace=True)

        # reindex the columns to in the same order as the example
        df_merge = df_merge.reindex(columns=['Date', 'InTime', 'InGate', 'InPC', 'ContactNo',
                                             'OutGate', 'OutTime', 'OutPC', 'StayMinsDuration'])

        # Filtering out negative durations(person might enter multiple times)
        df_merge = df_merge[df_merge['StayMinsDuration'] > 0]

        # writing to csv file
        df_merge.to_csv(out_file, index=False)

        # return the dataframe
        # return df_merge

    # print out the exception
    except Exception as ex:
        print(f'caused by {ex}\nProgram Terminated')
