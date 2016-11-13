#! /usr/bin/env python

import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import smtplib
import unittest
import time
import re


class fntsyLu(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.get("http://www.espn.com/fantasy/basketball/")

	def getNumber(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		elements = driver.find_elements_by_class_name("playerEditSlot")
		str = elements[num].get_attribute('id')
		playerNum = re.findall('\d+', str)
		return playerNum[0]

	def getPosition(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		str = "playername_" + playerList[num]
		playerPositionText = "//*[@id=" + '\'' + str + '\'' + "]"
		playerPositionTextElement = wait.until(lambda driver:driver.find_element_by_xpath(playerPositionText))
		playerHTML = playerPositionTextElement.get_attribute('innerHTML')
		positions = re.findall('PG|SG|SF|PF|\sC\s', playerHTML)
		return positions

	def hasGame(self, str):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		hasGame = True
		try:
			wait.until(lambda driver:driver.find_element_by_xpath(str))
		except TimeoutException:
			hasGame = False
			return hasGame

		return hasGame

	def getName(self, str):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		nameElement = wait.until(lambda driver: driver.find_element_by_xpath(str))
		name = nameElement.get_attribute('text')
		return name

	def setPlayerList(self):
		driver = self.driver
		elements = driver.find_elements_by_class_name("playertablePlayerName")
		playerHTML = ""
		for i in range(0, len(elements)):
			playerHTML += elements[i].get_attribute('id')

		digits = re.findall('\d+', playerHTML)
		global playerList
		playerList = []
		for d in range(0, len(digits), 1):
			playerList.insert(d, digits[d])  
				
	def getBenchList(self):
		benchPlayerList = []
		benchPlayerGameStatuses = []
		count = 0
		print playerList
		for i in range(10, 13, 1):
			print i
			str = "pncPlayerRow_" + self.getNumber(i)
			playerGameStatus = "//*[@id=" + "\'" + str + "\'" + "]/td[6]/a"
			benchPlayerGameStatuses.insert(count, self.hasGame(playerGameStatus))
			playerName = "//*[@id=" + '\'' + 'playername_' + playerList[i] + '\'' + ']/a[1]'
			newsXPath = "'//*[@id=" '\'' + "playername_" + playerList[i] + '\'' + "]/a[2]/img"
			if benchPlayerGameStatuses[count] == True:
				print self.hasGame(newsXPath)
				if not self.hasGame(newsXPath):
					benchPlayerList.insert(count, self.getName(playerName))
				else:
					print "NO NEWS"
					playerName = "//*[@id=" + '\'' + 'playername_' + playerList[i] + '\'' + ']/a'
					print playerName
					benchPlayerList.insert(count, self.getName(playerName))
			count += 1;
		return benchPlayerList

	def sendEmail(self, players):
		emailServer = smtplib.SMTP('smtp.gmail.com', 587)
		emailServer.ehlo()
		emailServer.starttls()
		email = "INSERT EMAIL HERE"
		password = "INSERT PASSWORD HERE"
		recipientEmail = "INSERT RECIPIENT EMAIL"
		emailServer.login(email, password)
		str = ""
		for i in range(0, len(players), 1):
			str += players[i]
			if i != len(players) - 1:
				str += ", "
		emailBody = '\nCould not get ' + str + ' into your starting lineup even though he has a game. '
		if len(players) > 1:
			emailBody = '\nCould not get ' + str + ' into your starting lineup even though they have games.'
		emailServer.sendmail(email, recipientEmail,
			'Subject: FANTASY LINEUP ISSUE' + '\n' + emailBody)
		emailServer.quit()
		# print "Email Sent!"

	def moveToPosition(self, num, num2):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		rowGameStatus = "pncPlayerRow_" + self.getNumber(num)
		rowGameStatusStr = "//*[@id=" + "\'" + rowGameStatus + "\'" + "]/td[6]/a"
		if self.hasGame(rowGameStatusStr):
			if num == 0 or num == 1:
				self.moveToPosition(5, num2)
				return
			elif num == 2 or num == 3:
				self.moveToPosition(6, num2)
				return
			elif num > 3:
				str = "pncButtonMoveSelected_" + playerList[num2]
				moveButton = "//*[@id=" + '\'' + str + '\'' + "]"
				moveButtonElement = wait.until(lambda driver: driver.find_element_by_xpath(moveButton))
				moveButtonElement.click()
			return
		else:
			str = "pncButtonHere_" + self.getNumber(num)
			position = "//*[@id=" + '\'' + str + '\'' + "]"
			positionButton = wait.until(lambda driver:driver.find_element_by_xpath(position))
			positionButton.click()
		return

	def movePlayerToPosition(self, positionList,  num):
		for i in range(0, len(positionList), 1):
			if positionList[i] == "PG":
				self.moveToPosition(0, num)
				return True
			elif positionList[i] == "SG":
				self.moveToPosition(1, num)
				return True 
			elif positionList[i] == "SF":
				self.moveToPosition(2, num)
				return True
			elif positionList[i] == "PF":
				self.moveToPosition(3, num)
				return True 
			elif positionList[i] == "C":
				self.moveToPosition(4, num)
				return True
		return False

	def submitLineUp(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		submit = "//*[@id='pncSaveRoster0']"
		submitElement = wait.until(lambda driver: driver.find_element_by_xpath(submit))
		submitElement.click()
		time.sleep(2)
		self.setPlayerList()

	def movePlayerToSL(self, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		positionList = self.getPosition(num)
		if num == 12:
			self.movePlayerToPosition(positionList, num)
			self.submitLineUp()
			return True
		return self.movePlayerToPosition(positionList, num)

	def movePlayerToUtil(self, str, str2, num, num2):
		driver = self.driver 
		wait = WebDriverWait(driver, 10)

		if self.hasGame(str):
			if num2 == 9:
				self.movePlayerToSL(num)
			return False 
		else:
			buttonElement = wait.until(lambda driver: driver.find_element_by_xpath(str2))
			buttonElement.click()
			if num == 12:
				self.submitLineUp()
			return True
		return False

	def initializeHereStrings(self, num):
		stringList = []
		playerRow = "pncPlayerRow_" + self.getNumber(num)
		playerRowGameStatus = "//*[@id=" + '\'' + playerRow + '\'' + "]/td[6]/a"
		here = "pncButtonHere_" + self.getNumber(num)
		playerRowButton = "//*[@id=" + '\'' + here + '\'' + "]"
		stringList = [playerRowGameStatus, playerRowButton]
		return stringList

	def moveToUtil(self, num):
		# Check UTIL - table rows 7, 8, 9
		driver = self.driver
		wait = WebDriverWait(driver, 10)

		row7Strings = self.initializeHereStrings(7)
		if self.movePlayerToUtil(row7Strings[0], row7Strings[1], num, 7):
			return
		
		row8Strings = self.initializeHereStrings(8)
		if self.movePlayerToUtil(row8Strings[0], row8Strings[1], num, 8):
			return

		row9Strings = self.initializeHereStrings(9)
		if self.movePlayerToUtil(row9Strings[0], row9Strings[1], num, 9):
			return
		
		return

	def initializeMoveStrings(self, num):
		stringList = []
		playerRow = "pncPlayerRow_" + self.getNumber(num)
		playerRowGameStatus = "//*[@id=" + '\'' + playerRow + '\'' + "]/td[6]/a"
		move = "pncButtonMove_" + playerList[num]
		playerRowButton = "//*[@id=" + '\'' + move + '\'' + "]"
		stringList = [playerRowGameStatus, playerRowButton]
		return stringList

	def movePlayer(self, str, str2, num):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		if self.hasGame(str):
			buttonElement = wait.until(lambda driver: driver.find_element_by_xpath(str2))
			buttonElement.click()
			if num == 10 or num == 11 or num == 12:
				self.moveToUtil(num)
		elif not self.hasGame(str):
			if num == 12:
				self.submitLineUp()
			else:
				pass

	def checkBench(self):
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		
		row10Strings = self.initializeMoveStrings(10)
		self.movePlayer(row10Strings[0], row10Strings[1], 10)

		row11Strings = self.initializeMoveStrings(11)
		self.movePlayer(row11Strings[0], row11Strings[1], 11)
	
		row12Strings = self.initializeMoveStrings(12)
		self.movePlayer(row12Strings[0], row12Strings[1], 12)

	def checkUtil(self):
		self.setPlayerList()
		row7Strings = self.initializeMoveStrings(7)
		self.movePlayer(row7Strings[0], row7Strings[1], 7)
		if self.movePlayerToSL(7):
			pass

		row8Strings = self.initializeMoveStrings(8)
		self.movePlayer(row8Strings[0], row7Strings[1], 8)
		if self.movePlayerToSL(8):
			pass

		row9Strings = self.initializeMoveStrings(9)
		self.movePlayer(row9Strings[0], row9Strings[1], 9)
		if self.movePlayerToSL(9):
			pass
		else:
			return

		self.checkBench()

	def login(self):
		# initialize variables
		driver = self.driver
		username = "INSERT USERNAME"
		password = "INSERT PASSWORD"
		wait = WebDriverWait(driver, 10)

		# click Log In button
		loginButtonXpath = "//*[@id='global-header']/div[2]/ul/li[2]/a"
		loginButtonElement1 = wait.until(lambda driver: driver.find_element_by_xpath(loginButtonXpath))
		loginButtonElement1.click()

		# find email and pass ID
		emailFieldID = "//*[@id='did-ui']/div/div/section/section/form/section/div[1]/div/label/span[2]/input"
		passFieldID = "//*[@id='did-ui']/div/div/section/section/form/section/div[2]/div/label/span[2]/input"
		
		# switch to frame so script can type
		driver.switch_to.frame("disneyid-iframe")
		
		# find email input box and type in email
		emailFieldElement = wait.until(lambda driver: driver.find_element_by_xpath(emailFieldID))
		emailFieldElement.click()
		emailFieldElement.clear()
		emailFieldElement.send_keys(username)

		# find pass input box and type in password
		passFieldElement = wait.until(lambda driver: driver.find_element_by_xpath(passFieldID))
		passFieldElement.click()
		passFieldElement.clear()
		passFieldElement.send_keys(password)
		
		# click log in button
		loginButtonXpath2 = "//*[@id='did-ui']/div/div/section/section/form/section/div[3]/button"
		loginButtonElement2 = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(loginButtonXpath2))
		loginButtonElement2.click()

		leagueID = str(self.LEAGUEID)
		teamID = str(self.TEAMID)
		leagueURL = "http://games.espn.com/fba/clubhouse?leagueId=" + leagueID + "&teamId=" + teamID + "&seasonId=2017"
		time.sleep(2)
		driver.get(leagueURL)
		time.sleep(2)

	def tearDown(self):
		self.driver.quit()

	def test_main(self):
		self.login()
		time.sleep(2)
		driver = self.driver
		wait = WebDriverWait(driver, 10)
		time.sleep(2)
		self.setPlayerList()
		self.checkBench()
		benchList = self.getBenchList()
		if len(benchList) > 0:
			self.checkUtil()
			self.sendEmail(benchList)
		else:
			pass
		time.sleep(2)
		self.tearDown()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		fntsyLu.TEAMID = sys.argv.pop()
		fntsyLu.LEAGUEID = sys.argv.pop()
	unittest.main()
		