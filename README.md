# carDB_tool
Command line tool for creating SQLite DB of Year/Make/Model/Engine from US government data.

Currently this program uses data from https://www.fueleconomy.gov/ as it's main source.
This is the most readily avaliable complete data from 1984 - future.

To build the database, simply run:
python3 carDB_tool.py

The output file will be named "base_car.db"

Currently there are no plans to go back farther in time than 1984.
Providing there is no change in the structure of the data from the government website, this tool
should continue to work for the forseeable future, rebuilding the database for new years as needed.

This tool does take a while to run as the information is very spread out, but there is
terminal output of the information being written to the DB.
