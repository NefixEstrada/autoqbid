#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, timedelta
from time import sleep

# Imports
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tabulate import tabulate


class AutoQbid:
    """
    Main class for the program
    """

    def __init__(
        self,
        username=None,
        password=None,
        year=None,
        month=None,
        day=None,
        form_data=[],
        browser="Firefox",
    ):
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

        self.form_data = [
            {"activity_id": activity[0], "hours": activity[1]} for activity in form_data
        ]

        try:
            if browser == "Headless":
                options = webdriver.ChromeOptions()
                options.add_argument("headless")

                self.driver = webdriver.Chrome(chrome_options=options)

            else:
                self.driver = getattr(webdriver, browser)()

            try:
                self.driver.maximize_window()

            except Exception:
                print("Sorry, your browser doesn't support maximizing the window!")

            self.driver.get("https://www.empresaiformacio.org/sBidAlumne/")
            self.driver.switch_to.frame(1)

        except Exception as e:
            print(e)

    def __del__(self):
        try:
            self.driver.close()

        except AttributeError:
            pass

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
            "desembre": 12,
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
            calendar_date_array = self.driver.find_element_by_id(
                "popupAgenda_calHeader0"
            ).text.split(" ")
            calendar_date = dict(
                {
                    "year": int(calendar_date_array[1]),
                    "month": int(months[calendar_date_array[0].lower()]),
                }
            )

            if not self.date["year"] == calendar_date["year"]:
                sleep(0.3)
                year_difference = self.date["year"] - calendar_date["year"]
                self.driver.execute_script(
                    "popupAgenda.shiftAgenda({})".format(year_difference * 12)
                )

            if not self.date["month"] == calendar_date["month"]:
                sleep(0.3)
                month_difference = self.date["month"] - calendar_date["month"]
                self.driver.execute_script(
                    "popupAgenda.shiftAgenda({})".format(month_difference)
                )

    def open_day_form(self, day=None, ignore_day_errors=False):
        """
        Select the day and open its form
        """
        if day:
            self.date["day"] = day

        try:
            day_to_fill = self.driver.find_element_by_id(
                "cellDay{}".format(self.date["day"])
            )
            day_to_fill_status = day_to_fill.get_attribute("class")

        except NoSuchElementException:
            print("Please, make sure that the day you have inserted exists!")
            sys.exit(1)

        # TODO: Improve this code. Make it again with tries and keeping it DRY
        if day_to_fill_status == "AgCell" or day_to_fill_status == "AgCellFestaF":
            if not ignore_day_errors:
                print("Please, select a day that you can fill!")
                sys.exit(1)

            else:
                print(
                    "Unable to fill {}/{}/{}!".format(
                        self.date["year"], self.date["month"], self.date["day"]
                    )
                )
                return False

        else:
            if (
                datetime.strptime(
                    "{}/{}/{}".format(
                        self.date["year"], self.date["month"], self.date["day"]
                    ),
                    "%Y/%m/%d",
                )
                > datetime.now()
            ):
                if not ignore_day_errors:
                    print("Sorry, you can't fill days that are from the future!")
                    sys.exit(1)

                else:
                    print(
                        "Unable to fill {}/{}/{}!".format(
                            self.date["year"], self.date["month"], self.date["day"]
                        )
                    )
                    return False

            else:
                self.driver.execute_script(
                    "popupAgenda.moveAgenda('{}', '{}', '{}', true)".format(
                        self.date["year"], self.date["month"], self.date["day"]
                    )
                )

                sleep(0.1)

                try:
                    activity_log_url = WebDriverWait(self.driver, 1).until(
                        ec.presence_of_element_located(
                            (
                                By.XPATH,
                                "//*[contains(text(), 'Activitat diària del dossier ')]",
                            )
                        )
                    )

                except TimeoutException:
                    print(
                        "Unable to fill {}/{}/{}!".format(
                            self.date["year"], self.date["month"], self.date["day"]
                        )
                    )
                    return False

                activity_log_url.click()
                return True

    def close_day_form(self):
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(1)

        home_button = self.driver.find_element_by_id(
            "titleInfo"
        ).find_element_by_class_name("ModuleLink")
        home_button.click()

    def fill_activity_log(self, form_data=None):
        """
        Fill the activity log form
        """
        if form_data:
            self.form_data = []
            for activity in form_data:
                self.form_data.append(
                    {"activity_id": activity[0], "hours": activity[1]}
                )

        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located(
                    (By.ID, "observacionsInutilsAlumneMaiOmplira")
                )
            )

        finally:
            options_to_clean = self.driver.find_elements_by_xpath(
                "//option[@value='0']"
            )
            for option in options_to_clean:
                option.click()

            for activity in self.form_data:
                select = self.driver.find_element_by_id(
                    "inp_" + activity["activity_id"]
                )
                option_to_click = select.find_element_by_xpath(
                    "./option[@value='{}']".format(activity["hours"])
                )
                option_to_click.click()

            sleep(0.5)

            save_button = self.driver.find_element_by_xpath(
                "//*[@title='Emmagatzemar activitat diària']"
            )
            save_button.click()
            sleep(1)

            self.close_day_form()

    def list_activites(self):
        """
        Prints a list of activities_ids and their name
        """
        now = datetime.now()
        self.date["year"] = int(now.strftime("%Y"))
        self.date["month"] = int(now.strftime("%m"))
        self.date["day"] = int(now.strftime("%d"))

        self.move_to_month()
        self.open_day_form()

        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located(
                    (By.ID, "observacionsInutilsAlumneMaiOmplira")
                )
            )

        finally:
            activities = []
            for activity in self.driver.find_elements_by_class_name("activitatDiaria"):
                try:
                    activity_description = (
                        activity.find_element_by_class_name("activitatInfo")
                        .find_element_by_tag_name("label")
                        .text
                    )

                    # Add a line break every 120 characters to make the table fill in a terminal
                    activity_description = "\n".join(
                        [
                            activity_description[i : i + 120]
                            for i in range(0, len(activity_description), 120)
                        ]
                    )

                    activity_id = (
                        "\033[1m\033[93m"
                        + activity.get_attribute("id").replace("activitat", "")
                        + "\033[0m\033[0m"
                    )

                except NoSuchElementException:
                    pass

                else:
                    try:
                        activity.find_element_by_class_name("activitatHores")
                        activities.append([activity_description, activity_id])

                    except NoSuchElementException:
                        pass

        print(
            tabulate(activities, ("Description", "Activity ID"), tablefmt="fancy_grid")
        )
        self.close_day_form()

    def fill_day(self, date=None, form_data=None, ignore_day_errors=False):
        """
        Fill a single day
        """
        if date:
            date = datetime.strptime(date, "%Y/%m/%d")
            self.date["year"] = date.year
            self.date["month"] = date.month
            self.date["day"] = date.day

        if form_data:
            self.form_data = []
            for activity in form_data:
                self.form_data.append(
                    {"activity_id": activity[0], "hours": activity[1]}
                )

        self.move_to_month()

        sleep(0.2)

        day_opened = self.open_day_form(ignore_day_errors=ignore_day_errors)
        if day_opened:
            self.fill_activity_log()

    def fill_days(
        self, start_date, end_date, form_data, different_data_every_day=False
    ):
        """
        Fill a range of days
        """
        start_date = datetime.strptime(start_date, "%Y/%m/%d")
        end_date = datetime.strptime(end_date, "%Y/%m/%d")
        days_difference = end_date - start_date

        for i in range(days_difference.days + 1):
            day = start_date + timedelta(days=i)
            if not different_data_every_day:
                day_form_data = form_data

            else:
                try:
                    day_form_data = form_data[day.day]

                except KeyError:
                    try:
                        day_form_data = form_data["default"]

                    except KeyError:
                        print("Please, add a 'default' key!")
                        sys.exit(1)

            self.fill_day(day.strftime("%Y/%m/%d"), day_form_data, True)
