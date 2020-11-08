#!/usr/bin/env python3

from selenium import webdriver
import requests
import time

ADMIN_SESSION = "pybu3zheoyeupyzgodcrxf7oqc"
PREFIX = "http://web"

options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.headless = True

def query(url):
    driver = webdriver.Chrome(options = options)
    driver.get(PREFIX)
    driver.delete_all_cookies()
    driver.add_cookie({'name': 'PHPSESSID', 'value': ADMIN_SESSION, 'path': '/'})
    driver.get(url)
    time.sleep(5)
    driver.close()

reports = requests.get(PREFIX + "/reports.php?secret=hunter2").text.strip().splitlines()
for report in reports:
    filetime, filename = report.split(";", 1)
    print("Checking %s" % filename)
    requests.get(PREFIX + "/reports.php?secret=hunter2&delete=%s" % filename)
    query(PREFIX + "/i/%s" % filename)

