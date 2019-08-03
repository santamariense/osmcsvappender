# encoding: utf-8
from __future__ import unicode_literals
from queryoncsv import csvtable ###
from osmfileREbuilder  import *    ###
from PyQt5.QtWidgets import QListWidget, QFileDialog, QDialog

from PyQt5 import QtWidgets, uic 
 
import sys
import os
import datetime

# Main UI
class Ui(QtWidgets.QMainWindow):

  # Global variables
  osmfilename = ''
  csvfilename = ''
  csvdelimiter = ''
  csvquotechar = ''
  geomselect = []
  directory = ''

  def __init__(self):
    super(Ui, self).__init__()
    uic.loadUi('main.ui', self)
    self.show()

    try: 
      self.loadlanguages()
      self.changeAppLanguageto('English')
    except: pass

    self.lstwgSelGeomTypes.setSelectionMode(QListWidget.MultiSelection)
    geometries = ['node','way','relation']
    self.lstwgSelGeomTypes.insertItem(0,"node")
    self.lstwgSelGeomTypes.insertItem(1,"way")
    self.lstwgSelGeomTypes.insertItem(2,"relation")
    self.lstwgSelGeomTypes.selectAll()

    #self.statusbar.showMessage("OSM CSV Appender",20000)

    self.stckedwMain.setCurrentIndex(0)

    self.frmPlus.setAutoFillBackground(True)
    self.frmPlus.hide()

    self.pshbtnChangeParam.hide()
    self.pshbtnChangeParam = self.findChild(QtWidgets.QPushButton, 'pshbtnChangeParam')
    self.pshbtnChangeParam.clicked.connect(self.changeParam)

    self.pshbtnPlus = self.findChild(QtWidgets.QPushButton, 'pshbtnPlus')
    self.pshbtnPlus.clicked.connect(self.plusBtnHit)

    self.pshbtnSelOSMf = self.findChild(QtWidgets.QPushButton, 'pshbtnSelOSMf')
    self.pshbtnSelOSMf.clicked.connect(self.getOSMfile)

    self.tblTags2match.horizontalHeader().setStretchLastSection(True) 

    self.pshbtnSelCSVf = self.findChild(QtWidgets.QPushButton, 'pshbtnSelCSVf')
    self.pshbtnSelCSVf.clicked.connect(self.getCSVfile)

    self.chkbxAllGeom = self.findChild(QtWidgets.QCheckBox, 'chkbxAllGeom')
    self.chkbxAllGeom.clicked.connect(self.selectallgeometries)

    self.rdbtGeomid = self.findChild(QtWidgets.QRadioButton, 'rdbtGeomid')
    self.rdbtGeomid.toggled.connect(self.fieldchosen)

    self.rdbtField = self.findChild(QtWidgets.QRadioButton, 'rdbtField')
    self.rdbtField.toggled.connect(self.fieldchosen)

    self.pshbtnTestCSV = self.findChild(QtWidgets.QPushButton, 'pshbtnTestCSV')
    self.pshbtnTestCSV.clicked.connect(self.testCSVloadFields)

    self.pshbtnDismiss = self.findChild(QtWidgets.QPushButton, 'pshbtnDismiss')
    self.pshbtnDismiss.clicked.connect(self.dismissCSVmsg)

    self.chkbxAllFields = self.findChild(QtWidgets.QCheckBox, 'chkbxAllFields')
    self.chkbxAllFields.clicked.connect(self.selectallfields)

    self.pshbtnFindFolder = self.findChild(QtWidgets.QPushButton, 'pshbtnFindFolder')
    self.pshbtnFindFolder.clicked.connect(self.selectFolder)

    self.pshbtnAppend = self.findChild(QtWidgets.QPushButton, 'pshbtnAppend')
    self.pshbtnAppend.clicked.connect(self.joinCSVintoOSM)

    self.pshbtnUseAgain = self.findChild(QtWidgets.QPushButton, 'pshbtnUseAgain')
    self.pshbtnUseAgain.clicked.connect(self.useAgain)

    self.pshbtnClose = self.findChild(QtWidgets.QPushButton, 'pshbtnClose')
    self.pshbtnClose.clicked.connect(self.closeApp)

    self.cbLanguage = self.findChild(QtWidgets.QComboBox, 'cbLanguage')
    self.cbLanguage.currentIndexChanged.connect(self.languageSelector)

  def languageSelector(self):
    # Get language value from cbLanguage
    langname = self.cbLanguage.currentText()
    self.changeAppLanguageto(langname)

  def gt(self,t): #Get text from a specific language in CSV list
    currlang = (self.cbLanguage.currentText()).encode('utf-8')
    l = currlang
    celltext = csvtable().getcellvalueof(l,t,'languages.csv',str(';'),str('"'))
    return celltext

  def changeAppLanguageto(self,lang):
    l = lang
    self.lblOSMFile.setText(self.gt('TXT002'))
    self.pshbtnSelOSMf.setText(self.gt('TXT003'))
    self.gbOSMFilters.setTitle(self.gt('TXT004'))
    self.lblSelectGeomTypes.setText(self.gt('TXT005'))
    self.chkbxAllGeom.setText(self.gt('TXT006'))
    self.lblTags2match.setText(self.gt('TXT007'))
    self.lblCSVFile.setText(self.gt('TXT008'))
    self.pshbtnSelCSVf.setText(self.gt('TXT009'))
    self.gbCSV.setTitle(self.gt('TXT010'))
    self.pshbtnChangeParam.setText(self.gt('TXT011'))
    self.lblDelimiter.setText(self.gt('TXT012'))
    self.lblQtchar.setText(self.gt('TXT013'))
    self.lblJoinby.setText(self.gt('TXT014'))
    self.rdbtGeomid.setText(self.gt('TXT015'))
    self.rdbtField.setText(self.gt('TXT016'))
    self.pshbtnTestCSV.setText(self.gt('TXT017'))
    self.lblFieds2Import.setText(self.gt('TXT018'))
    self.chkbxAllFields.setText(self.gt('TXT019'))
    self.gbReady2go.setTitle(self.gt('TXT020'))
    self.pshbtnFindFolder.setText(self.gt('TXT021'))
    self.lblOvrQuestion.setText(self.gt('TXT022'))
    self.rdbtnKeep.setText(self.gt('TXT023'))
    self.rdbtnOvwr.setText(self.gt('TXT024'))
    self.lblLanguage.setText(self.gt('TXT025'))
    self.lblWikiOSM.setText(self.gt('TXT026'))
    self.lblDevby.setText(self.gt('TXT027'))
    self.lblLicense.setText(self.gt('TXT028'))
    self.lblVersion.setText(self.gt('TXT029'))
    self.lblCSVFileErrors.setText(self.gt('TXT030'))
    self.pshbtnDismiss.setText(self.gt('TXT031'))
    self.lblReady.setText(self.gt('TXT032'))
    self.lblAppending.setText(self.gt('TXT033'))
    self.lblFileList.setText(self.gt('TXT034'))
    self.lblTrackErrors.setText(self.gt('TXT035'))
    self.pshbtnUseAgain.setText(self.gt('TXT036'))
    self.pshbtnClose.setText(self.gt('TXT037'))
    self.lblfeedb.setText(self.gt('TXT038'))
    self.pshbtnAppend.setText(self.gt('TXT039'))


  def plusBtnHit(self):
    if ( self.pshbtnPlus.text() == '+' ):
      self.pshbtnPlus.setText('-')
      self.frmPlus.show()
    else:
      self.pshbtnPlus.setText('+')
      self.frmPlus.hide()

  def loadlanguages(self):
    if ( self.cbLanguage.currentText() == '' ):
      langlist = csvtable().getfieldsname('languages.csv',str(';'),str('"'))
      self.cbLanguage.clear()
      try:
        langlist.remove('txt_id')
        langlist.remove('widgetid')
        langlist.remove('active')
        langlist.remove('translatable')
        langlist.remove('nativeapptext')
      except: pass
      i = 0
      for lang in langlist:
        self.cbLanguage.insertItem(i,lang)
      i += 1
      self.cbLanguage.setCurrentText('English')

  def joinCSVintoOSM(self):
    self.stckedwMain.setCurrentIndex(2)
    osmfs = self.osmfilename
    csvfs = self.csvfilename
    opdir = self.directory
    csvd = self.csvdelimiter
    csvq = self.csvquotechar
    matchtl = []
    for i in range(10):
      try : matchtl_k = self.tblTags2match.item(i,0).text()
      except: matchtl_k = ''
      try : matchtl_v = self.tblTags2match.item(i,1).text()
      except: pass
      if ( matchtl_v == '' ): matchtl_v = '*'
      if ( matchtl_k != '' ):
        matchtl.append([matchtl_k.encode('utf-8'),matchtl_v.encode('utf-8')])
    matchg = [item.text().encode('utf-8') for item in self.lstwgSelGeomTypes.selectedItems()]
    importf = [item.text().encode('utf-8') for item in self.lstwgFields2import.selectedItems()]
    if ( self.rdbtGeomid.isChecked() ):
      pk = 'osmfullid'
    else:
      pk = self.cbFieldPK.currentText()
    ow = self.rdbtnOvwr.isChecked()
    # Generate output files
    timebefore = filter(str.isdigit, str(datetime.datetime.now()))[10:]
    results = inserttagsto(osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
    timeafter = filter(str.isdigit, str(datetime.datetime.now()))[10:]
    timeofexecution = str(( float(timeafter) - float(timebefore) ) / 1000000) + 's'
    results.append(timeofexecution)
    logfile = self.createLogFile(results,osmfs,csvfs,opdir,csvd,csvq,matchtl,matchg,importf,pk,ow)
    self.lblFileListOSM.setText(' - '+os.path.basename(results[1]))
    self.lblFileListCSV.setText(' - '+os.path.basename(results[2]))
    self.lblFileListLog.setText(' - '+'osmcsvappender_'+results[0]+'.log')
    logfile = open(logfile,'r')
    self.pltxtLog.clear()
    for line in logfile:
      self.pltxtLog.insertPlainText(line)
    logfile.close
    counter = csvtable().getalltagsof(pk,'total',results[2],csvd,csvq)
    tcounter = counter[1][1]
    ncounter = counter[2][1]
    wcounter = counter[3][1]
    rcounter = counter[4][1]
    summarizedstats = tcounter + self.gt('TXT040') +ncounter+ self.gt('TXT041') +wcounter+ self.gt('TXT042') +rcounter+ self.gt('TXT043')
    self.lblStatSumm.setText(summarizedstats)

  def createLogFile(self, results, osmfs, csvfs, opdir, csvd, csvq, matchtl, matchg, importf, pk, ow):
    logfile =  self.directory + "osmcsvappender_" + results[0] + ".log"
    counter = csvtable().getalltagsof(pk,'total',results[2],csvd,csvq)
    tcounter = counter[1][1]
    ncounter = counter[2][1]
    wcounter = counter[3][1]
    rcounter = counter[4][1]
    if ( ow == True ):
      ow = self.gt('TXT044')
    else:
      ow = self.gt('TXT045')
    if ( pk == 'osmfullid' ): pk = self.gt('TXT046')
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
    # Write log file
    f = open(logfile, 'w')
    f.write('---------------------------- ')
    f.write(self.gt('TXT047'))
    f.write(' ----------------------------'+'\n')
    f.write('> ')
    f.write(self.gt('TXT048'))
    f.write('\n')
    f.write('  >> ')
    f.write(self.gt('TXT049'))
    f.write(osmfs + ' \n')
    f.write('  >> ')
    f.write(self.gt('TXT050'))
    f.write(csvfs + ' \n')
    f.write('> ')
    f.write(self.gt('TXT051'))
    f.write('\n')
    f.write('  >> ')
    f.write(self.gt('TXT052'))
    f.write(csvd + '\n')
    f.write('  >> ')
    f.write(self.gt('TXT053'))
    f.write(csvq + '\n')
    f.write('  >> ')
    f.write(self.gt('TXT054'))
    f.write(matchg + '\n')
    f.write('  >> ')
    f.write(self.gt('TXT055'))
    f.write(matchtl + '\n')
    f.write('  >> ')
    f.write(self.gt('TXT056'))
    f.write(importf + '\n')
    f.write('  >> ')
    f.write(self.gt('TXT057'))
    f.write(pk+'\n')
    f.write('  >> ')
    f.write(self.gt('TXT058'))
    f.write(ow+'\n')
    f.write('> ')
    f.write(self.gt('TXT059'))
    f.write('\n')
    f.write('  >> ')
    f.write(self.gt('TXT060'))
    f.write(self.directory + ' \n')
    f.write('  >> ')
    f.write(self.gt('TXT061'))
    f.write(results[1] + ' \n')
    f.write('  >> ')
    f.write(self.gt('TXT062'))
    f.write(results[2] + ' \n')
    f.write('  >> ')
    f.write(self.gt('TXT063'))
    f.write(logfile + ' \n')
    f.write('> ')
    f.write(self.gt('TXT064'))
    f.write('\n')
    f.write('  >> '+tcounter)
    f.write(self.gt('TXT065'))
    f.write('('+ncounter)
    f.write(self.gt('TXT066'))
    f.write(wcounter)
    f.write(self.gt('TXT067'))
    f.write(rcounter)
    f.write(self.gt('TXT068'))    
    f.write('\n')
    f.write('  >> ')
    f.write(self.gt('TXT076'))
    f.write(results[3])
    f.close
    return logfile

  def getOSMfile(self):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName = QFileDialog.getOpenFileName(self,self.gt('TXT069'), "","OSM File (*.osm);OSM File (*.OSM)", options=options)
    fileName = fileName[0].encode("utf-8")
    if ( fileName != '' ):
      self.osmfilename = fileName
      self.lblSelOSMf.setText(os.path.basename(self.osmfilename))
      self.OSMFileChosen(True)
    else:
      self.osmfilename = ''
      self.lblSelOSMf.setText(self.osmfilename)
      self.OSMFileChosen(False)


  def getCSVfile(self,csvfilename):
    self.resetParam(1)
    # Open file dialog
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fileName = QFileDialog.getOpenFileName(self,self.gt('TXT070'), "","CSV File (*.csv);CSV File (*.CSV)", options=options)
    fileName = fileName[0].encode("utf-8")
    if ( fileName != '' ):
      self.csvfilename = fileName
      self.lblSelCSVf.setText(os.path.basename(self.csvfilename))
      self.resetParam(2)
    else:
      self.CSVFileChosen(False)
      self.csvfilename = ''
      self.lblSelCSVf.setText(self.csvfilename)


  def fieldchosen(self):
    self.pshbtnTestCSV.setEnabled(True)
    if (self.rdbtGeomid.isChecked()):
      self.lblOfi.setEnabled(True)
      self.cbFieldPK.setEnabled(False)
    else:
      self.lblOfi.setEnabled(False)
      self.cbFieldPK.setEnabled(True)
     

  def testCSVloadFields(self):
    errorslist = []
    csvhasconsistency = csvtable().hasconsistency(self.csvfilename,self.csvdelimiter,self.csvquotechar)
    if not csvhasconsistency: errorslist.append('1')
    if (self.rdbtGeomid.isChecked()):
      selectfieldcanbepk = csvtable().canbepk('osmfullid',self.csvfilename,self.csvdelimiter,self.csvquotechar)
    else:
      selectfieldcanbepk = csvtable().canbepk(str(self.cbFieldPK.currentText()),self.csvfilename,self.csvdelimiter,self.csvquotechar)
    if not selectfieldcanbepk: errorslist.append('2')
    if ( csvhasconsistency and selectfieldcanbepk ):
      self.CSVFileTested(True)
      ## Load fields into lstwgFields2import
      self.lstwgFields2import.setSelectionMode(QListWidget.MultiSelection)
      fieldsname = csvtable().getfieldsname(self.csvfilename,self.csvdelimiter,self.csvquotechar)
      try: fieldsname.remove(self.cbFieldPK.currentText())
      except: pass
      i = 0
      for field in fieldsname:
        self.lstwgFields2import.insertItem(i,field)
        i += 1
    else: # Show message box with errors
      self.pltxtCSVErrors.clear()
      self.pltxtCSVErrors.insertPlainText(self.gt('TXT071'))
      self.pltxtCSVErrors.insertPlainText('\n')
      for error in errorslist:
        if ( error == '1' ):
          self.pltxtCSVErrors.insertPlainText(self.gt('TXT072'))
          self.pltxtCSVErrors.insertPlainText('\n')
        if ( error == '2' ):
          self.pltxtCSVErrors.insertPlainText(self.gt('TXT073'))
          self.pltxtCSVErrors.insertPlainText('\n\n')
      self.pltxtCSVErrors.insertPlainText(self.gt('TXT074'))
      self.pltxtCSVErrors.insertPlainText('\n')
      self.stckedwMain.setCurrentIndex(1)

  def dismissCSVmsg(self):
    self.stckedwMain.setCurrentIndex(0)

  def selectallfields(self):
    if ( self.chkbxAllFields.isChecked() ):
      self.lstwgFields2import.selectAll()

  def selectallgeometries(self):
    if ( self.chkbxAllGeom.isChecked() ):
      self.lstwgSelGeomTypes.selectAll()
      self.lstwgSelGeomTypes.setEnabled(False)
    else:
      self.lstwgSelGeomTypes.setEnabled(True)


  def selectFolder(self):
    # Open directory dialog
    directory = QFileDialog.getExistingDirectory(self,self.gt('TXT075'))
    directory = directory
    if ( directory != '' ):
      self.directory = directory + "/"
      self.lblFindFolder.setText(self.directory)
      self.pshbtnAppend.setEnabled(True)
    else:
      self.directory = ''
      self.lblFindFolder.setText(self.directory)
      self.pshbtnAppend.setEnabled(False)
    

  def resetParam(self,paramid):
    if ( paramid == 1):
      ## Clear possible cbFieldPK and lstwgFields2import items set before
      self.cbFieldPK.clear()
      self.lstwgFields2import.clear()
      ## Clear possible lnedDelimiter and lnedQtchar items set before
      self.lnedDelimiter.setText('')
      self.lnedQtchar.setText('')  
      ## Uncheck rdbtGeomid and rdbtField
      self.rdbtGeomid.setAutoExclusive(False)
      self.rdbtGeomid.setChecked(False)
      self.rdbtGeomid.setAutoExclusive(True)
      self.rdbtField.setAutoExclusive(False)
      self.rdbtField.setChecked(False)
      self.rdbtField.setAutoExclusive(True)
    if ( paramid == 2):
      self.CSVFileChosen(True)
      # rdbtGeomid only will be enabled if osmfullid exists on csv
      # Fill delimiter and quotechar and save their values to a variable
      self.lnedDelimiter.setText(csvtable().likelydelimiter(self.csvfilename,self.csvdelimiter,self.csvquotechar))
      self.lnedQtchar.setText(csvtable().likelyquotechar(self.csvfilename,self.csvdelimiter,self.csvquotechar))
      self.csvdelimiter = str(self.lnedDelimiter.text())
      self.csvquotechar = str(self.lnedQtchar.text())
      ##
      osmfullidexists = csvtable().columnexists('osmfullid',self.csvfilename,self.csvdelimiter,self.csvquotechar)
      self.rdbtGeomid.setEnabled(osmfullidexists)
      ## Load (new) fields into cbFieldPK
      fieldsname = csvtable().getfieldsname(self.csvfilename,self.csvdelimiter,self.csvquotechar)
      i = 0
      for field in fieldsname:
        self.cbFieldPK.insertItem(i,field)
        i += 1
      

  def OSMFileChosen(self,tf):
    self.gbOSMFilters.setEnabled(tf)
    self.chkbxAllGeom.setEnabled(tf)
    self.tblTags2match.setEnabled(tf)
    self.lblSelectGeomTypes.setEnabled(tf)
    self.lblTags2match.setEnabled(tf)
    if ( self.lstwgFields2import.isEnabled() ):
      self.gbReady2go.setEnabled(tf)
      if ( self.directory != '' ):
        self.pshbtnAppend.setEnabled(tf)

  def CSVFileChosen(self,tf):
    self.pshbtnChangeParam.hide()
    self.gbCSV.setEnabled(tf)
    self.lblDelimiter.setEnabled(tf)
    self.lblQtchar.setEnabled(tf)
    self.lnedDelimiter.setEnabled(tf)
    self.lnedQtchar.setEnabled(tf)
    self.lblJoinby.setEnabled(tf)
    self.rdbtGeomid.setEnabled(tf)
    self.rdbtField.setEnabled(tf)
    if ( tf == False ):
      self.lblOfi.setEnabled(tf)
      self.cbFieldPK.setEnabled(tf)
      self.pshbtnTestCSV.setEnabled(tf)
      self.lblFieds2Import.setEnabled(tf)
      self.chkbxAllFields.setEnabled(tf)
      self.lstwgFields2import.setEnabled(tf)
      self.gbReady2go.setEnabled(tf)
      if ( self.directory != '' ):
        self.pshbtnAppend.setEnabled(tf)
    if not ( self.rdbtGeomid.isChecked() and self.rdbtField.isChecked() ):
      self.pshbtnTestCSV.setEnabled(False)
      self.cbFieldPK.setEnabled(False)
      
  def CSVFileTested(self,tf):
    # Enable fields to import
    self.lblFieds2Import.setEnabled(tf)
    self.chkbxAllFields.setEnabled(tf)
    self.lstwgFields2import.setEnabled(tf)
    if ( self.gbOSMFilters.isEnabled() ):
      self.gbReady2go.setEnabled(tf)
      if ( self.directory != '' ):
        self.pshbtnAppend.setEnabled(tf)
    # Disable parameters
    self.pshbtnChangeParam.show()
    self.lblDelimiter.setEnabled(not tf)
    self.lblQtchar.setEnabled(not tf)
    self.lnedDelimiter.setEnabled(not tf)
    self.lnedQtchar.setEnabled(not tf)
    self.lblJoinby.setEnabled(not tf)
    self.rdbtGeomid.setEnabled(not tf)
    self.rdbtField.setEnabled(not tf)
    self.lblOfi.setEnabled(not tf)
    self.pshbtnTestCSV.setEnabled(not tf)
    self.cbFieldPK.setEnabled(not tf)
    

  def changeParam(self):
    self.pshbtnChangeParam.hide()
    self.resetParam(1)
    self.resetParam(2)
    self.lblFieds2Import.setEnabled(False)
    self.chkbxAllFields.setEnabled(False)
    self.lstwgFields2import.setEnabled(False)
    self.gbReady2go.setEnabled(False)
    self.pshbtnAppend.setEnabled(False)
    
  def useAgain(self):
    self.stckedwMain.setCurrentIndex(0)
    
  def closeApp(self):
    self.close()
    
    
    
    

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Ui()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()



