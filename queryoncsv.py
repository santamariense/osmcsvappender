from __future__ import unicode_literals
import csv
from shutil import copyfile
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class csvtable():
  
  # Test CSV file consistency. All the rows have to have the same number os columns
  def hasconsistency(self,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csvfile:
      if csvquotechar:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter)
      csvisvalid = True
      csvheader = next(spamreader)
      for row in spamreader:
        if not (len(row) == len(csvheader)):
          csvisvalid = False
      return csvisvalid 

  # Test CSV file consistency. The tag/field used to join CSV to OSM need be a primary key
  def canbepk(self,key,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csvfile:
      if csvquotechar:
        spamDictReader = csv.DictReader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamDictReader = csv.DictReader(csvfile, delimiter=csvdelimiter)
      pklist = []
      for row in spamDictReader: # Creates a primary key list
        pklist.insert(len(pklist),row[key])
      pkexclusivity = True
      for item in pklist:
        if pklist.count(item) > 1: # To guarantee consistency it can't there be reapeted primary keys in the list
          pkexclusivity = False
      return pkexclusivity 

  # Test if there is a specific key in the table
  def columnexists(self,key,csvfilename,csvdelimiter,csvquotechar):
    with open (csvfilename,'rb') as csvfile:
     if csvquotechar:
       spamreader = csv.reader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
     else:
       spamreader = csv.reader(csvfile, delimiter=csvdelimiter)
     csvheader = next(spamreader)
     if key in csvheader:
       return True
     else:
       return False

  def getalltagsof(self,key,value,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csvfile:
      if csvquotechar:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter)
      key = key.encode('utf-8')
      value = value.encode('utf-8')
      taglist = []
      # Get primary key column index   
      header = spamreader.next()
      headersize = len(header)
      i = 0
      pkindex = 0
      for column in header:
        if ( column == key ):
          pkindex = i
        i += 1
      valueslist = []
      for row in spamreader:
        if ( row[pkindex] == value ):
          valueslist = row
      if ( valueslist != [] ):
        for i in range(headersize):
          taglist.append([header[i],valueslist[i]])
      return taglist

  def getfieldsname(self,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csvfile:
      if csvquotechar:
        spamDictReader = csv.DictReader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamDictReader = csv.DictReader(csvfile, delimiter=csvdelimiter)
      i = spamDictReader.next()
      fieldsname = [row for row in i]
      try:fieldsname.remove('osmfullid')
      except: pass
    return fieldsname

  def countcharinfile(self,char,csvfilename):
    csvfile = open(csvfilename,'r')
    countchar = 0
    for line in csvfile:
      countchar += line.count(char)
    csvfile.close()
    return countchar

  def likelydelimiter(self,csvfilename,csvdelimiter,csvquotechar):
    delimiterlist = [',',';',':','\t',' ','|']
    probdelimiter = ''
    charoccurrence = 0
    for delimiter in delimiterlist:
      if ( self.countcharinfile(delimiter,csvfilename) > charoccurrence ):
        charoccurrence = self.countcharinfile(delimiter,csvfilename)
        probdelimiter = delimiter
    return probdelimiter

  def likelyquotechar(self,csvfilename,csvdelimiter,csvquotechar):
    quotecharlist = ["'",'"','`']
    probquotechar = ''
    charoccurrence = 0
    for quotechar in quotecharlist:
      if ( self.countcharinfile(quotechar,csvfilename) > charoccurrence ):
        charoccurrence = self.countcharinfile(quotechar,csvfilename)
        probquotechar = quotechar
    return probquotechar

  def copyCSVfile (self, timenow, outputdirectory ,csvfilename,csvdelimiter,csvquotechar):
    csvfilename_copy = outputdirectory + os.path.splitext(os.path.basename(csvfilename))[0] + "_osmcsvappender_" + timenow + ".csv"
    copyfile(csvfilename,csvfilename_copy)
    return csvfilename_copy
    
  def adjustCSVlogfile (self,primarykey,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csv_in, open(csvfilename+'.tmp','wb') as csv_out:
      if csvquotechar:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter, quotechar=csvquotechar)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter)  
      # Get primary key column index   
      header = spamreader.next()
      headersize = len(header)
      i = 0
      for column in header:
        i += 1
        if ( column == primarykey ):
          pkindex = i
      # Create a new file without removed columns
      spamwriter.writerow([primarykey,'total_updated','node_updated','way_updated','relation_updated'])
      for row in spamreader:
        del row[0:pkindex-1]
        del row[1:(headersize-(pkindex-1))]
        spamwriter.writerow([row[0],'0','0','0','0'])
      # Move data from tmp to main file
      ready2delete = False
      while ( ready2delete == False ): ready2delete = os.access(csvfilename,os.W_OK)
      os.remove(csvfilename)
      os.rename(csvfilename+".tmp",csvfilename)
      
  def modifyCSVLine(self,newlinevalues,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csv_in, open(csvfilename+'.tmp','wb') as csv_out:
      if csvquotechar:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter, quotechar=csvquotechar)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter)
      for row in spamreader:
        if ( row[0] == newlinevalues [0] ):
          spamwriter.writerow(newlinevalues)
        else:
          spamwriter.writerow(row)
      # Move data from tmp to main file
      ready2delete = False
      while ( ready2delete == False ): ready2delete = os.access(csvfilename,os.W_OK)
      os.remove(csvfilename)
      os.rename(csvfilename+".tmp",csvfilename)     
      
  def CSVsummation(self,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csv_in, open(csvfilename+'.tmp','wb') as csv_out:
      if csvquotechar:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter, quotechar=csvquotechar)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csv_in, delimiter=csvdelimiter)
        spamwriter = csv.writer(csv_out, delimiter=csvdelimiter)
      total = 0
      nodes = 0
      ways = 0
      relations = 0
      i = 0
      for row in spamreader:
        spamwriter.writerow(row)
        if ( i > 0 ):
          total += int(row[1])
          nodes += int(row[2])
          ways += int(row[3])
          relations += int(row[4])
        i += 1
      spamwriter.writerow(['total',total,nodes,ways,relations]) 
      # Move data from tmp to main file
      ready2delete = False
      while ( ready2delete == False ): ready2delete = os.access(csvfilename,os.W_OK)
      os.remove(csvfilename)
      os.rename(csvfilename+".tmp",csvfilename)  

  def getcellvalueof(self,language,text_id,csvfilename,csvdelimiter,csvquotechar):
    with open(csvfilename,'rb') as csvfile:
      if csvquotechar:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter, quotechar=csvquotechar)
      else:
        spamreader = csv.reader(csvfile, delimiter=csvdelimiter)
      language = language
      text_id = text_id
      cellvalue = ''
      # Get primary key column index   
      header = spamreader.next()
      headersize = len(header)
      i = 0
      langindex = 0
      for column in header:
        if ( column == language ):
          langindex = i
        i += 1
      j = 0
      txt_idindex = 0
      for column in header:
        if ( column == 'txt_id' ):
          txt_idindex = j
        j += 1
      for row in spamreader:
        if ( row[txt_idindex] == text_id ):
          cellvalue = row[langindex]
      return cellvalue





