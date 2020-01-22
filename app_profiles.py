#!/usr/bin/env python3
# coding: utf-8

import constants as const
from constants import  jj_env
from proge import ProfileGenerator
from pprint import PrettyPrinter
import datetime
import re
import json
import pandas as pd
import argparse
import os
import pandas_profiling

''' APP FUNCTIONS '''
def get_apps_s3_json() -> dict:
    """Get apps from json stored on S3
    """
    apps = dict()
    try:
        obj = const.s3_resource.Object(const.DATA_BUCKET, 'apps/apps.json')
        apps = json.loads(obj.get()['Body'].read().decode('utf-8'))
    except Exception as e:
        print("Error fecthing apps/apps.json from {}: {}".format(const.DATA_BUCKET, e))
    return apps

def get_apps_s3_reports(networks) -> dict:
    """Function to get app dict data from s3
    Args:
        networks: list of networks we want to get apps from
            ['ironsource','mopub']
    Return:
        apps: dict of app data
    """
    apps = {}
    for network in networks:
        # change this path according to configuration
        path = 's3://hg-prod-nv-orion/refe/reports/20191013/{}/apps.csv.gz'.format(network)
        df = pd.read_csv(path,compression='gzip')
        for index, row in df.iterrows():
            tmp = row
            if(int(row['monetization_app_status']) == 1):
                if row['bundle_id'] not in apps:
                    apps[row['bundle_id']] = {'id':row['bundle_id'],
                                              'name':row['name'],
                                              'status':row['monetization_app_status'],
                                              'ad_networks':[],
                                              'monet_networks':[network],
                                              'platforms':[],
                                              'categories':[],
                                              'description':'',
                                              'campaigns':[]
                                              }
                    apps[row['bundle_id']]['platforms'].append(row['platform'])
                else:
                    if row['platform'] not in apps[row['bundle_id']]['platforms']:
                        apps[row['bundle_id']]['platforms'].append(row['platform'])
    return apps

def get_apps(networks, type='json') -> dict:
    """Get dictionary of apps
    """
    apps = dict()
    if type == 'json':
        apps = get_apps_s3_json()
    elif type == 'reports':
        apps = get_apps_s3_reports(networks)
    else:
        print("Input parameter 'type'={} not recognized".format(type))
    return apps

def app_directories(apps) -> None:
    """Function to create app directories if necessary for saving report data
    Args:
        apps: a list of apps we want to check directory existence
    """
    # check if directories exist for each app, if not create them
    for app in apps:
        p = const.LOCAL_DIR / app
        if not os.path.exists(p):
            os.mkdir(p)
            print("App folder in local path {} doesn't exist, creating new app folder".format(p))
    return

def save_apps_s3(apps, bucket):
    """Saves apps.json to s3 bucket
    Args:
        apps: dict containing app data
    """
    local_path = LOCAL_DIR
    s3_path = 'apps/apps.json'
    if local_path.exists():
        file = local_path / 'apps.json'
        with open(file, 'w') as f:
            json.dump(apps, f)
    try:
        s3_client.upload_file(str(file), bucket, s3_path)
    except Exception as err:
        print("Error uploading apps.json: ", err)
    return

def file_name(ext, app_id, xday, start_date, days=7) -> str:
    """Generate file name
    """
    start = start_date.strftime('%Y%m%d')
    end   = (start_date - datetime.timedelta(days=days-1)).strftime('%Y%m%d')
    # Generate name: '<bundle_id>-ltvd<xday>-<start_date (YYYYmmdd)>-<end_date (YYYYmmdd)>.csv'
    file_name = app_id.replace(".","_") + '-' + 'ltvd' + str(xday) + '-' + start + '-' + end + ext
    return file_name

def upload_to_s3(local_path, bucket_name, filename, public=False) -> None:
    """Helper function to upload a file from local to S3
    """
    s3_path = 'apps/' + app + '/' + filename
    try:
        bucket = s3_resource.Bucket(bucket_name)
        if public:
            bucket.upload_file(local_path, s3_path, ExtraArgs={'ACL':'public-read','ContentType':'text/html'})
        else:
            bucket.upload_file(local_path, s3_path, ExtraArgs={'ACL':'public-read','ContentType':'text/html'})
    except Exception as e:
        print("Error uploading: {} | ({})".format(s3_path,e))
    return

''' LTV FUNCTIONS '''
def generate_dates(curr_date, days=7):
    """Function to generate a series of dates compatible to s3 starting from today up to a given number of days
        Args:
            curr_date: the starting date
            days: number of days we want to go back

        Return:
            dates: a list of dates
    """
    dates = [curr_date.strftime('%Y%m%d')]
    for i in range(1,days):
        past_date = curr_date - datetime.timedelta(days=i)
        dates.append(past_date.strftime('%Y%m%d'))
    return dates

def get_xday_ltv(client, bucket, folder, xday=2):
    """Function to get the oldest ltv dataframe of a specific folder
        Args:
            client: s3 client
            bucket: name of bucket we want to use
            folder: path to folder we want to explore
            xday: ltv dX we want

        Return:
            recent_df: name of most recent dataframe for xday
    """
    results = client.list_objects(Bucket=bucket, Prefix=folder, Delimiter='/')
    xday_df = ''
    for result in results['Contents']:
        match = re.search(r'\bltvs-d([0123456789]+)\.csv\.gz', result['Key'])
        tmp = int(match[1])
        if tmp == xday:
            xday_df = result['Key']
        # print(match[0])
    return xday_df

def get_ltv_df(start_date, days=7):
    """Function to get a combine ltf df over several days
        Args:
            start_date: datetime.date of starting date
            days: number of days we want to go back (default: 7)

        Return:
            ltv_df: merged ltv dataframe for all dates
    """
    dates = generate_dates(start_date, days)
    file_paths = []
    for date in dates:
        for network in const.MONET_NETWORKS:
            path = const.PATH_REPORTS +'/'+ date + '/' + network + '/'
            file_path = 's3://' + const.ORION_BUCKET + '/' + get_xday_ltv(const.s3_client, const.ORION_BUCKET, path, xday=const.XDAY)
            file_paths.append(file_path)
            #print(file_path)

    # fetch ltv data to build dataframe
    ltv_df = pd.DataFrame()
    for file_path in file_paths:
        tmp_df = pd.read_csv(file_path, compression='gzip')
        tmp_df = tmp_df[tmp_df['xday']==2] # use configuration
        ltv_df = pd.concat([ltv_df,tmp_df],ignore_index=True)
    ltv_df['date'] = pd.to_datetime(ltv_df['date'])
    return ltv_df

''' OTHER FUNCTIONS '''
def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    pp = PrettyPrinter()

    # -------------------------------------------------------------------------
    # Set up argument parser.
    # Arguments allow user modification of what needs to be run without
    # altering configuration file, useful for testing
    # -------------------------------------------------------------------------
    parser = argparse.ArgumentParser(
        prog="python3",
        formatter_class=argparse.RawTextHelpFormatter,
        description='Profile Generator'
    )

    # default values are specified in the configuration file
    '''
    parser.add_argument(
        "-df", "--save_df",
        type=str2bool,
        help="Save app df locally (config={})".format(const.config['save_app_df'])
    )
    '''
