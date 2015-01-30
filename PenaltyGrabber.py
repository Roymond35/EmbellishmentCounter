'''
	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''
from HTMLParser import HTMLParser
import glob,os

''' Brief Explanation of the penalty array elements:
	i[0] - Player's Team
	i[1] - Player's Name
	i[2] - Player's Penalty
	i[3] - Home or Away
	i[4] - Opponent
	i[5] - Date
	i[6] - First Ref
	i[7] - Second Ref
'''


def processFiles():
	'''	This function runs through every file in the GameLogs directory and processes all the data into an array.
		It returns the array and the total number of penalties.
	'''
	penaltyList = []
	allPenalties = []
	totalNumberOfPenalties = 0
	for filename in glob.iglob('GameLogs\*\*.htm'): #This will iterate through every folder and file
		pathway = os.path.dirname(os.path.realpath(filename))
		index_path = pathway.find("GameLogs\\") + len("GameLogs\\") #Figures out the date based on the file structure
		date = pathway[index_path::]
		file = open(filename,"r")
		scan = file.read()

		'''	This section is going to scan the file for the game_string attribute and return the two playing teams.
			The first team in the array will be the AWAY team
			The second team in the array will be the HOME team	
		'''
		game_string = scan.find("game_string: \"") + len("game_string: \"")
		teams = scan[game_string: game_string + scan[game_string::].find("\"")] # Have to add game_string for the same reason as raw_Penalty_Data
		nhl_teams_abbr = [	"ANA","ARI","BOS","BUF","CGY","CAR","CHI","COL","CBJ","DAL",
										"DET","EDM","FLA","LAK","MIN","MTL","NSH","NJD","NYI",
										"NYR","OTT","PHI","PIT","SJS","STL","TBL","TOR","VAN","WSH",
										"WPG"	]
		playingTeams = []
		for i in nhl_teams_abbr:
			if i in teams:
				playingTeams.append(i)

		
		'''	Looking for referees
			Right now the NHL Box Scores only have one reference to referees. I can leverage this to find the officials		
		'''
		location_of_Referees = scan.lower().find("referees")+len("referees: ")
		location_of_Comma = scan[location_of_Referees::].lower().find(",")
		refereesSection = scan[location_of_Referees::]
		first_Ref = refereesSection[0:location_of_Comma]
		end_Of_Refs = refereesSection.lower().find("<")
		second_Ref = refereesSection[(location_of_Comma+2):end_Of_Refs]
		
		
	
		
		'''
			Currently the NHL game data is set up so that Penalty Summary comes above the Stats section.
			The next two lines scan for those key words and the third stores the relevant data into a new variable
			that will be used for further processing.
			
			Note for location_of_Stats: It is important to focus only on the section of the file from penalty summary forward.
			If I don't, then the search would get confused by the menu bar for "Stats"
			
			Note for raw_Penalty_Data: Since the find for location_of_Stats is only looking at a subset, the index is lower than it
			should be, which is why I add location_of_PS to it.
		'''
		location_of_PS = scan.lower().find("penalty summary")
		location_of_Stats = scan[location_of_PS::].lower().find("stats")
		raw_Penalty_Data =  scan[ location_of_PS   :  location_of_Stats+location_of_PS  ]

		
		'''I have no idea why this has to be here... but it does in order for it to work...'''
		GeneralData = []

		class MyHTMLParser(HTMLParser):
			'''This generates an Array with all the HTML elements so I can quickly sort through it.'''	
			def handle_data(self, data):
				GeneralData.append(data)
				
		parser= MyHTMLParser() #Creates an instance of the HTML Parser class
	
		parser.feed(raw_Penalty_Data)
		
		
		'''	How this for loop works is that it will iterate over every piece of data in the array looking for the playingTeams, if it finds it,
			then it knows that the next two elements are the player and the team. This can be assumed since we are trimming the data
			to just the penalty section. From there it adds in whether the player is on the home or away team and weather adds the opponent.
			The home/away and opponent are for later when we sort through the collection of data to build statistics.
		'''
		for i in range(0,len(GeneralData)):
			for team in playingTeams:
				if team in GeneralData[i]:
					penaltyEvent =[]
					penalizedTeam = GeneralData[i]
					penalizedPlayer = GeneralData[i+1]
					
					#To format the penaltyCommitted
					penaltyCommitted = GeneralData[i+2]
					
					'''	This had to be added in the even that a player commits two penalties
						before the stoppage of play. We have to look two data slots to the right
						One Data slot would give you the player who is serving their penalty
					'''
					if "served by" in GeneralData[i+2]:
						penaltyCommitted = GeneralData[i+4]
					
					penaltyCommitted = penaltyCommitted[3::]
					endOfPenalty = penaltyCommitted.find("\n")
					penaltyCommitted = penaltyCommitted[0:endOfPenalty]
					
					#This code has to be introduced because of an error on NHL.com's page for
					#The Edmonton game on 2014-12-31 in which Keith Aulie's penalty is "Keith Aulie"
					if "ith Aulie" not in penaltyCommitted:
						penaltyEvent.append(penalizedTeam)
						penaltyEvent.append(penalizedPlayer)
						penaltyEvent.append(penaltyCommitted)

						
						#This is going to give me a complete list of all the penalties called this season
						if penaltyCommitted not in penaltyList:
							if " (maj)" not in penaltyCommitted:
								penaltyList.append(penaltyCommitted)
						if "rved by" in penaltyCommitted:
							print penalizedPlayer, penalizedTeam, date, filename
						
					
						if penalizedTeam == playingTeams[0]:
							penaltyEvent.append("AWAY")
							penaltyEvent.append(playingTeams[1])
						else:
							penaltyEvent.append("HOME")
							penaltyEvent.append(playingTeams[0])	
						
						penaltyEvent.append(date) #Appends the date to the array for further sorting later
						penaltyEvent.append(first_Ref)
						penaltyEvent.append(second_Ref)

						allPenalties.append(penaltyEvent)
						totalNumberOfPenalties +=1
	print len(allPenalties)
	return allPenalties, totalNumberOfPenalties, penaltyList



def sort_data(desiredSort):
	'''Takes in the dictionaries, creates arrays and sorts them based on the number of infractions'''
	unsorted_data = []
	for l in desiredSort:
		unsorted_data.append([l,desiredSort[l]])
	sorted_data = sorted(unsorted_data, key=lambda x: x[1], reverse=True)
	return sorted_data
	
def playerCounter(penalties):
	'''
		This function creates a dictionary of all the players who have committed a penalty and the number
		times they have.
	'''
	players = {}
	for i in penalties:
		player_name = i[1]
		if player_name != "": #Verifies that the name is not blank
			if player_name in players.keys():
				#Checks to see if the player is already in the list.
				players[player_name]+=1 
			else:
				#If player is not in the list, adds them to the list.
				players[player_name]=1
	return players

def teamCounter(penalties):
	'''
		This function creates a dictionary of all the teams who have committed a penalty and the number
		times they have.
	'''
	teams = {}
	for i in penalties:
		team_name = i[0]
		if team_name != "": #Verifies that the name is not blank
			if team_name in teams.keys():
				#Checks to see if the team is already in the list.
				teams[team_name]+=1 
			else:
				#If team is not in the list, adds them to the list.
				teams[team_name]=1
	return teams

def refCounter(penalties):
	'''
		This function creates a dictionary of all the refs who have called a penalty and the number
		times they have.
	'''
	refs = {}
	for i in penalties:
		ref_name = i[6]
		if ref_name != "": #Verifies that the name is not blank
			if ref_name in refs.keys():
				#Checks to see if the ref is already in the list.
				refs[ref_name]+=1 
			else:
				#If ref is not in the list, adds them to the list.
				refs[ref_name]=1
		ref_name = i[7]
		if ref_name != "": #Verifies that the name is not blank
			if ref_name in refs.keys():
				#Checks to see if the ref is already in the list.
				refs[ref_name]+=1 
			else:
				#If ref is not in the list, adds them to the list.
				refs[ref_name]=1
	return refs

def writeCounter(total,players,teams,refs,desiredPenalty):
	'''
		This function writes all the sorted data to a TXT file
	'''
	fileName = desiredPenalty + "_Counted.txt"
	file = open("Penalties\\" + fileName, 'w')
	file.write("This is the sorted data for the calls involving %s\n\nIt has been called %d times\n\nTeams\n\n" % (desiredPenalty, total))
	for i in teams:
		file.write(i[0] + " - " + str(i[1]) + "\n")
	file.write("\nPlayers\n\n")
	for i in players:
		file.write(i[0] + " - " + str(i[1]) + "\n")
	file.write("\nReferees\n\n")
	for i in refs:
		file.write(i[0] + " - " + str(i[1]) + "\n")
	file.close()
	print "Successful."


def searchForPenalty(desiredPenalty, Penalties):
	'''	This function takes the user's input, parses it through the master Penalty array and moves all the matches into a text document
		formatted to easily publish to Reddit.
		
	'''
	totalTimesCalled = 0
	desiredPenArray = []
	outputFileName = desiredPenalty + ".txt"
	if not os.path.exists("Penalties"):
		os.makedirs("Penalties")
	outputFile = open("Penalties\\" + outputFileName, 'w')
	if len(Penalties) != 0:
		for i in Penalties:
			if desiredPenalty.lower() in i[2].lower():
				totalTimesCalled += 1
				desiredPenArray.append(i)
		outputFile.write("Player's Team | Player Name | Home or Away | Opponent | Date | First Referee | Second Referee  \n---|---|---|---|---|---|---\n")
		for i in desiredPenArray:
			outputFile.write("%s | %s | %s | %s | %s | %s | %s  \n" % (i[0],i[1],i[3],i[4],i[5],i[6],i[7]))
	else:
		print "None Found"
		outputFile.write("None Found")
	outputFile.close()
	return desiredPenArray, totalTimesCalled

def group_penalties(penList):
	groupedList = []
	for i in penList:
		pass

'''All code that does not exist in a function'''	
allPenalties, totalNumberOfPenalties, penaltyList = processFiles()
desiredPenalty = raw_input("Please enter the penalty you are looking for: ")
desiredPenArray, totalTimesCalled = searchForPenalty(desiredPenalty, allPenalties)
desiredPlayers = playerCounter(desiredPenArray)
desiredTeams = teamCounter(desiredPenArray)
desiredRefs = refCounter(desiredPenArray)
writeCounter(totalTimesCalled, sort_data(desiredPlayers),sort_data(desiredTeams),sort_data(desiredRefs),desiredPenalty)