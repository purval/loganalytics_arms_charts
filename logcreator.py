#python script: script creates sample log files in pipe seperated form -- date|time|pid|status|data|comment
#for data field it takes random line from sampletext.txt file which has text from http://www.cloudian.com/products/ page

import sys
import datetime
import random
import os
import time
try:
	os.remove('data/logfile.txt')
except OSError:
	pass
try:
	os.remove('js/csvfile.js')
except OSError:
	pass

status = ['OK', 'TEMP', 'PERM']

datafile = open("data/sampletext.txt","rw+")
count_lines = len(datafile.readlines())
datafile.close()

timedifference = datetime.datetime.now()

logfile = open("data/logfile.txt","ab+")
timer = datetime.datetime.utcnow()
#current date
dateV = datetime.datetime.utcnow()
countTEMP = 0
countOK = 0
countPERM = 0
csvfile = open("js/csvfile.js","ab+")
csvfile.write("function generateChartData() { var chartData = [")
csvfile.close()
for num in range(0,9999):
	randomline = random.randint(1, count_lines)
	dataline = ""
	with open("data/sampletext.txt") as f:
	    count = 0
	    for line in f:
		if (count == randomline):
			dataline = line
	    		break
	        count = count + 1	
	#randomly selected status
	statusV = random.choice(status)
	#add 10 seconds to current date and format it to %H:%M:%S
	dateV += datetime.timedelta(seconds=10)
	timeV = dateV.time().strftime("%H:%M:%S")
	#timestamp for js object
	if(statusV == "OK"):
		countOK = countOK + 1
	elif(statusV == "TEMP"):
		countTEMP = countTEMP + 1
	else:
		countPERM = countPERM + 1

	if(int((dateV - timer).seconds)>60):
		timer = dateV
		csvfile = open("js/csvfile.js","ab+")
		writeObj = "{date:"+str(time.mktime(dateV.timetuple())*1000)+",OK:"+str(countOK)+",TEMP:"+str(countTEMP)+",PERM:"+str(countPERM)+"},"
		csvfile.write(writeObj)
		csvfile.close()
		countOK, countTEMP, countPERM = 0,0,0 
	
	writestr = str(dateV.date())+"|"+str(timeV)+"|"+str(random.randint(3000, 5000))+"|"+statusV+"|"+dataline.replace('\n', '')+"|"	 
	while(sys.getsizeof(writestr) < 499):
		writestr += "X"
	writestr += "\n"
	logfile.write(writestr)

logfile.close()	

csvfile = open("js/csvfile.js","ab+")
csvfile.write("];return chartData;}")
csvfile.close()

#reading the each line of the log file and displaying size in bytes
#with open("logfile.txt") as f:
    #for line in f:
	#print sys.getsizeof(line)

#size of the file in bytes
print os.path.getsize("data/logfile.txt")
