#!/usr/bin/env python3
# coding: utf-8

import yaml
from pathlib import Path
from beautifultable import BeautifulTable
import colorama
from colorama import Fore
import datetime
import jinja2 as jj

colorama.init()

# use to print profile specific configurations in printConfig()
table = BeautifulTable()
table.set_style(BeautifulTable.STYLE_BOX)
table.column_headers = ['','run','local save','s3 save']

# import configuration
with open("config_default.yaml", 'r') as ymlfile:
    config = yaml.load(ymlfile, Loader=yaml.FullLoader)

file_loader = jj.FileSystemLoader(PATH_TEMPLATES)
jj_env = jj.Environment(loader=file_loader)


def colored(txt, color) -> str:
    """Change str txt to color for terminal output
    Args:
        txt: text to change print color
        color: str color we want: ['green','cyan','magenta','red','blue']
    Return:
        txt: output text with ansi color
    """
    txt = str(txt)
    if color == "green":
        txt = Fore.GREEN + txt
    elif color == "red":
        txt = Fore.RED + txt
    elif color == "yellow":
        txt = Fore.YELLOW + txt
    txt += Fore.RESET
    return txt

def dictToTable(cols, dic):
    """Helper function to convert dict to beautifulTable"""
    from beautifultable import BeautifulTable
    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_BOX)
    table.column_headers = cols
    for key, val in dic.items():
        table.append_row([key, colored(val, "yellow")])
    return table

def colorBool(v) -> str:
    """Convert True to 'True' in green and False to 'False' in red
    """
    if v:
        return colored(str(v),"green")
    else:
        return colored(str(v),"red")

def printConfig():
    """Print configuration values
    """
    print(" CONFIGURATION ".center(60,'-'))
    print("\nS3")
    print('> {: <20}: {}'.format("")))

    print("\n1")
    print('> {: <20}: {}'.format("")))

    print("\n2")
    print('> {: <20}: {}'.format("")))

    print("\n3")
    table.append_row(['', colorBool(True), '',''])
    table.append_row(['', colorBool(True), '',''])
    table.append_row(['', colorBool(True), '',''])
    print(table)
    print("".center(60,'-'))


if __name__ == "__main__":
    printConfig()
