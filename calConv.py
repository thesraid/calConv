#!/usr/bin/env python

"""
thesraid@gmail.com

0.1 Switches, Open File, regex out lines and convert ISO 8601 date
"""

import argparse
import re
import dateutil.parser
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

   args = get_args()

   csv=args.csv

   file = open(args.ics, 'r')
   ics = file.read().strip()
   file.close()

   #print ics

   description = re.search(r'DESCRIPTION:(.*)^CLASS', ics, re.DOTALL|re.MULTILINE)
   location = re.search(r'LOCATION:(.*)', ics)
   organiser = re.search(r'ORGANIZER;CN=(.*):MAILTO', ics)
   dtstart = re.search(r'DTSTART:(.*)', ics)
   dtend = re.search(r'DTEND:(.*)', ics)
   summary = re.search(r'SUMMARY:(.*)', ics)
   print description.group(1)
   print location.group(1)
   print organiser.group(1)
   print summary.group(1)

   startDate = dateutil.parser.parse(dtstart.group(1))
   endDate = dateutil.parser.parse(dtend.group(1))

   print startDate
   print endDate

   
###########################################################################################

""" Start program """
if __name__ == "__main__":
    main()
