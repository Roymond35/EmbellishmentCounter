from HTMLParser import HTMLParser
import glob,os

GeneralData=[] #This is all the data fields stored from the HTML File
totalNumberOfPenalties = 0 #Just for a pure curiousity I am keeping track of this.
lastRan = ""
allPenalties = [] #Creating a Master Array that will store all the game penalties. This can be used to sort later.

'''Temporary Embellishment Code'''
Embellishments = []
embellishmentFile = open("Embellishment_Test.txt",'w')


class MyHTMLParser(HTMLParser):
	def handle_data(self, data):
		GeneralData.append(data)
		
parser= MyHTMLParser() #Creates an instance of the HTML Parser class

while True: #Temporarily disabling so the file gets generated new every time
	'''try:
		storingFiles = open("Penalties - 2014-15 Season.txt",'a')
		previouslyRan = linecache.getline("Penalties - 2014-15 Season.txt",1")
		print previouslyRan
		break	
	except NameError:'''
	storingFiles = open("Penalties - 2014-15 Season.txt",'w')
	storingFiles.write("Penalties in the 2014-15 Season\n\n")
	break		

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

	GeneralData=[] #This is all the data fields stored from the HTML File

	parser.feed(raw_Penalty_Data)
	
	storingFiles.write(date +" - %s at %s \n\n" % (playingTeams[0],playingTeams[1])); #This puts the date and game everywhere appropriate
	
	gamePenalties = [] # Clears this array so we are ONLY getting the penalties from that game.
	
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
				penaltyCommitted = penaltyCommitted[3::]
				endOfPenalty = penaltyCommitted.find("\n")
				penaltyCommitted = penaltyCommitted[0:endOfPenalty]
				
				penaltyEvent.append(penalizedTeam)
				penaltyEvent.append(penalizedPlayer)
				penaltyEvent.append(penaltyCommitted)
			
				if penalizedTeam == playingTeams[0]:
					penaltyEvent.append("AWAY")
					penaltyEvent.append(playingTeams[1])
				else:
					penaltyEvent.append("HOME")
					penaltyEvent.append(playingTeams[0])	
				
				penaltyEvent.append(date) #Appends the date to the array for further sorting later
				
				gamePenalties.append(penaltyEvent)
				allPenalties.append(penaltyEvent)
				totalNumberOfPenalties +=1

	
	'''	Once the program has looked through all the relevant data from the file, it writes it to the txt file. It is formatted in a way to easily
		search through later or publish to reddit.
	'''
	for i in gamePenalties:
		storingFiles.write("%s | %s | %s | %s | %s\n" % (i[0],i[1],i[2],i[3],i[4]))
	storingFiles.write("\n\n")

storingFiles.close()

def searchForPenalty(desiredPenalty, Penalties):
	'''	This function takes the user's input, parses it through the master Penalty array and moves all the matches into a text document
		formatted to easily publish to Reddit.
		
	'''
	desiredPenArray = []
	outputFileName = desiredPenalty + ".txt"
	outputFile = open(outputFileName, 'w')
	if len(gamePenalties) != 0:
		for i in Penalties:
			if desiredPenalty.lower() in i[2].lower():
				desiredPenArray.append(i)
		outputFile.write("Player's Team | Player Name | Home or Away | Opponent | Date  \n---|---|---|---|---\n")
		for i in desiredPenArray:
			outputFile.write("%s | %s | %s | %s | %s  \n" % (i[0],i[1],i[3],i[4],i[5]))
	else:
		print "None Found"
		outputFile.write("None Found")
	outputFile.close()
	
desiredPenalty = raw_input("Please enter the penalty you are looking for: ")
searchForPenalty(desiredPenalty, allPenalties)
