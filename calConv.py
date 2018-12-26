#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
thesraid@gmail.com
"""

import argparse # Used to read in arguments from the command line
import re # Used to write regular expressions to match patterns in the ics file
import dateutil.parser # Used to convert the date format
import datetime # Used to extract the date and time seperately from the date
from subprocess import call # Used to run Operating SYstem commands
###########################################################################################
"""
Get command line args from the user.
"""
def get_args():
    parser = argparse.ArgumentParser(
        description='ICS and CSV details')

    parser.add_argument('-i', '--ics',
                        required=True,
                        action='store',
                        help='ICS file location')

    parser.add_argument('-c', '--csv',
                        required=True,
                        action='store',
                        help='CSV file location')

    args = parser.parse_args()

    return args

###########################################################################################

"""
Main module
"""
def main():

   # Get the arguments from the command line using the get_args function above
   args = get_args()
  
   # Run dos2unix to get rid of windows crap
   call(["dos2unix", "-q", args.ics])

   # Open the ics file, read it's contents to ics then close the file
   icsFile = open(args.ics, 'r')
   ics = icsFile.read().strip()
   icsFile.close()

   # Open the csv file fir writing
   csvFile = open(args.csv, 'w+')
   # Write the column headings
   csvFile.write("Event Venue Name,Event Organizer Name,Event Name,Event Start Date,Event Start Time,Event End Date,Event Description,Timezone\n")

   # Search for any text that exists beween BEGIN:VEVENT and END:VEVENT using a regular expression
   # Add all of the search results to "reg"
   reg = re.compile(r'BEGIN:VEVENT(.*?(?=))END:VEVENT', re.DOTALL|re.MULTILINE)
   # FOr each result (called block) in reg
   for block in re.finditer(reg, ics):
      # Search the text that comes after DTSTAMP and add it to group1, search for the text after LAST-MODIFIED and add it to groups 2 etc.
      reg = re.compile(r'DTSTAMP:(.*)LAST-MODIFIED:(.*)CREATED:(.*)SEQUENCE:(.*)ORGANIZER;CN=(.*):MAILTO(.*)DTSTART:(.*)DTEND:(.*)UID:(.*)SUMMARY:(.*)LOCATION:(.*?(?=))URL:(.*)DESCRIPTION:(.*?(?=))CLASS:(.*)STATUS:(.*)PARTSTAT:(.*)', re.DOTALL|re.MULTILINE)
      for out in re.finditer(reg, block.group(1)):

         # Grab the dates from group 7 & 8
         # Convert the date to standard date
         start = dateutil.parser.parse(out.group(7))
         end = dateutil.parser.parse(out.group(8))

         # Extract the date and time from the dates
         # Convert the dates to the format the calendar app wants. 
         startDate = start.strftime('%Y-%m-%d')
         endDate = end.strftime('%Y-%m-%d')
         startTime = start.strftime('%H:%M:%S')
         endTime = end.strftime('%H:%M:%S')

         # Write the other stuff in the correct order replacing newlines, commas and other stuff that will confuse the calendar app, with spaces and nothing
         csvFile.write(((((out.group(11).replace('\n ','').replace(',', ''))).replace('\\n',' ')).replace('\\','')).replace('\n','') + ',') # LOCATION
         csvFile.write(((((out.group(5).replace('\n ','').replace(',', ''))).replace('\\n',' ')).replace('\\','')).replace('\n','') + ',') # ORGANIZER
         csvFile.write(((((out.group(10).replace('\n ','').replace(',', ''))).replace('\\n',' ')).replace('\\','')).replace('\n','') + ',') # SUMMARY
         csvFile.write(startDate + ',') # DTSTART
         csvFile.write(startTime + ',') # DTSTARTTIME
         csvFile.write(endDate + ',') # DTEND
         csvFile.write(((((out.group(13).replace('\n ','').replace(',', ''))).replace('\\n',' ')).replace('\\','')).replace('\n','') + ',') # DESCRIPTION
         csvFile.write("Europe/Dublin\n")

   # CLose the CSV file
   csvFile.close()

         
###########################################################################################

""" Start program """
if __name__ == "__main__":
    main()
