#!/usr/bin/python

### Librairies

import os
from os import listdir
from os.path import isfile, join
import fnmatch

import sys
import time

import datetime
from datetime import date, datetime, timedelta

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr

### Class

EMAIL_HTML_TEMPLATE="""<html>
                  <head>
                  </head>
                  <body>
                    <p style ="margin: 5px 0;line-height: 25px;">Bonjour {},<br>
                    <br>
                    Ceci est un mail au format html.
                    <br>
                    {}
                    <br>
                    Bien à vous,<br>
                    {} <br>
                    </p>
                  </body>
                </html>
                """

class EmailSenderClass:
	def __init__(self):
		""" """
		self.logaddr = "test@gmail.com"
		self.fromaddr = "contact@domaine.com"# alias
		self.password = ""#
		
	def sendMessageViaServer(self,toaddr,msg):
		# Send the message via local SMTP server.
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(self.logaddr, self.password)
		text = msg.as_string()
		server.sendmail(self.fromaddr, toaddr, text)
		server.quit()
				
	def sendHtmlEmailTo(self,destName,destinationAddress,msgBody):
		#Message setup
		msg = MIMEMultipart()
		
		msg['From'] =  "Me<"+self.fromaddr+">"
		msg['To'] = destinationAddress
		msg['Subject'] = "Hello mail"
		
		hostname=sys.platform
		
			
		txt = EMAIL_HTML_TEMPLATE
		
		txt=txt.format(destName,msgBody,hostname)
		
		#Add text to message
		msg.attach(MIMEText(txt, 'html'))
		
		print("Send email from {} to {}".format(self.fromaddr,destinationAddress))
		self.sendMessageViaServer(destinationAddress,msg)


### Functions

PATH = os.path.expanduser('~/.clock/')
# UBUNTU PATH = "/home/pseudo/.clock/"
# MAC PATH = /Users/pseudo/.clock/


def displayTime(seconds):
	if seconds >= 3600:
	
		return time.strftime('%H h %M min %S s', time.gmtime(int(seconds)))
	
	elif seconds >= 60:
	
		return time.strftime('%M min %S s', time.gmtime(int(seconds)))
	
	else:
		return time.strftime('%S s', time.gmtime(int(seconds)))

def helpFunction():
	print("HELP")
	print("Valid arguments :")
	print("enter -- break -- break_end -- lunch -- lunch_end -- go")

def verifyParity(value):
	# Calculate the parity
	result = value % 2
	if(result == 0):
		# It is pair
		return 0
	else:
		# It is not pair
		return 1

def cleanBreaks():
	# Init cpt value to 1
	cpt = 1

	# Count the number of break
	num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*'))
	
	# Cleaning break file
	while cpt != num_break:
		cleanFile(PATH+'day/break'+str(cpt)+'.txt')
		cpt = cpt + 1

	# Count the number of end_break
	num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'end_break*'))
	
	# Cleaning end_break file
	while cpt != num_break:
		cleanFile(PATH+'day/end_break'+str(cpt)+'.txt')
		cpt = cpt + 1

def calculateBreaks():
	# Init total value to 0
	total = 0

	# Init cpt value to 1
	cpt = 1

	# Count the number of break
	num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'end_break*'))

	# Calculate total time of breaks
	while cpt != num_break:
		total = total + readValue(PATH+'day/end_break'+str(cpt)+'.txt')
	
	return total

def readValue(fileName):
	fichier = open(PATH+fileName,"r")

	for line in fichier:
		return line

def readHour(fileName):
	fichier = open(PATH+fileName,"r")

	for line in fichier:
		fields = line.split(':')
		return int(fields[0])
		
def readRate(fileName):
	fichier = open(PATH+fileName,"r")

	for line in fichier:
		fields = line.split(':')
		return float(fields[1])
		
def readMargin(fileName):
	fichier = open(PATH+fileName,"r")

	for line in fichier:
		fields = line.split('=')
		return float(fields[1])

def verifyFile(filename):
	try:
		with open(PATH+filename): pass
		return True
	except IOError:
		print("Erreur! Le fichier n' pas pu être ouvert")
		return False

def saveFile(string, filename):
	fichier = open(PATH+filename, "a")
	fichier.write(string)
	fichier.close()

def cleanFile(fileName):
	try:
		os.remove(PATH+fileName)
	except OSError as e:
		print(e)
	else:
		print("File is deleted successfully")

def recupFields(file):
	lunch = 0
	work = 0
	nb = 0
	
	for line in file:
		total = 0
		# Delete new line
		line = line.strip()
		print(line)
		# Separate the line
		fields = line.split(':')
		
		# Convert into seconds
		if "h" in fields[1]:
			hours = fields[1].split('h')
			#print("H : "+hours[0])
			total = total + (int(hours[0].strip()) *60 *60)
			
			if "min" in hours[1]:
				min = hours[1].split("min")
				#print("Min : "+min[0])
				total = total + (int(min[0].strip()) *60)
				
				if "s" in min[1]:
					seconds = min[1].split('s')
					#print("S : "+seconds[0])
					total = total + (int(seconds[0].strip()))
		
		elif "min" in fields[1]:
			min = fields[1].split("min")
			#print("Min : "+min[0])
			total = total + (int(min[0].strip()) *60)
			
			if "s" in min[1]:
				seconds = min[1].split('s')
				#print("S : "+seconds[0])
				total = total + (int(seconds[0].strip()))
			
		else:
			seconds = fields[1].split('s')
			#print("S : "+seconds[0])
			total = total + (int(seconds[0].strip()))
		
		if nb == 0:
			lunch = total
			nb = nb + 1
		else:
			work = total
		
	# Return result
	return work - lunch

def writeMargin(margin, supp):
	
	total = readMargin("margin.conf")
	
	if supp == True:
		total = total + (margin/60)
	else:
		total = total - (margin/60)
	
	fichier = open(PATH+"margin.conf","w")
	
	fichier.write("Total = "+total)
	
	fichier.close()

def compHours(seconds):
	hours = readHour('clock.conf')*60
	total = (seconds / 60) / 60

	if seconds < hours:
		
		# Prevention message
		msg = "It miss you: " + displayTime(hours-total)
		
		# Send mail
		email= EmailSenderClass()
		email.sendHtmlEmailTo("Admin","email@email.com",msg)
		
		# Register margin
		writeMargin(hours-total, True)
		
	elif seconds > hours:
		
		# Prevention message
		msg = "You got: " + displayTime(total-hours) + " more"
		
		# Send mail
		email= EmailSenderClass()
		email.sendHtmlEmailTo("Admin","email@email.com",msg)
		
		# Register margin
		writeMargin(total-hours, False)
		
	else:
		# Prevention message
		msg = "You got: " + displayTime(total-hours) + " more"
		
		# Send mail
		email= EmailSenderClass()
		email.sendHtmlEmailTo("Admin","")
		# TODO
	

def main(argv):
	
	if argv == "enter":
		
		print("Enter")
		enter = time.perf_counter()
		
		# Save the data into a file named day
		saveFile(str(enter), "day/day.txt")
		
	elif argv == "go":
		
		if verifyFile("day/day.txt") == True:
			
			if verifyFile("day/lunch.txt") == True:
				
				if len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*')) != 0:
				
					if verifyParity(len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*'))) == 0:
						
						print("Breaks taken today")
						total_break = calculateBreaks()
						strtime = displayTime(total_break)
						print("Breaks took :", strtime)

						# Save the data into a file named date_work.log
						filename = "day/."+str(date.today())+".log"
						saveFile("Time of breaks: "+strtime+"\n", filename)

						print("Go out")
						enter = float(readValue("day/day.txt"))
						out = time.perf_counter()
						
						# Calculate time of work
						strtime = displayTime(out-enter)
						print("Work took :", strtime)
						
						# Save the data into a file named date_work.log
						filename = "day/."+str(date.today())+".log"
						saveFile("Time of work: "+strtime+"\n", filename)
						
						# Erase the file when exiting 
						cleanFile("day/day.txt")
						cleanFile("day/lunch.txt")
						cleanBreaks()
						
						# If Friday
						d = date.today()
						if d.weekday() == 4:
							total = 0
							fichiers = [f for f in listdir(PATH+'day/') if isfile(join(PATH+'day/', f))]
							for fichier in fichiers:
								if fichier != ".DS_Store":
									# Print Name file
									print(fichier)
									# Read file
									my_file = open(PATH+'day/'+fichier, "r")
									# Get data 
									result = recupFields(my_file)
									total = total + result
									print("Total : "+str(result))
									my_file.close()
							print("Total hours for this week : "+displayTime(total))
							
							# Save the data into a file named week_work.log
							filename = "week/."+str(datetime.now().isocalendar()[1])+".log"
							saveFile("Time of work for this week: "+displayTime(total)+"\n", filename)
							
							# Make the review
							compHours(total)
					
					else:
						print("Break not ended")

				else:

					print("No Break taken")

					print("Go out")
					enter = float(readValue("day/day.txt"))
					out = time.perf_counter()
					
					# Calculate time of work
					strtime = displayTime(out-enter)
					print("Work took :", strtime)
					
					# Save the data into a file named date_work.log
					filename = "day/."+str(date.today())+".log"
					saveFile("Time of work: "+strtime+"\n", filename)
					
					# Erase the file when exiting 
					cleanFile("day/day.txt")
					cleanFile("day/lunch.txt")
					
					# If Friday
					d = date.today()
					if d.weekday() == 4:
						total = 0
						my_dir = os.path.expanduser('~/.clock/day/')
						week_dir = os.path.expanduser('~/.clock/week/')
						fichiers = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
						for fichier in fichiers:
							if fichier != ".DS_Store":
								# Print Name file
								print(fichier)
								# Read file
								my_file = open(my_dir+fichier, "r")
								# Get data 
								result = recupFields(my_file)
								total = total + result
								print("Total : "+str(result))
								my_file.close()
						print("Total hours for this week : "+displayTime(total))
						
						# Save the data into a file named week_work.log
						filename = "week/."+str(datetime.now().isocalendar()[1])+".log"
						saveFile("Time of work for this week: "+displayTime(total)+"\n", filename)
						
						# Make the review
						compHours(total)
			
			else:
				print("Lunch not started")
		
		else:
			print("Work not started")
	
	elif argv == "break":
		
		if verifyFile("day/day.txt") == True:
			
			print("Break start")
			start = time.perf_counter()
			
			# Count the number of break
			num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*'))
			
			# Increment the number of break
			if num_break == 0:
				num_break = 1
			else:
				num_break = num_break + 1
			
			# Save the data into a file named break
			saveFile(str(start), "day/break"+str(num_break)+".txt")
		
		else:
			print("Work not started")
	
	elif argv == "break_end":
		
		if verifyFile("day/day.txt") == True:
			
			if len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*')) != 0:
				
				if verifyParity(len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*'))) == 1:

					# Count the number of break
					num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'break*'))

					print("Break end")
					start = float(readValue("day/break"+str(num_break)+".txt"))
					finish = time.perf_counter()
					
					# Calculate time of break
					strtime = displayTime(finish-start)
					print("Break took :", strtime)
					
					# Count the number of break
					num_break = len(fnmatch.filter(os.listdir(PATH+'day/'), 'end_break*'))

					# Increment the number of break
					if num_break == 0:
						num_break = 1
					else:
						num_break = num_break + 1

					# Save the data into a file named end_break
					saveFile(str(strtime), "day/end_break"+str(num_break)+".txt")

				else:
					print("Break not started")
			
			else:
				print("Break not started")
		
		else:
			print("Work not started")

	elif argv == "lunch":
	
		if verifyFile("day/day.txt") == True:
			
			print("Lunch start")
			start = time.perf_counter()
			
			# Save the data into a file named lunch
			saveFile(str(start), "day/lunch.txt")
		
		else:
			print("Work not started")
		
	elif argv == "lunch_end":
		
		if verifyFile("day/day.txt") == True:
			
			if verifyFile("day/lunch.txt") == True:

				print("Lunch end")
				start = float(readValue("day/lunch.txt"))
				finish = time.perf_counter()
				
				# Calculate time of lunch
				strtime = displayTime(finish-start)
				print("Lunch took :", strtime)
				
				# Save the data into a file named date_work.log
				filename = "day/."+str(date.today())+".log"
				saveFile("Time of lunch: "+strtime+"\n", filename)
			
			else:
				print("Lunch not started")
		
		else:
			print("Work not started")
		
	elif argv == "help":
		
		helpFunction()
		
	else:
		print("Not a valid argument")
		
	

### Main

if __name__ == "__main__":
	
	if len(sys.argv) == 1:
		print("No argument")
	else:
		# Debugging infos
		#print("Number of arguments:", len(sys.argv)-1, "arguments.")
		#print("Argument List:", str(sys.argv[1:]))
		
		# Main function
		main(sys.argv[1])
		
