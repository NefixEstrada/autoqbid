#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class AutoQbid:
    """
    Main class for the program
    """
    def __init__(self, username=None, password=None, year=None, month=None, day=None, form_data=[], browser="Firefox"):
        if username:
            self.username = username

        if password:
            self.password = password

        self.date = dict()
        if year:
            self.date["year"] = year

        if month:
            self.date["month"] = month

        if day:
            self.date["day"] = day

        self.form_data = [{
            "activity_id": activity[0],
            "hours": activity[1]
        } for activity in form_data]

        try:
            self.driver = getattr(webdriver, browser)()

            try:
                self.driver.maximize_window()

            except Exception:
                print("Sorry, your browser doesn't support maximizing the window!")

            self.driver.get("https://www.empresaiformacio.org/sBidAlumne/")
            self.driver.switch_to.frame(1)

        except Exception:
            pass

    def __del__(self):
        self.driver.close()

    def login(self, username=None, password=None):
        """
        Login to Qbid
        """
        if username:
            self.username = username

        if password:
            self.password = password

        username_input = self.driver.find_element_by_id("username")
        password_input = self.driver.find_element_by_id("password")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        password_input.send_keys(Keys.RETURN)

    def move_to_month(self):
        pass

    def open_day_form(self):
        pass

    def fill_activity_log(self):
        pass

    def fill_day(self):
        pass
