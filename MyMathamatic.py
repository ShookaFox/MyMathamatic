import json
import time
import requests
import yaml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

try:
	with open('config.yaml', 'r') as file:
		config = yaml.safe_load(file)
except:
	print("Config file config.yaml missing or damaged!")
	exit()

browser = webdriver.Firefox(keep_alive=False, executable_path=config['geckodriver_path'])
browser.get(config['mymathlab_url'])
# Go to the log in page (to set a cookie) and log in
browser.find_element_by_link_text("Sign in").click()
browser.find_element_by_id("username").send_keys(config['username'])
browser.find_element_by_id('password').send_keys(config['password'] + Keys.RETURN)
# Skip any kind of account verification
if browser.find_elements_by_id("skip"):
	browser.find_element_by_id("skip").click()
time.sleep(3)
# Go through all the links to classes and click the one specified
for class_link in browser.find_elements_by_class_name("title-wrapper")[1:]:
	if class_link and class_link.text == config['class']:
		class_link.click()
		break
# This should trigger if user specifies the wrong course
if '?courseId' not in browser.current_url:
	print('I couldn\'t  find your course, perhaps you entered the wrong course name?')
	exit()