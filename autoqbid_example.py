#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
from autoqbid import AutoQbid

# Open a Firefox AutoQbid instance
#   Note: to use it, install geckodriver
qbid = AutoQbid()
qbid.driver.close() # And close it


# Open a Chrome AutoQbid instance
#   Note: to use it, install chromedriver
qbid = AutoQbid(browser="Chrome")


# Login with your username and password
qbid.login("username", "password")


# List all your activities (needed to get their IDs)
qbid.list_activites()


# Fill an specific day
#   Note: to get the activities ID, execute qbid.list_activites()
#   Note 2: the hours are in float format:
#       15 mins         -> 0.25,
#       30 mins         -> 0.50,
#       1h              -> 1.0,
#       2h and 45 mins  -> 2.75
#       ...
form_data = [
    ["Activity1ID", "HOURS"],
    ["Activity2ID", "HOURS"]
]
qbid.fill_day("2018/5/19", form_data)


# Fill a whole week with the same data
form_data = [
    ["Activity1ID", "HOURS"],
    ["Activity2ID", "HOURS"]
]
qbid.fill_days("2018/5/7", "2018/5/11", form_data)

# Fill a whole week with specific data for each day
form_data = {
    "default": [
        ["Activity1ID", "HOURS"]
    ],
    9: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ],
    10: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ]
}
qbid.fill_days("2018/5/7", "2018/5/11", form_data, different_data_every_day=True)


# And more! Use your imagination! Extend the class and make a pull request!
