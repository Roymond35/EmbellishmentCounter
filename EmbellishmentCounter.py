import xlrd,os,time

def print_data(players,teams,ps,ts,username):
	'''Prints the newly created data into the file.
	players is the dictionary of players with recorded infractions
	teams is the dictionary of teams with recorded infractions
	ps is the sorted player list (Sorted on the number of infractions, most on top)
	ts is the sorted team list, similar to PS	
	'''
	EC = "EmbellishmentCount.txt" # This is where all the scores are stored.
	files = open(EC,'w')
	
	#Writes out the list of players, sorted by number of infractions
	last_updated = "Last updated on " + time.strftime("%c", time.localtime()) + "\n\n"
	files.write(last_updated)
	files.write("Players who have been called for Embellishment\n\n")
	for key in ps:
		files.write(key[0] + " - " + str(key[1]) + "\n")
		
	#Writes out list of teams, sorted by number of infractions
	files.write("\n\n\nTeams Sorted\n\n")
	for key in ts:
		files.write(key[0] + " - " + str(key[1]) + "\n")

	
	#Closes the file.
	files.close
	print "The program was successfully ran on " + time.strftime("%c", time.localtime())

	
def sort_data(players,teams):
	'''Takes in the dictionaries, creates arrays and sorts them based on the number of infractions'''
	unsorted_players = []
	unsorted_team=[]
	for k in players:
		player_team = k + " - " + players[k][0]
		unsorted_players.append([player_team,players[k][1]])
	#Called to sort the array by the second term
	sorted_players = sorted(unsorted_players, key=lambda x: x[1], reverse=True)
	for l in teams:
		unsorted_team.append([l,teams[l]])
	sorted_teams = sorted(unsorted_team, key=lambda x: x[1], reverse=True)
	return sorted_players,sorted_teams
	

	
def main():
	os.system('cls')
	players = {}
	teams = {}
	#Establishes user numbers. This could probably be reworked
	username = os.getenv("username")
	filename = "Embellishment.xlsx"
	book = xlrd.open_workbook(filename);
	sh = book.sheet_by_index(0) #This is the line that sets the first sheet.
	for rx in range(1,sh.nrows):
		player_name = sh.cell_value(rowx=rx,colx=0)
		team_name = sh.cell_value(rowx=rx,colx=1)
		if player_name != "": #Verifies that the name is not blank
			if player_name in players.keys():
				#Checks to see if the player is already in the list.
				players[player_name][1]+=1 
			else:
				#If player is not in the list, adds them to the list.
				players[player_name]=[]
				players[player_name].append(team_name)
				players[player_name].append(1)
			if team_name in teams.keys():
				teams[team_name]+=1
			else:
				teams[team_name]=1

	#Sorts the player data.
	players_sorted,teams_sorted = sort_data(players,teams)
	
	#Prints the file.
	print_data(players,teams,players_sorted,teams_sorted, username)
	
		
main()
		