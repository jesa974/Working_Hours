#!/usr/bin/python

import os
import sys
import time
from datetime import date

PATH="/home/matthieu/.clock/"
#PATH = /Users/jlprezut/.clock/

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

def main(argv):
	
	if argv == "enter":
		
		print("Enter")
		enter = time.perf_counter()
		
		# Save the data into a file named day
		saveFile(str(enter), "day.txt")
		
	elif argv == "go":
		
		if verifyFile("day.txt") == True:
			
			if verifyFile("lunch.txt") == True:
		
				print("Go out")
				enter = float(readValue("day.txt"))
				out = time.perf_counter()
				
				# Calculate time of work
				strtime = displayTime(out-enter)
				print("Work took :", strtime)
				
				# Save the data into a file named date_work.log
				filename = "."+str(date.today())+".log"
				saveFile("Time of work: "+strtime+"\n", filename)
				
				# Erase the file when exiting 
				#cleanFile("day.txt")
			
			else:
				print("Lunch not started")
		
		else:
			print("Work not started")
		
	elif argv == "lunch":
	
		if verifyFile("day.txt") == True:
			
			print("Lunch start")
			start = time.perf_counter()
			
			# Save the data into a file named lunch
			saveFile(str(start), "lunch.txt")
		
		else:
			print("Work not started")
		
	elif argv == "lunch_end":
		
		if verifyFile("day.txt") == True:
			
			if verifyFile("lunch.txt") == True:

				print("Lunch end")
				start = float(readValue("lunch.txt"))
				finish = time.perf_counter()
				
				# Calculate time of lunch
				strtime = displayTime(finish-start)
				print("Lunch took :", strtime)
				
				# Save the data into a file named date_work.log
				filename = "."+str(date.today())+".log"
				saveFile("Time of lunch: "+strtime+"\n", filename)
				
				# Erase the file when exiting
				#cleanFile("lunch.txt")
			
			else:
				print("Lunch not started")
		
		else:
			print("Work not started")
		
	elif argv == "help":
		
		helpFunction()
		
	else:
		print("Not a valid argument")

if __name__ == "__main__":
	
	if len(sys.argv) == 1:
		print("No argument")
	else:
		# Debugging infos
		#print("Number of arguments:", len(sys.argv)-1, "arguments.")
		#print("Argument List:", str(sys.argv[1:]))
		
		# Main function
		main(sys.argv[1])
		
		
		
		
		
		
		
		
		
