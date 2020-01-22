# An Automated Dataset Report Generator

[!] Code and approach is based on Pandas Profiling:
https://github.com/pandas-profiling/pandas-profiling

The objective of this code is to be able to easily generate an HTML report of any given dataset.
Ideally we want the user to be able to write up his own analysis and be able to push it to a special class which will load the results into an HTML report.

## Features

The user can:
- Define the title of the report
- Generate a summary passed as a dictionary of values
- Generate visualizations and display them in a list of cards
- etc.
- Pass his analysis functions so that they are saved and can be run as an
automated pipeline.
