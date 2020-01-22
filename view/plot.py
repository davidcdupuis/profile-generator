"""Plot functions for the profile"""

import base64
from io import BytesIO
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def plot_ltv_app_country(app, country, df):
    """A function to plot ltv for an app and a specific country
    Args:
        app : Application
            The application we want to analyze

        country : Country
            The country in which the campaign was run

        df : Dataframe
            The dataframe containg the data we want to use

    Return:
        out: ?
    """
    fig, axes = plt.subplots(2,1,constrained_layout=True,sharex=True,sharey=True)
    fig.suptitle('LTVD2 over Time for ({0}|{1})'.format(app,country),fontsize=14)

    platforms = ['android','ios']
    net = ['Applovin','ironSource','Organic']

    for i in range(len(platforms)):
        axes[i].set_title(platforms[i])
        axes[i].set_ylabel('ltv (¢)')
        AL_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].date.astype('O')
        AL_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].ltv

        IS_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].date.astype('O')
        IS_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].ltv

        OG_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].date.astype('O')
        OG_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].ltv

        axes[i].set_title(platforms[i])
        axes[i].plot(AL_x,AL_y,color='b')
        axes[i].plot(IS_x,IS_y,color='orange')
        axes[i].plot(OG_x,OG_y,color='g')
        axes[i].legend(net)
    return

def my_plotter(ax, data1, data2, title='', param_dict={}):
    """A helper function to make a graph
    Args:
        ax : Axes
            The axes to draw to

        data1 : array
            The x data

        data2 : array
            The y data

        param_dict : dict
            Dictionary of kwargs to pass to ax.plot

    Return:
        out : list
            list of artists added
    """
    ax.set_title(title)
    out = ax.plot(data1, data2, **param_dict)
    return out

def plot_ltv_app_country(app, country, df):
    """A function to plot ltv for an app and a specific country
    Args:
        app : Application
            The application we want to analyze

        country : Country
            The country in which the campaign was run

        df : Dataframe
            The dataframe containg the data we want to use

    Return:
        out: ?
    """
    fig, axes = plt.subplots(2,1,constrained_layout=True,sharex=True,sharey=True)
    fig.suptitle('LTVD2 over Time for ({0}|{1})'.format(app,country),fontsize=14)

    platforms = ['android','ios']
    net = ['Applovin','ironSource','Organic']

    for i in range(len(platforms)):
        axes[i].set_title(platforms[i])
        axes[i].set_ylabel('ltv (¢)')
        AL_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].date.astype('O')
        AL_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].ltv

        IS_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].date.astype('O')
        IS_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].ltv

        OG_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].date.astype('O')
        OG_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].ltv

        axes[i].set_title(platforms[i])
        axes[i].plot(AL_x,AL_y,color='b')
        axes[i].plot(IS_x,IS_y,color='orange')
        axes[i].plot(OG_x,OG_y,color='g')
        axes[i].legend(net)
    plt.close()
    return fig

def plot_installs_app_country(app, country, df):
    """Function to plots installs over time"""
    fig, axes = plt.subplots(2,1,constrained_layout=True,sharex=True,sharey=True)
    fig.suptitle('Installs over Time for ({0}|{1})'.format(app,country),fontsize=14)

    platforms = ['android','ios']
    net = ['Applovin','ironSource','Organic']

    for i in range(len(platforms)):
        axes[i].set_title(platforms[i])
        axes[i].set_ylabel('installs')
        AL_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].date.astype('O')
        AL_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].installs

        IS_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].date.astype('O')
        IS_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].installs

        OG_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].date.astype('O')
        OG_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].installs

        axes[i].set_title(platforms[i])
        axes[i].plot(AL_x,AL_y,color='b')
        axes[i].plot(IS_x,IS_y,color='orange')
        axes[i].plot(OG_x,OG_y,color='g')
        axes[i].legend(net)
    plt.close()
    return fig

def plot_cumulRev_app_country(app, country, df):
    """"""
    fig, axes = plt.subplots(2,1,constrained_layout=True,sharex=True,sharey=True)
    fig.suptitle('Cumulated Revenue over Time for ({0}|{1})'.format(app,country),fontsize=14)

    platforms = ['android','ios']
    net = ['Applovin','ironSource','Organic']

    for i in range(len(platforms)):
        axes[i].set_title(platforms[i])
        axes[i].set_ylabel('cumul_revenue')
        AL_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].date.astype('O')
        AL_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[0])&(df['platform']==platforms[i])].cumul_revenue

        IS_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].date.astype('O')
        IS_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[1])&(df['platform']==platforms[i])].cumul_revenue

        OG_x = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].date.astype('O')
        OG_y = df[(df['country']==country)&(df['bundle_id']==app)&(df['ad_network_name']==net[2])&(df['platform']==platforms[i])].cumul_revenue

        axes[i].set_title(platforms[i])
        axes[i].plot(AL_x,AL_y,color='b')
        axes[i].plot(IS_x,IS_y,color='orange')
        axes[i].plot(OG_x,OG_y,color='g')
        axes[i].legend(net)
    plt.close()
    return fig

def plot_to_str(plt):
    """Convert matplotlib plot to base64 encoded string
    Args:
        plt: matplotlib plot
    Return:
        figdata_png: base64 encoded png string
    """
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0) # rewind to beginning of file
    figdata_png = base64.b64encode(figfile.getvalue()).decode('utf8')
    return figdata_png
