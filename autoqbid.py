#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep


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

    def move_to_month(self, year=None, month=None):
        """
        Change the month (and year) in the calendar
        """
        if year:
            self.date["year"] = year

        if month:
            self.date["month"] = month

        months = {
            "gener": 1,
            "febrer": 2,
            "març": 3,
            "abril": 4,
            "maig": 5,
            "juny": 6,
            "juliol": 7,
            "agost": 8,
            "setembre": 9,
            "octubre": 10,
            "novembre": 11,
            "desembre": 12
        }

        try:
            WebDriverWait(self.driver, 1).until(
                ec.frame_to_be_available_and_switch_to_it("contentmain")
            )

            WebDriverWait(self.driver, 1).until(
                ec.presence_of_element_located((By.ID, "popupAgenda_calHeader0"))
            )
        except TimeoutException:
            try:
                self.driver.find_element_by_id("popupAgenda_calHeader0")

            finally:
                pass

        finally:
            calendar_date_array = self.driver.find_element_by_id("popupAgenda_calHeader0").text.split(" ")
            calendar_date = dict({
                "year": int(calendar_date_array[1]),
                "month": int(months[calendar_date_array[0].lower()])
            })

            if not self.date["year"] == calendar_date["year"]:
                sleep(0.3)
                year_difference = self.date["year"] - calendar_date["year"]
                self.driver.execute_script("popupAgenda.shiftAgenda({})".format(year_difference * 12))

            if not self.date["month"] == calendar_date["month"]:
                sleep(0.3)
                month_difference = self.date["month"] - calendar_date["month"]
                self.driver.execute_script("popupAgenda.shiftAgenda({})".format(month_difference))

    def open_day_form(self):
        pass

    def fill_activity_log(self):
        pass

    def fill_day(self):
        pass
