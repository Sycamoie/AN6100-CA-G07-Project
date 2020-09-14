import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# This module is used for the merge functionality of the application
# To use the module, import the module into the main function and call the
# merge_file() function,the parameters are the path of the directory storing the in and out
# csv file and the name for the csv output file

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
        df_list.append(cleaned_data(pd.read_csv(file)))
    return df_list


# tansform both the in file and out file into a dataframe,
# append them to a list
def construct_dataframe(path):
    # assuming the file is inside the directory
    in_file, out_file = in_out_sort(path)
    # change the working directory to 'INNOT
    os.chdir(path)
    df_in_list = get_dataframe_list(in_file)
    df_out_list = get_dataframe_list(out_file)
    return df_in_list, df_out_list


# performa concatenation and merge between two list of dfs
def concat_n_merge(df_in_list, df_out_list, key):
    # concatenate the list of dataframes into a single dataframe for both in and out
    df_in = pd.concat(df_in_list, axis=0)
    df_out = pd.concat(df_out_list, axis=0)
    # merge the two dataframes into a single dataframe
    df_merge = pd.merge(df_in, df_out, left_on=key, right_on=key)
    return df_merge


# transformed the column into a datetime Series based on the format sepcified
def get_dateime_series(dataframe, column, format):
    if format.upper() == 'YMD':
        dtSeries = dataframe[column].map(
            lambda x: datetime.strptime(str(x), '%Y-%m-%d'))
    elif format.upper() == 'HM':
        dtSeries = dataframe[column].map(
            lambda x: datetime.strptime(str(x), '%H:%M'))
    return dtSeries


# get a list of datetime Series from a a column dictionary
# with kv-pair being column name and formats
def get_datetime_list(dataframe, columndict):
    dt_list = []
    for colname, format in columndict.items():
        dt_list.append(get_dateime_series(dataframe, colname, format))
    return dt_list

# used to clean missing values, drop rows containing Nans


def cleaned_data(dataframe):
    cleaned = dataframe.dropna()
    return cleaned


# get the stay duration in minutes


def get_total_durmins(dtlist):
    dur_day = dtlist[2]-dtlist[0]
    dur_hour = dtlist[3]-dtlist[1]
    # get the total timedelta, and transform the result into a series a minutes
    total_dur = dur_day+dur_hour
    total_dur = total_dur.map(lambda x: x.seconds//60)
    return total_dur


# used to output a merge file in csv format, must specify the path and also
# the name of the file to be outputed
def merge_file(pathname, newfilename):
    columnsdictionary = {'Date_x': 'YMD',
                         'TimeIn': 'HM', 'Date_y': 'YMD', 'TimeOut': 'HM'}
    # construct the dataframe list and unpack the in df and out df
    df_in_list, df_out_list = construct_dataframe(pathname)
    # merge the two dfs into a single df using NRIC number
    df_merge = concat_n_merge(df_in_list, df_out_list, 'NRIC')
    df_merge = cleaned_data(df_merge)
    # data manipulation on arrival and leave date, get a
    # list of datetime objects
    dt_list = get_datetime_list(df_merge, columnsdictionary)
    # get a Series of duration in minutes
    total_dur = get_total_durmins(dt_list)
    # add the series to the dataframe
    df_merge['StayMinsDuration'] = total_dur
    # drop the NRIC and Date_y column
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
    df_merge.to_csv(newfilename, index=False)
    return df_merge


print(merge_file('/Users/linghao/Desktop/6100_project/INOUT', 'merged10.csv'))
