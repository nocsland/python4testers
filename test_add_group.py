# -*- coding: utf-8 -*-
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from group import Group


def open_home_page(driver):
    driver.get("http://localhost/addressbook/")


def login(driver, username, password):
    driver.find_element_by_name("user").click()
    driver.find_element_by_name("user").send_keys(username)
    driver.find_element_by_name("pass").click()
    driver.find_element_by_name("pass").send_keys(password)
    driver.find_element_by_xpath(u"//input[@value='Войти']").click()


def open_groups_page(driver):
    driver.find_element_by_link_text(u"Группы").click()


def create_group(driver, group):
    # init group creation
    driver.find_element_by_name("new").click()
    # fill group form
    driver.find_element_by_name("group_name").click()
    driver.find_element_by_name("group_name").clear()
    driver.find_element_by_name("group_name").send_keys(group.name)
    driver.find_element_by_name("group_header").click()
    driver.find_element_by_name("group_header").clear()
    driver.find_element_by_name("group_header").send_keys(group.header)
    driver.find_element_by_name("group_footer").click()
    driver.find_element_by_name("group_footer").clear()
    driver.find_element_by_name("group_footer").send_keys(group.footer)
    # submit group creation
    driver.find_element_by_name("submit").click()


def return_to_groups_page(driver):
    driver.find_element_by_link_text(u"Группы").click()


def logout(driver):
    driver.find_element_by_link_text(u"Выйти").click()


class UntitledTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_add_empty_group(self):
        driver = self.driver
        open_home_page(driver)
        login(driver, username="admin", password="secret")
        open_groups_page(driver)
        create_group(driver, Group(name="", header="", footer=""))
        return_to_groups_page(driver)
        logout(driver)

    def test_add_group(self):
        driver = self.driver
        open_home_page(driver)
        login(driver, username="admin", password="secret")
        open_groups_page(driver)
        create_group(driver, Group(name="ttththrt", header="gregeg", footer="thtrhrwh"))
        return_to_groups_page(driver)
        logout(driver)

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
