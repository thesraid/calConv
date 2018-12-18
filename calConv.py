#!/usr/bin/env python

"""
thesraid@gmail.com

0.1 Switches, Open File, regex out lines and convert ISO 8601 date
0.2 write to CSV in correct format
"""

import argparse # Used to read in arguments from the command line
import re # Used to write regular expressions to match patterns in the ics file
import dateutil.parser # Used to convert the date format
import datetime # Used to extract the date and time seperately from the date
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

   # Open the ics file, read it's contents to ics then close the file
   icsFile = open(args.ics, 'r')
   ics = icsFile.read().strip()
   icsFile.close()

   # Used regex to search through the file to match the follow patterns. Then save the result
   # Everything in the brackets (.*) represents text that we want to save. It will automatically be saved as group 1
   # TO see the result you need to run print result.group(1) to show just the data in group 1
   description = re.search(r'DESCRIPTION:(.*)^CLASS', ics, re.DOTALL|re.MULTILINE)
   location = re.search(r'LOCATION:(.*)', ics)
   organiser = re.search(r'ORGANIZER;CN=(.*):MAILTO', ics)
   dtstart = re.search(r'DTSTART:(.*)', ics)
   dtend = re.search(r'DTEND:(.*)', ics)
   summary = re.search(r'SUMMARY:(.*)', ics)

   # Convert the date to standard date
   start = dateutil.parser.parse(dtstart.group(1))
   end = dateutil.parser.parse(dtend.group(1))

   # Extract the date and time from the dates
   startDate = start.strftime('%Y-%m-%d')
   endDate = end.strftime('%Y-%m-%d')
   startTime = start.strftime('%H:%M:%S')
   endTime = end.strftime('%H:%M:%S')

   # Write the above data to a CSV file using the approprate column names
   # https://theeventscalendar.com/knowledgebase/csv-files-options-and-examples

   # Open the csv file, write to it then close the file
   # group(1) is used for the regex results to write only the data in group 1 (.*)
   # The replace option removes stupid winodws return chars
   csvFile = open(args.csv, 'w+')
   csvFile.write("Event Venue Name,Event Organizer Name,Event Name,Event Start Date,Event Start Time,Event End Date,Event Description,Timezone,tag\n")
   # This should be in a loop reading from a matrix or something maybe
   csvFile.write(location.group(1).replace('\r',''))
   csvFile.write(",")
   csvFile.write(organiser.group(1).replace('\r',''))
   csvFile.write(",")
   csvFile.write(summary.group(1).replace('\r',''))
   csvFile.write(",")
   csvFile.write(startDate.replace('\r',''))
   csvFile.write(",")
   csvFile.write(startTime.replace('\r',''))
   csvFile.write(",")
   csvFile.write(endDate.replace('\r',''))
   csvFile.write(",")
   # Need to do some work to nicelt format the description date
   descOneLine = description.group(1).replace('\n','')
   descNewLine = descOneLine.replace('\\n',' ')
   csvFile.write(descNewLine.replace('\r ',''))
   csvFile.write(",Europe/Dublin,Ireland\n")
   # Need to add this stuff to pad out the end as the import on the site is buggy
   
   csvFile.close()
 

   
###########################################################################################

""" Start program """
if __name__ == "__main__":
    main()
