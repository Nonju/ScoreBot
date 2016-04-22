#usr/bin/env
# -*- utf-8 -*-

""" Program for calculating team win/loss-rates between two teams in CS:GO 
	<Powered by HLTV.org> """


import requests #for receiving webpages as tree-structured data
from lxml import etree #for scanning tree-structured tag-languages

import sys #for exit from menus (inside functions)
import datetime #from datetime import timedelta

def TeamSelection(removeTeam=None): #filename
	content = []
	#with open(filename) as f:
	with open('teamids.txt') as f:
		for line in f:
			if line[0] == '\n': continue #removes empty lines
			if line[0:2] == '//': continue #removes comments
			content.append(line[0:-1]) #!add way to write comments at end of line

	#prints available teams
	print('Pick a team: (enter team number)')
	counter = 0
	for entry in content:
		tmpArr = entry.split()[0:-1]
		if removeTeam != None and removeTeam['ID'] == tmpArr[-1]: continue

		print ('{0}: {1}'.format(counter+1,
				 ''.join([e+' ' if e != tmpArr[-1] else e for e in tmpArr])))
		counter += 1
	print ('\n0: Exit program') #option to end running program

	#print ('CONTENT:',content)
	#allow user to select a team 
	selection = ''
	while True:
		tmp = input('Team: ')
		if tmp == '0': sys.exit()
		if tmp.isdigit():
			tmp = int(tmp)
			if tmp >= 1 and tmp <= len(content):
				selection = int(tmp)
				break
			
		print('Invalid entry, try again!')
	
	#filtering content-array and storing selected team-data as a dict
	tmpArr = content[selection-1].split()
	teamName = ''.join([e+' ' if e != tmpArr[-1] else '' for e in tmpArr])
	teamName = teamName[0:-1] #quickfix to remove 'newline' from names
	team = {'name' : teamName, 'ID': tmpArr[-1]}

	#return int(content[selection].split()[1])
	#print('Receiving stats for team:', content[selection-1].split()[0])
	print('Receiving stats for team:', team['name']) #remove
	print('Team ID:', team['ID']) #remove
	#return content[selection-1].split()[-1]
	return team


def BuildMatchDict(arr=[]):
	"""Builds a predifined dict from array of matchdata"""
	if not arr: return #array is empty

	output = {}

	cont1 = arr[1].split() #team1 + rounds won
	cont2 = arr[2].split() #tema2 + rounds won

	output['date'] = arr[0]
	output['team1'] = cont1[0]
	output['team2'] = cont2[0]
	output['score'] = (cont1[1] + '-' + cont2[1])
	output['map'] = arr[3]
	output['outcome'] = arr[4]

	if len(arr) >= 6:
		output['event'] = arr[5]

	return output


def GetTeamData(team={}): # url=''
	"""Gets team data from webpage htmlpage"""
	if not team: #no team-dict passed to function
		print ('No team dict entered --> exiting function')
		return

	#request document from hltv-match-statistic-page
	url = 'http://www.hltv.org/?pageid=188&teamid=' + team['ID']
	page = requests.get(url)
	tree = etree.HTML(page.text)
	
	#retrieve all game data that can be found
	gamesList = tree.xpath('//div[@style="width:606px;height:22px;background-color:white"]')
	
	#filter text to get desired result
	result = []
	for section in gamesList:
		game = etree.HTML(etree.tostring(section))
		content = game.xpath('//div[@class="covSmallHeadline"]/text()')
		
		#content.append(game.xpath('//span/text()')[0])
		tmp = game.xpath('//span/text()') #get if won/loss
		if tmp: content.append(tmp[0])

		tmp = game.xpath('//div[@title]/text()')[0] #get event title
		if tmp: content.append(tmp)

		#make sure only specified teams (if any) are selected
		tmp = BuildMatchDict(content)
		result.append(tmp)
		#print(content) #remove
		
	return result

def HandleTeamData(matchData=[], teamData={}):
	"""Handles previous received team data and prints it to terminal
		- matchData: container with all of team1's matches
		- teamData: team1's name and ID as a dict
		- versusData: same as 'matchData' but only between team1/team2"""
	
	#allows user to match specified team with another specified team
	opt = input('Do you want to select an opponent?(y/n): ')
	if opt == 'y':
		print('inne') #remove
		opponent = TeamSelection(teamData)
		versusData = [] #stats between the 2 specified teams
		#versusData.append = list()
		print('Otherteam:', opponent['name'])

		#Filters team1's gamelist from matches with other teams than against team2
		versusData = list([e for e in matchData if e['team2'].upper() == opponent['name'].upper()])
		
		
		for entry in versusData: print (entry, '\n')

		#code for displaying stats vs that opponent

	print('efter') #remove

	#code for displaying teams general stats
	pass

	

def main():

	""" TODO:
	- Read all teamID's from file (+ Find out more teamIDs!!)
	- Search all pages from HLTV with those ID's (or specified (probably this one))
	- Find all games that matches both teams (ex: NiP vs fnatic)
	- 

	baseurl: http://www.hltv.org/?pageid=188&teamid=4411&mapid=29
	"""

	

	teamData = TeamSelection()

	#webpageUrl = 'http://www.hltv.org/?pageid=188&teamid=' + teamID
	#container = GetTeamData(webpageUrl) #get team stats as dict
	container = GetTeamData(teamData) #get team stats as dict
	if not container: #no-data-found failsafe
		print ('No team stats could be found, exiting program.')
		return

	
	HandleTeamData(container, teamData)



if __name__ == '__main__':
	main()

	