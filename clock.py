#!/usr/bin/python

### Librairies

import os
from os import listdir
from os.path import isfile, join

import sys
import time

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
	print("enter -- lunch -- lunch_end -- go")

def readValue(fileName):
	fichier = open(PATH+fileName,"r")

	for line in fichier:
		return line

def verifyFile(filename):
	try:
		with open(PATH+filename): pass
		return True
	except IOError:
		print("Erreur! Le fichier n' pas pu être ouvert")
		return False

def saveFile(string, filename):
	fichier = open(PATH+"day/"+filename, "a")
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

def main(argv):
	
	if argv == "enter":
		
		print("Enter")
		enter = time.perf_counter()
		
		# Save the data into a file named day
		saveFile(str(enter), "day.txt")
		
	elif argv == "go":
		
		if verifyFile("day/day.txt") == True:
			
			if verifyFile("day/lunch.txt") == True:
		
				print("Go out")
				enter = float(readValue("day/day.txt"))
				out = time.perf_counter()
				
				# Calculate time of work
				strtime = displayTime(out-enter)
				print("Work took :", strtime)
				
				# Save the data into a file named date_work.log
				filename = "."+str(date.today())+".log"
				saveFile("Time of work: "+strtime+"\n", filename)
				
				# Erase the file when exiting 
				cleanFile("day.txt")
				
				# If Friday
				d = datetime.date.today()
				if d.weekday() == 4:
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
							print("Total : "+str(result))
							my_file.close()
			
			else:
				print("Lunch not started")
		
		else:
			print("Work not started")
		
	elif argv == "lunch":
	
		if verifyFile("day/day.txt") == True:
			
			print("Lunch start")
			start = time.perf_counter()
			
			# Save the data into a file named lunch
			saveFile(str(start), "lunch.txt")
		
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
				filename = "."+str(date.today())+".log"
				saveFile("Time of lunch: "+strtime+"\n", filename)
				
				# Erase the file when exiting
				cleanFile("lunch.txt")
			
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
		
