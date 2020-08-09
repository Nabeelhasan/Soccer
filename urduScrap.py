from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pprint import pprint
import time
import subprocess
import ast
import hashlib

browser = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
browser.get("https://forvo.com/languages-pronunciations/ur/")
for i in range(20):
	url = "https://forvo.com/languages-pronunciations/ur/page-"+str(i)+"/"
	browser.get(url)
	# langPath = browser.find_elements_by_xpath("//a[contains(@class, 'word')]")
	voicePath = browser.find_elements_by_xpath("//span[contains(@class, 'play ')]")
	ResourceList = []
	texList = []
	# print(len(langPath))
	for p in voicePath:
		print(p.text)
		time.sleep(10)
		p.location_once_scrolled_into_view
		# button = browser.execute(p.click())
		button = p.click()
		if button is None:
			print("button is clicked")

			# time.sleep(5)
			Resources = browser.execute_script("return window.performance.getEntries();")
			for resource in Resources:
				if '.mp3' in resource['name']:
					# print(resource['name'])

					if p.text.split(" pronunciation")[0] not in texList:
						print("This is the Text After Split:",p.text.split(" pronunciation")[0])
						texList.append(p.text.split(" pronunciation")[0])
					if resource['name'] not in ResourceList:
						ResourceList.append(resource['name'])

	for i in range(len(texList)):
		try:
			# newDict[texList[i]] = ResourceList[i+1]
			result = hashlib.md5(texList[i].encode())
			hashcode = result.hexdigest()
			f = open("/home/maximuslinux/Voice/forvoUrdu/"+hashcode+"forvoUrdu"+".txt",'w')
			f.write(texList[i].strip("\n"))
			f.close()
			# AudioResponse = requests.get(ResourceList[i+1])
			fileName = "/home/maximuslinux/Voice/forvoUrdu/"+hashcode+"forvoUrdu"+".mp3"
			subprocess.call(['wget','-O',fileName,ResourceList[i+1]])
			
		except IndexError:
			pass



browser.quit()