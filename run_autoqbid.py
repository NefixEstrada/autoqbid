#!/usr/bin/env python3

import time

from autoqbid import AutoQbid

USERNAME = "user"
PASSWORD = "password"

qbid = AutoQbid()
qbid.login(USERNAME, PASSWORD)

time.sleep(2)

form_data = [["1234", "6.0"]]
qbid.fill_days("2019/03/26", "2019/05/30", form_data)
