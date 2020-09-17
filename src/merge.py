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
    return [pd.read_csv(file) for file in filenamelist]


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
            lambda x: datetime.strptime(x, '%Y-%m-%d'))
    elif format.upper() == 'HM':
        dtSeries = dataframe[column].map(
            lambda x: datetime.strptime(x, '%H:%M'))
    return dtSeries


# get a list of datetime Series from a a column dictionary
# with kv-pair being column name and formats
def get_datetime_list(dataframe, columndict):
    dt_list = [get_dateime_series(dataframe, colname, format)
               for colname, format in columndict.items()]
    return dt_list

# transform two datetime theories, dts1 in YMD format, dts2 in
# HM format into a single datatime series in DTMHM format


def combinedtseries(dtseries1, dtseries2):
    cdtseries = pd.Series(np.zeros(len(dtseries1)))
    for i in range(len(dtseries1)):
        cdtseries[i] = datetime.combine(datetime.date(
            dtseries1[i]), datetime.time(dtseries2[i]))
    return cdtseries


def get_total_durmins(dtlist):
    dt_in = combinedtseries(dtlist[0], dtlist[1])
    dt_out = combinedtseries(dtlist[2], dtlist[3])
    dt_dur = dt_out-dt_in
    # get the total timedelta, and transform the result into a series a minutes
    total_dur_mins = dt_dur.map(lambda x: x.days*24*60+x.seconds//60)
    return total_dur_mins


# used to output a merge file in csv format, must specify the path and also
# the name of the file to be outputed
def merge_file(pathname, pathsaved, filename):
    try:
        columnsdictionary = {'Date_x': 'YMD',
                             'TimeIn': 'HM', 'Date_y': 'YMD', 'TimeOut': 'HM'}
    # construct the dataframe list and unpack the in df and out df
        df_in_list, df_out_list = construct_dataframe(pathname)
    # merge the two dfs into a single df using NRIC number
        df_merge = concat_n_merge(df_in_list, df_out_list, 'NRIC')
    # df_merge = cleaned_data(df_merge)
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
        return df_merge
    # rename the columns
        df_merge.rename(columns={'Date_x': 'Date', 'TimeIn': 'In Time', 'GateIn': 'In Gate',
                                 'PCIn': 'In PC', 'GateOut': 'OutGate', 'TimeOut': 'Out Time',
                                 'PCOut': 'Out PC'}, inplace=True)
    # reindex the columns to in the same order as the example
        df_merge = df_merge.reindex(columns=['Date', 'In Time', 'In Gate', 'In PC', 'ContactNo',
                                             'Out Time', 'Out PC', 'StayMinsDuration'])
    # Filtering out negative durations(person might enter multiple times)
        df_merge = df_merge[df_merge['StayMinsDuration'] > 0]
        os.chdir(pathsaved)
        df_merge.to_csv(filename, index=False)
    except ValueError:
        print('Please Enter a Valid Path. Program Terminated')
    except BaseException as ex:
        print(f'{ex}')
        print("Program Terminated")


print(merge_file('/Users/linghao/Desktop/6100_project/INOUT',
                 '/Users/linghao/Desktop/6100_project/6100practice/AN6100-CA-G07-Project', 'merge.csv'))
print(os.getcwd())
