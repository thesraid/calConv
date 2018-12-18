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
   
   # Need to clean the file first to get rid of messy charecters, multi-line entries
   # Cut up the file into smaller chunks
   # Regex each file

   # Then big regex with loads of groups goes here.

   # BEGIN:VEVENT\sDTSTAMP(.*)\sLAST-MODIFIED:(.*)\sCREATED:(.*)\sSEQUENCE:(.*)\sORGANIZER;CN=(.*):MAILTO(.*)\sDTSTART:(.*)\sDTEND:(.*)\sUID:(.*)\sSUMMARY:(.*)\sLOCATION(.*[\S\s]*?(?=))\sURL:(.*)\sDESCRIPTION:(.*[\s\S]*?(?=))CLASS:(.*)\sSTATUS:(.*)\sPARTSTAT:(.*)\sEND:VEVENT

   reg = re.compile(r'BEGIN:VEVENT.*DTSTAMP:(.*)LAST-MODIFIED:(.*)CREATED:(.*)SEQUENCE:(.*)ORGANIZER;CN=(.*):MAILTO(.*)DTSTART:(.*)DTEND:(.*)UID:(.*)SUMMARY:(.*)LOCATION:(.*?(?=))URL:(.*)DESCRIPTION:(.*?(?=))CLASS:(.*)STATUS:(.*)PARTSTAT:(.*)END:VEVENT', re.DOTALL|re.MULTILINE)
   for out in re.finditer(reg, ics):
      print out.group(1).replace('\n','')
      print out.group(2).replace('\n','')
      print out.group(3).replace('\n','')
      print out.group(4).replace('\n','')
      print out.group(5).replace('\n','')
      print out.group(6).replace('\n','')
      print out.group(7).replace('\n','')
      print out.group(8).replace('\n','')
      print out.group(9).replace('\n','')
      print out.group(10).replace('\n','')
      print out.group(11).replace('\n','')
      print out.group(12).replace('\n','')
      print (((out.group(13).replace('\n','')).replace('\\n',' ')).replace('\r ','')).replace('\\','')
      print out.group(14).replace('\n','')
      print out.group(15).replace('\n','')
      print out.group(16).replace('\n','')

   '''
   out = re.search(r'BEGIN:VEVENT.*DTSTAMP:(.*)LAST-MODIFIED:(.*)CREATED:(.*)SEQUENCE:(.*)ORGANIZER;CN=(.*):MAILTO(.*)DTSTART:(.*)DTEND:(.*)UID:(.*)SUMMARY:(.*)LOCATION:(.*?(?=))URL:(.*)DESCRIPTION:(.*?(?=))CLASS:(.*)STATUS:(.*)PARTSTAT:(.*)END:VEVENT', ics, re.DOTALL|re.MULTILINE)
   print out.group(1)
   print out.group(2)
   print out.group(3)
   print out.group(4)
   print out.group(5)
   print out.group(6)
   print out.group(7)
   print out.group(8)
   print out.group(9)
   print out.group(10)
   print out.group(11)
   print out.group(12)
   print out.group(13)
   print out.group(14)
   print out.group(15)
   print out.group(16)
   '''

   # Used regex to search through the file to match the follow patterns. Then save the result
   # Everything in the brackets (.*) represents text that we want to save. It will automatically be saved as group 1
   # TO see the result you need to run print result.group(1) to show just the data in group 1
   #description = re.search(r'DESCRIPTION:(.*)^CLASS', ics, re.DOTALL|re.MULTILINE)
   #descOneLine = description.group(1).replace('\n','')
   #descNewLine = descOneLine.replace('\\n',' ')
   #print(descNewLine.replace('\r ',''))

   
###########################################################################################

""" Start program """
if __name__ == "__main__":
    main()
