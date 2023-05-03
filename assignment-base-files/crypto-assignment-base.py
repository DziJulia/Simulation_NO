#!/usr/bin/python
#
# crypto-assignment-base.py
#
# full implementation of the cryptocurrency prediction assignment by using numerical optimisation

# imports needed to make this script work
import csv
import math
import random

import self
from simanneal import Annealer
from deap import base
from deap import creator
from deap import tools
import timeit

from f import CryptoAnneal
from simulation import Simulation
from NewSimulation import Simulation1


# function that will read in all of the cryptocurrenies and will assemble it into workable data
def assembleData(dates, closing_values):
    # read in all of the CSV files to make sure they are working
    bitcoin_rows = readCSVFile('coin_Bitcoin.csv')
    dogecoin_rows = readCSVFile('coin_Dogecoin.csv')
    ethereum_rows = readCSVFile('coin_Ethereum.csv')
    litecoin_rows = readCSVFile('coin_Litecoin.csv')
    xrp_rows = readCSVFile('coin_XRP.csv')

    # create a set of all the dates in all 5 CSVs. skip the first row as it is the header
    # sort the set at the end and turn it into a list
    dateset = set()
    for i in range(1, len(bitcoin_rows)):
        dateset.add(stripTime(bitcoin_rows[i][3]))
    for i in range(1, len(dogecoin_rows)):
        dateset.add(stripTime(dogecoin_rows[i][3]))
    for i in range(1, len(ethereum_rows)):
        dateset.add(stripTime(ethereum_rows[i][3]))
    for i in range(1, len(litecoin_rows)):
        dateset.add(stripTime(litecoin_rows[i][3]))
    for i in range(1, len(xrp_rows)):
        dateset.add(stripTime(xrp_rows[i][3]))
    for i in list(sorted(dateset)):
        dates.append(i)

    # create lists for all 5 currencies that contain all of the closing values that are mapped to the correct date
    # the first row will be the date
    for i in range(5):
        closing_values.append([0.0] * len(dateset))

    # add the closing value of all of the currencies into the closing values 2D list
    mapClosingValues(bitcoin_rows, closing_values, dates, 0)
    mapClosingValues(dogecoin_rows, closing_values, dates, 1)
    mapClosingValues(ethereum_rows, closing_values, dates, 2)
    mapClosingValues(litecoin_rows, closing_values, dates, 3)
    mapClosingValues(xrp_rows, closing_values, dates, 4)


def runer():
    weights = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # bitcoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # bitcoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # dodgecoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # dodgecoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Ethereum
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Ethereum
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # LiteCoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # LiteCoin
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # xrp
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # xrp
    ]
    nameCurrency = ['BitCoin', 'DogeCoin', 'Ethereum', 'LiteCoin', 'XRP']
    i = 0
    while i < len(weights):
        j = 0
        while j < len(weights[i]):
            a = random.uniform(-1, 1)
            weights[i][j] = a
            j += 1
        i += 1

    tsp = CryptoAnneal(weights, my_simulation2.totalNetValue(), closing_values, nameCurrency)
    tsp.steps = 100000
    # run the annealer
    state, e = tsp.anneal()


# function that will map the closing value data from the given set of rows to the correct dates in the dataset
def mapClosingValues(rows, closing_values, dates, currency):
    # take the first date from the rows as this will give us our starting index.
    # unlike the stock market, crypto markets work on weekends as well so the dates will be in order
    date = stripTime(rows[1][3])
    starting_index = dates.index(date)

    # go through each of the rows and set the closing value. we skip the irst row as it is a header
    for i in range(1, len(rows)):
        closing_values[currency][starting_index + i - 1] = float(rows[i][7])


# function that will take in the given CSV file and will read in its entire contents
# and return a list of lists
def readCSVFile(file):
    # the rows to return
    rows = []

    # open the file for reading and give it to the CSV reader
    csv_file = open(file)
    csv_reader = csv.reader(csv_file, delimiter=',')

    # read in each row and append it to the list of rows.
    for row in csv_reader:
        rows.append(row)

    # close the file when reading is finished
    csv_file.close();

    # return the rows at the end of the function
    return rows


# function that will take a date time and strip out the time from it
def stripTime(str_datetime):
    # datetimes will have the first 10 characters to represent the date so just extract these
    return str_datetime[0:10]


# entry point to the script
if __name__ == '__main__':
    # empty lists for the dates and the closing data we need
    dates = []
    closing_values = []
    weights = [
        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  # bitcoin
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01],  # bitcoin
        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  # dodgecoin
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01],  # dodgecoin
        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  # Ethereum
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01],  # Ethereum
        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  # LiteCoin
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01],  # LiteCoin
        [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  # xrp
        [-0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01, -0.01],  # xrp
    ]
    # assemble the data that we need and run the appropriate optimisation
    assembleData(dates, closing_values)
    my_simulation2 = Simulation1(closing_values, weights)
    #

    runer()


    my_simulation2.simulate()
    # my_simulation2.printPortfolioStrategy()
    # value with tax
    print("\nValue what i have portfolio", my_simulation2.totalValue())
    print("Total minus capital gains", my_simulation2.totalNetValue())