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


def construct_dataframe(path):
    # assuming the file is inside the directory
    in_file, out_file = in_out_sort(path)
    # change the working directory to 'INNOT
    os.chdir(path)
    df_list = []
    # tansform both the in file and out file into a dataframe, append them to a list
    df_list.append(get_dataframe_list(in_file))
    df_list.append(get_dataframe_list(out_file))
    return df_list


def concat_n_merge(df_in_list, df_out_list):
    # concatenate the list of dataframes into a single dataframe for both in and out
    df_in = pd.concat(df_in_list, axis=0)
    df_out = pd.concat(df_out_list, axis=0)
    # merge the two dataframes into a single dataframe
    df_merge = pd.merge(df_in, df_out, left_on='NRIC', right_on='NRIC')
    return df_merge


def get_datetime_list(dataframe, columndict):
    dt_list = []
    # get datetime object for both time columns
    for colname, format in columndict.items():
        dt_list.append(get_dateime_object(dataframe, colname, format))
    return dt_list


def get_total_durmins(dtlist):
    dur_day = dtlist[2]-dtlist[0]
    dur_hour = dtlist[3]-dtlist[1]
    # get the total timedelta, and transform the result into a series a minutes
    total_dur = dur_day+dur_hour
    total_dur = total_dur.map(lambda x: x.seconds//60)
    return total_dur


def merge_file(pathname, newfilename):
    columnsdictionary = {'Date_x': 'YMD',
                         'TimeIn': 'HM', 'Date_y': 'YMD', 'TimeOut': 'HM'}
    df_list = construct_dataframe(pathname)
    df_in_list = df_list[0]
    df_out_list = df_list[1]
    df_merge = concat_n_merge(df_in_list, df_out_list)
    dt_list = get_datetime_list(df_merge, columnsdictionary)
    total_dur = get_total_durmins(dt_list)
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
    df_merge.to_csv(newfilename, index=False)
