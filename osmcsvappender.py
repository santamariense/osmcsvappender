#!/usr/bin/env python2.7
import sys
import os
from queryoncsv import csvtable ###
import ast
from osmfileREbuilder  import *    ###

def createLogFile(results, osmfs, csvfs, opdir, csvd, csvq, matchtl, matchg, importf, pk, ow):
    logfile =  opdir + "osmcsvappender_" + results[0] + ".log"
    counter = csvtable().getalltagsof(pk,'total',results[2],csvd,csvq)
    tcounter = counter[1][1]
    ncounter = counter[2][1]
    wcounter = counter[3][1]
    rcounter = counter[4][1]
    if ( ow == True ):
      ow = 'Overwrite with CSV file values'
    else:
      ow = 'Keep original values in OSM file'
    if ( pk == 'osmfullid' ): pk = '"Object ID on OSM"'
    geomtxt = '|'
    for geom in matchg:
      geomtxt += geom+'|'
    matchg = geomtxt
    mtltxt = '|'
    for key, value in matchtl:
      mtltxt += key+'='+value+'|'
    matchtl = mtltxt
    impttxt = '|'
    for fieds in importf:
      impttxt += fieds+'|'
    importf = impttxt  
    txt = []
    txt.append('---------------------------- OSM CSV Appender usage LOG FILE ----------------------------'+'\n')
    txt.append('> '+'Input information...'+'\n')
    txt.append('  >> '+'OSM File: ' + osmfs + ' \n')
    txt.append('  >> '+'CSV File: ' + csvfs + ' \n')
    txt.append('> '+'Settings and variables...' + '\n')
    txt.append('  >> '+'CSV delimiter: ' + csvd + '\n')
    txt.append('  >> '+'CSV quote char: ' + csvq + '\n')
    txt.append('  >> '+'Selected geometries: ' + matchg + '\n')
    txt.append('  >> '+'Selected geometries in OSM file need to match the following tags: ' + matchtl + '\n')
    txt.append('  >> '+'Selected keys/fields to be imported from CSV file: ' + importf + '\n')
    txt.append('  >> '+'Selected key/field to be used as primary key to join files data: '+pk+'\n')
    txt.append('  >> '+'Selected option in case of confliting keys/fields between files: '+ow+'\n')
    txt.append('> '+'Output information...'+'\n')
    txt.append('  >> '+'Directory with generated files: ' + opdir + ' \n')
    txt.append('  >> '+'OSM File with the result of appending: ' + results[1] + ' \n')
    txt.append('  >> '+'CSV File with statistics of appending: ' + results[2] + ' \n')
    txt.append('  >> '+'Log file (this one): ' + logfile + ' \n')
    txt.append('> '+'Final result... '+'\n')
    txt.append('  >> '+tcounter+' objects modified: '+'('+ncounter+' nodes, '+wcounter+' ways and '+rcounter+' relations)'+'\n' )
    txt.append('-----------------------------------------------------------------------------------------'+'\n')    
    logtxt = ''
    for item in txt:
      logtxt += item
    f = open(logfile, 'w')
    f.write(logtxt)
    f.close
    return logfile

def doappend(osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow):
    if ( ow == 'True' ): ow = True
    if ( ow == 'False' ): ow = False 
    if ( csvq == 'none' ): csvq = ''
    hasconsistency = csvtable().hasconsistency(csvfs,csvd,csvq)
    canbepk = csvtable().canbepk(pk,csvfs,csvd,csvq)
    if ( hasconsistency ):
      if ( canbepk ):
        #try:
          results = inserttagsto(osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
          logfile = createLogFile(results,osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
          whatever = raw_input('Files succefully generated. Use the hashtag #osmcsvappender in changeset comment to help us to track application usage and possible errors.\n Type Enter Key to see LOG FILE')
          logfile = open(logfile,'r')
          logfiletxt = ''
          for line in logfile:
            print line
          logfile.close
        #except:
          print 'One or more error was found. Type --help to get some help.'
      else:
        print '"%s" can not be used as primary key because there are rows with repeated values.' %pk
    else:
      print 'Error: CSV file - All the rows have to have the same number of columns.\nMake sure to select the correct delimiter and quote char.'



helptxt = '''

OSM CSV Appender - HELP

0 - osmcsvappender.py
1 - ----
1.1 - --version : Command to get version
1.2 - --help : Command to get help
1.3 - --cmdln : Pass arguments by command line
1.4 - --tint : Open terminal interface
2 - --cmdln osmfs : osmfs is the full path to OSM file. Example: /home/me/file.osm
3 - --cmdln osmfs csvfs : csvfs is the full path to CSV file. Exemple:  /home/me/file.csv
4 - --cmdln osmfs csvfs opdir : opdir is the full path to directory where generated files will be saved. Example: /home/output/
5 - --cmdln osmfs csvfs opdir csvd : csvd is the delimiter used to separate columns in CSV file
6 - --cmdln osmfs csvfs opdir csvd csvq : csvq is the quote char used in CSV file. For empty value type none
7 - --cmdln osmfs csvfs opdir csvd csvq matchtl: matchtl is the list of tags that a geometry in OSM file need to have to get new fields from CSV file. Examples of values: [] - [['key','value']] - [['key1','*'],['key2','value2']] ...
8 - --cmdln osmfs csvfs opdir csvd csvq matchtl matchg: matchg is the geometry list that is able to get CSV file new fields. The values can be node, way or/and relation. Examples: way - node,relation - ['way','node','relation']
9 - --cmdln osmfs csvfs opdir csvd csvq matchtl matchg importf: importf is the list of fields to be importer from CSV file. Examples: ['field1','field2','field7','field4']
10 - --cmdln osmfs csvfs opdir csvd csvq matchtl matchg importf pk: pk is the field to be used for joining CSV data with OSM one. Example: 'amenity' - 'osmfullid' (to use OSM geometry full id, example of values on CSV file: r987654, n67834, w348987)
11 - --cmdln osmfs csvfs opdir csvd csvq matchtl matchg importf ow: ow is short for "overwrite". What to do if OSM file already has the field that will be imported from CSV? Type True to overwrite or False to keep original OSM file values.

Example of a simple case with solution using --cmdln command:

 > To update the population and source:population tags of all places nodes, joining CSV to OSM by a fictional id tag called QSYU:NKMHGID...
  >> Solution: --cmdln "/home/myfolder/places.osm" "/home/myfolder/poptable.csv" "/home/myfolder/" ";" "none" "[['place','*']]" "['node']" "['population','source:population']" "QSYU:NKMHGID" "True"

Visit https://wiki.openstreetmap.org/wiki/OSM_CSV_Appender for full information
'''

argv_len = len(sys.argv) - 1 # argv indexes
smthgdone = False

if ( argv_len == 0 ):
  try:
    os.system('python gui.pyc')
    smthgdone = True
  except:
    try:
      os.system('python2 gui.pyc')
      smthgdone = True
    except:
      try:
        os.system('python2.7 gui.pyc')
        smthgdone = True
      except: 
        print "Impossible to run OSM CSV Appender in graphic mode"


if ( argv_len == 1 ):
  if ( sys.argv[1] == '--version' ):
    print 'OSM CSV Appender - Version 1.0'
    smthgdone = True
  if ( sys.argv[1] == '--help' ):
    print helptxt
    smthgdone = True
  if ( sys.argv[1] == '--cmdln' ):
    print 'Using OSM CSV Appender in command line. Type --help for get some help.'
  if ( sys.argv[1] == '--tint' ):
    print '\nUsing OSM CSV Appender on terminal interface. Type --help for get some help.\n'
    osmfs = raw_input('Step (1/10) - OSM file full path: ')
    csvfs = raw_input('Step (2/10) - CSV file full path: ')
    opdir = raw_input('Step (3/10) - Output directory full path: ')
    csvd = raw_input('Step (4/10) - CSV delimiter: ')
    csvq = raw_input('Step (5/10) - CSV quote char (for empty value type none): ')
    matchtl = ast.literal_eval(raw_input('Step (6/10) - All tags in OSM files need to match: '))
    matchg = ast.literal_eval(raw_input('Step (7/10) - Geometries to apply changes: '))
    importf = ast.literal_eval(raw_input('Step (8/10) - List of fields to import: '))
    pk = raw_input('Step (9/10) - Field to join CSV to OSM file: ')
    ow = raw_input('Step (10/10) - Overwrite values? (True or False): ')
    doappend(osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
    smthgdone = True

if ( argv_len == 11 and sys.argv[1] == '--cmdln' ):
  osmfs = sys.argv[2]
  csvfs = sys.argv[3]
  opdir = sys.argv[4]
  csvd = sys.argv[5]
  csvq = sys.argv[6]
  matchtl = ast.literal_eval(sys.argv[7])
  matchg = ast.literal_eval(sys.argv[8])
  importf = ast.literal_eval(sys.argv[9])
  pk = sys.argv[10]
  ow = sys.argv[11]
  doappend(osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
  #print type(osmfs), type(csvfs), type(opdir), type(csvd), type(csvq), type(matchtl), type(matchg), type(importf), type(pk), type(ow)
  #print matchtl #,matchg,importf,pk,ow
  smthgdone = True

if ( not smthgdone ):
  print 'Whoops! Something has gone wrong. No operation realized. Type --help to get some help.'


