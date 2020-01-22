#!/usr/bin/env python3
# coding: utf-8

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pprint
import re
import datetime
import os
from IPython.core.display import display, HTML
from pathlib import Path
from io import BytesIO
import base64
from view.plot import plot_ltv_app_country, my_plotter, plot_ltv_app_country, plot_installs_app_country, plot_cumulRev_app_country, plot_to_str
import jinja2 as jj
import constants as const

class ProfileGenerator():
    """Generate a profile report from a Dataset stored as a pandas `DataFrame`.
    """

    def __init__(self, df, apps, today, type='app', mode='business'):
        """
        """
        self.today   = today
        self.apps    = apps
        self.app_df  = df
        self.type    = type
        self.mode    = mode
        self.html    = None
        # self.profile = None

        if mode == 'business':
            if self.type == 'app':
                self.check_dataframe()
                self.app_id = self.app_df['bundle_id'].unique()[0]
            else:
                print("no other types implemented yet!")
        elif mode == 'tech':
            self.html = self.app_df.profile_report(title='Tech Profiling Report').to_html()

    def app_description(self):
        """Function to generate HTML formatted string of app description
        Args:
           app_id: bundle_id of application we want to describe
           apps: dictionary containing app information

        Return:
            desc: HTML formatted app description
        """
        app_desc = {'id':self.app_id,
                    'title':self.app_df[self.app_id]['name'],
                    'monet_network':self.app_df[self.app_id]['network'],
                    'platforms':self.app_df[self.app_id]['platforms']
                   }
        # APP ID | APP NAME | APP MONET NETWORK | APP PLATFORMS
        return env.get_template('app_description.html').render(app_desc)

    def top_countries(self, top):
        """Function to get top countries in df
        Args:
            df: dataframe
            app_id: bundle_id of app
            top: number of top value to get

        Return:
            lst: list of top countries in descending order
        """
        # return self.app_df[self.app_df['bundle_id']==self.app_id]['country'].value_counts()[:top]
        return self.app_df.groupby(['country']).sum()['installs'].sort_values(ascending=False)[:top]

    def app_proge(self):
        """Generate business profile for a specific application
        """
        file_loader = jj.FileSystemLoader('view/templates')
        env = jj.Environment(lstrip_blocks=True,trim_blocks=True,loader=file_loader)
        template = env.get_template('app_profile.html')

        tmp_df = self.app_df.groupby(['platform','bundle_id','country','ad_network_name','date']).sum()
        tmp_df['ltv'] = tmp_df['cumul_revenue'] / tmp_df['installs'] * 100
        tmp_df = tmp_df.reset_index()

        date_range = self.today.strftime('%d-%m-%Y') + '_' + (self.today - datetime.timedelta(days=5)).strftime('%d-%m-%Y')
        rows,columns = tmp_df.shape
        df_data = {'date_range':date_range,
                   'xday':2,
                   'rows':rows,
                   'columns':columns}

        countries = self.top_countries(5) # get top countries based on installs
        countries_data = []
        for item in countries.iteritems():
            country = item[0]
            ltvIMG = ''
            installsIMG = ''
            cumulRevIMG = ''
            # LTV
            fig1 = plot_ltv_app_country(self.app_id,country,tmp_df)
            ltvIMG = plot_to_str(fig1)
            # INSTALLS
            fig2 = plot_installs_app_country(self.app_id,country,tmp_df)
            installsIMG = plot_to_str(fig2)
            # CUMUL_REV
            fig3 = plot_cumulRev_app_country(self.app_id,country,tmp_df)
            cumulRevIMG = plot_to_str(fig3)
            country_data = {'name': const.COUNTRIES[country],
                            'id':country,
                            'ltvTimeImg':ltvIMG,
                            'installsTimeImg':installsIMG,
                            'cumulRevTimeImg':cumulRevIMG}
            countries_data.append(country_data)
            fig1.clf()
            fig2.clf()
            fig3.clf()

        self.html = template.render(title='Business Profile', app=self.apps[self.app_id], df=df_data, countries=countries_data)

    def check_dataframe(self) -> None:
        """Check if dataframe has appropriate column names and values for
        profile
        * Column names must be:
            ['platform','bundle_id','country','ad_network_name','date',
            'ltv','cumul_revenue','installs']
        * df['bundle_id'] must have a single value

        """
        if self.type == 'app':
            app_cols = ['platform','bundle_id','country','ad_network_name','date',
            'ltv','cumul_revenue','installs']
            # check column names
            error = False
            for col in app_cols:
                if col not in self.app_df.columns:
                    error = True
                    print("Column name {} not found in dataframe!".format(col))
            if error:
                exit(1)

            if len(self.app_df['bundle_id'].unique()) != 1:
                print("App ID must be unique, found {}".format(self.app_df['bundle_id'].unique()))
                exit(1)
        return

    def to_file(self, output_file: Path or str, silent: bool = True) -> None:
        """Write the report to a file.
        By default a name is generated.
        Args:
            output_file: The name or the path of the file to generate including the extension (.html).
            silent: if False, opens the file in the default browser
        """
        if type(output_file) == str:
            output_file = Path(output_file)

        with output_file.open("w", encoding="utf8") as f:
            wrapped_html = self.html
            f.write(wrapped_html)

        if not silent:
            import webbrowser

            webbrowser.open_new_tab(output_file)

    def to_html(self):
        """"""
        return template.render(title='Business Profile',
                               app=self.apps[self.app_id],
                               df=df_data,
                               countries=countries_data)
