'''
	This code is to grab the boxscore HTML file for every game that happened the previous night
	It is going to be using the following modules:
		urllib - To open the desired webpages, read them or save them to disk.
		os - To create the directories corresponding to the correct date.

	This program was written by Roy W. Gero.
	If you have questions, comments or concerns please contact him on GitHub
'''
import urllib,os

#The desired webpage to see all the games that happened the previous day.
desiredWebsite = urllib.urlopen("http://www.nhl.com/ice/scores.htm")
websiteData = desiredWebsite.read()

#Looking at the source code, I can see a reference to the current date after the "datepicker" query.
#Using this I can get the date and format it in a way that is consistent with my other folders. (YYYY-MM-DD)
dateStart = websiteData.find("jQuery.datepicker.parseDate('mm/dd/yy',")+len("jQuery.datepicker.parseDate('mm/dd/yy', '")
dateEnd = websiteData[dateStart::].find("');")+dateStart
date = websiteData[dateStart:dateEnd]
dateFormat = date[len(date)-4::] + "-" + date[0:2] + "-" + date[3:5]

games = [] # Creates a blank array to store the boxscore URLs found on the page.

#This is a simple search through the webpage's HTML. It relies on the fact that there will be at least one game.
found = 0
while found!=-1:
	'''	After inspecting the HTML of the source page, I can see that every boxscore is a simple HTML link
		From this, I can easily find each instance of a boxscore link and the URL by finding the word "BOXSCORE"
		and then looking at the data backwards to find the start of the link tag.
	'''
	found = websiteData.find("\">BOXSCORE")
	startOfLink = websiteData[found:0:-1].find("\"=ferh")
	if found!=-1:
		gameURL = websiteData[found-startOfLink+1:found]
		games.append(gameURL)
	websiteData = websiteData[found+1::] #Have to offset found by one so the search doesn't repeat itself

folder = "GameLogs\\" + dateFormat #The destined folder to save the filter
if len(games)!=0 and not os.path.exists(folder): #Makes sure the folder does not exist. If it does, this doesn't run.
	counter = 0
	os.makedirs(folder) #Makes the directory for storing the files.
	for i in games:
		counter +=1
		location = "GameLogs\\" + dateFormat + "\\" +  str(counter) + ".htm"
		urllib.urlretrieve(i,location) #Downloads the file to the correct directory
else:
	print "This already potentially ran. Check the folder"