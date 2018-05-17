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
qbid.fill_day(2018, 5, 18, form_data)


# Fill a whole week with the same data
week_start = 7
week_end_plus_one = 12 # Friday is 11, but you need to add 1 more number (more info, range() Python function)

form_data = [
    ["Activity1ID", "HOURS"],
    ["Activity2ID", "HOURS"]
]

for day in range(week_start, week_end_plus_one):
    qbid.fill_day(2018, 5, day, form_data)


# Fill a whole week with specific data for each day
week_start = 7
week_end_plus_one = 12 # Friday is 11, but you need to add 1 more number (more info, range() Python function)

form_data = {
    7: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ],
    8: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ],
    9: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ],
    10: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ],
    11: [
        ["Activity1ID", "HOURS"],
        ["Activity2ID", "HOURS"]
    ]
}

for day in range(week_start, week_end_plus_one):
    qbid.fill_day(2018, 5, day, form_data[day])


# And more! Use your imagination! Extend the class and make a pull request!
