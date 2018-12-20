#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
thesraid@gmail.com

0.1 Switches, Open File, regex out lines and convert ISO 8601 date
0.2 write to CSV in correct format
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
This starts everything
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

   csvFile = open(args.csv, 'w+')
   csvFile.write("Event Venue Name,Event Organizer Name,Event Name,Event Start Date,Event Start Time,Event End Date,Event Description,Timezone,tag\n")


   reg = re.compile(r'BEGIN:VEVENT(.*?(?=))END:VEVENT', re.DOTALL|re.MULTILINE)
   for block in re.finditer(reg, ics):
      reg = re.compile(r'DTSTAMP:(.*)LAST-MODIFIED:(.*)CREATED:(.*)SEQUENCE:(.*)ORGANIZER;CN=(.*):MAILTO(.*)DTSTART:(.*)DTEND:(.*)UID:(.*)SUMMARY:(.*)LOCATION:(.*?(?=))URL:(.*)DESCRIPTION:(.*?(?=))CLASS:(.*)STATUS:(.*)PARTSTAT:(.*)', re.DOTALL|re.MULTILINE)
      for out in re.finditer(reg, block.group(1)):
         '''
         print out.group(1).replace('\n','') # DTSTAMP
         print out.group(2).replace('\n','') # LAST-MODIFIED:
         print out.group(3).replace('\n','') # CREATED:
         print out.group(4).replace('\n','') # SEQUENCE:
         print out.group(5).replace('\n','') # ORGANIZER
         print out.group(6).replace('\n','') # MAILTO
         print out.group(7).replace('\n','') # DTSTART
         print out.group(8).replace('\n','') # DTEND
         print out.group(9).replace('\n','') # UID
         print out.group(10).replace('\n','') # SUMMARY
         print out.group(11).replace('\n','') # LOCATION
         print out.group(12).replace('\n','') # URL
         print (((out.group(13).replace('\n','')).replace('\\n','')).replace('\r ','')).replace('\\','') # DESCRIPTION
         print out.group(14).replace('\n','') # CLASS
         print out.group(15).replace('\n','') # STATUS
         print out.group(16).replace('\n','') # PARTSTAT
         '''
         csvFile.write((out.group(11).replace('\n','').replace(',', ''))  + ',') # LOCATION
         csvFile.write((out.group(5).replace('\n','').replace(',', '')) + ',') # ORGANIZER
         csvFile.write((out.group(10).replace('\n','').replace(',', '')) + ',') # SUMMARY
         csvFile.write((out.group(7).replace('\n','').replace(',', '')) + ',') # DTSTART
         csvFile.write((out.group(7).replace('\n','').replace(',', '')) + ',') # DTSTARTTIME
         csvFile.write((out.group(8).replace('\n','').replace(',', '')) + ',') # DTEND
         csvFile.write((((out.group(13).replace('\n ','').replace(',', ''))).replace('\\n','')).replace('\\','') + ',') # DESCRIPTION
         csvFile.write(",Europe/Dublin,Ireland\n")

   csvFile.close()

         
###########################################################################################

""" Start program """
if __name__ == "__main__":
    main()
