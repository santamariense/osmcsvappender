import xml.dom.minidom
from xml.dom import minidom
from queryoncsv import *
import datetime
import os

def inserttagsto( osmfilesource , csvfilesource, outputdirectory, csvdelimiter, csvquotechar, matchtaglist, matchgeometries, importfieldlist, primarykey, ovwrtags):  

  timenow = filter(str.isdigit, str(datetime.datetime.now()))[8:][:6]   

  # copy csv file to count usage
  csvfilecounter = csvtable().copyCSVfile(timenow,outputdirectory, csvfilesource,csvdelimiter,csvquotechar)
  csvtable().adjustCSVlogfile (primarykey,csvfilecounter,csvdelimiter,csvquotechar)

  # "s" preffix refers to source osm file while "t" preffix refers to target osm file

  #####################################################################################
  ## Working with the OSM file
  parseOSM = xml.dom.minidom.parse(osmfilesource);
  
  sosmfile = parseOSM.documentElement
  sxml_osm = sosmfile.nodeName
  sxml_osm_version = sosmfile.getAttribute('version')
  sxml_osm_upload = sosmfile.getAttribute('upload')
  sxml_osm_generator = sosmfile.getAttribute('generator')
  
  # OSM file builder: 1 - It starts building a new osmfile
  tdoc = minidom.Document() 
  txml_osm = tdoc.createElement('osm')                   #<osm>
  if sxml_osm_version:
    txml_osm.setAttribute('version',sxml_osm_version)
  if sxml_osm_upload:
    txml_osm.setAttribute('upload',sxml_osm_upload)
  if sxml_osm_generator:
    txml_osm.setAttribute('generator',(sxml_osm_generator))
  
  sgeometries = [sgeometry for sgeometry in sosmfile.childNodes if sgeometry.nodeType== \
             sosmfile.ELEMENT_NODE]
  
  # get geometry type - node, way or relation -, or bounds, as well as their attributes: 
  # OSM file builder: It builds geometry (node, way or relation) as well as their attributes
  osmfullidfound = False
  osmfullidvalue = None
  csvlistoftags = []
  rCount = 0
  wCount = 0
  nCount = 0
  for sgeometryType in sgeometries:
    sxml_geometry = sgeometryType.nodeName
    geometrymatches = ( sxml_geometry in matchgeometries )
    txml_geometry = tdoc.createElement(sxml_geometry)
    txml_osm.appendChild(txml_geometry) # bounds, node, way or relation
    for key, value in sgeometryType.attributes.items():
      txml_geometry.setAttribute(key,value)
      # if primarykey="osmfullid" the join will be by osm geometry full id, example: r63342
      if ( primarykey == 'osmfullid' ):
        if ( key == 'id' ):
          osmfullidfound = True
          osmfullidvalue = sxml_geometry[:1] + value
          csvlistoftags = csvtable().getalltagsof('osmfullid', osmfullidvalue,csvfilesource,csvdelimiter,csvquotechar)
          #print ' '
          #print ' '
          try:csvlistoftags.remove(['osmfullid',osmfullidvalue])
          except: primarykeyfound = False # It didnt find a value to a key "primarykey" on csv file
  
    # Get geometry's items
    sgeometrySubTags = [sdetail for sdetail in sgeometryType.childNodes if sdetail.nodeType == \
               sosmfile.ELEMENT_NODE]
  
  
    # Get geometry item: nd, member or tag
    # OSM file builder: It builds geometry's item (nd, member or tag) as well as their attributes
    primarykeyfound = True
    itemistag = False
    sosmfiletags = []
    pk_key = ''
    pk_value = ''
    # Copy the tags from source osm file to target one
    for sgeometryDetails in sgeometrySubTags:
      sxml_geometry_item = sgeometryDetails.nodeName
      itemistag = (sxml_geometry_item == "tag")    
      txml_geometry_item = tdoc.createElement(sxml_geometry_item)
      for key, value in sgeometryDetails.attributes.items():
        if ( not itemistag ):
          txml_geometry.appendChild(txml_geometry_item)  # nd or member
          txml_geometry_item.setAttribute(key,value)
          txml_geometry_item.setAttribute(key,value)
        else:
          #from now on, test if primary key exists and create a list of osm source file tags
          stag_key = sgeometryDetails.getAttribute('k') 
          stag_value = sgeometryDetails.getAttribute('v')
          if ( [stag_key, stag_value] not in sosmfiletags):
            sosmfiletags.append([stag_key, stag_value])
          if ( primarykey == stag_key ):
            pk_key = stag_key
            pk_value = stag_value
    if ( not osmfullidfound ): 
      csvlistoftags = csvtable().getalltagsof(pk_key, pk_value,csvfilesource,csvdelimiter,csvquotechar)
      try:csvlistoftags.remove([pk_key,pk_value])
      except: primarykeyfound = False # It didnt find a value to a key "primarykey" on csv file
            

    #remove osmfullid=* from the import list fields
    for csvkey, csvvalue in csvlistoftags:
      if (csvkey == "osmfullid"): 
        csvlistoftags.remove([csvkey,csvvalue])

    # Verify if matchtaglist matches with osm source file tags
    matchcount = 0
    tagmatches = False
    for key, value in matchtaglist:
      if value == "*":
        if ( any(key in i for i in sosmfiletags) ): matchcount += 1
      else:
        if ( [key,value] in sosmfiletags ): matchcount += 1
    if ( len(matchtaglist) ==  matchcount ): tagmatches = True
    # Get a final tag list
    if ( geometrymatches and tagmatches and (primarykeyfound or osmfullidfound) ): # If it passes in tag filter  
      finaltl = []
      if ovwrtags: # priority is csvfile
        for csvkey, csvvalue in csvlistoftags:
          if ( csvkey in importfieldlist ):
            finaltl.append([csvkey,csvvalue])
        for skey, svalue in sosmfiletags: # If it wasnt on csv list, add from osmfile one
          if not (any(skey in i for i in finaltl)):
            finaltl.append([skey,svalue])
      else:  # priority is sosmfile
        for skey, svalue in sosmfiletags:
          finaltl.append([skey,svalue])
        for csvkey, csvvalue in csvlistoftags:
          if ( csvkey in importfieldlist ):
            if not (any(csvkey in i for i in finaltl)):
              finaltl.append([csvkey,csvvalue])
    else: # If tags don't match, final tags will be osm source file itself
      finaltl = sosmfiletags
    # Set a tag for each item on final tag list
    for key, value in finaltl:
      txml_geometry_item = tdoc.createElement("tag")
      txml_geometry.appendChild(txml_geometry_item)
      txml_geometry_item.setAttribute('k',key)
      txml_geometry_item.setAttribute('v',value)
      if ( finaltl != sosmfiletags ):
        txml_geometry.setAttribute('action','modify')

    # Count how many times a row in csv file is used
    totalusecount = 0
    nodeusecount = 0
    wayusecount = 0
    relationusecount = 0
    if ( finaltl != sosmfiletags ):
      if ( primarykey == 'osmfullid' ):
        pk_value = osmfullidvalue
      else:
        for key, value in finaltl:
          if ( key == primarykey ):
            pk_value = value
      pk_counter = csvtable().getalltagsof(primarykey,pk_value,csvfilecounter,csvdelimiter,csvquotechar)
      for key, value in pk_counter:
        if ( key == 'total_updated' ):
          totalusecount = str(int(value) + 1)
        if ( key == 'node_updated' ):
          nodeusecount = str(int(value))
          if ( sxml_geometry == 'node'):
            nodeusecount = str(int(value) + 1)
        if ( key == 'way_updated' ):
          wayusecount = str(int(value))
          if ( sxml_geometry == 'way'):
            wayusecount = str(int(value) + 1)
        if ( key == 'relation_updated' ):
          relationusecount = str(int(value))
          if ( sxml_geometry == 'relation'):
            relationusecount = str(int(value) + 1)
      pk_counter = [pk_value,totalusecount,nodeusecount,wayusecount,relationusecount]
      csvtable().modifyCSVLine(pk_counter,csvfilecounter,csvdelimiter,csvquotechar)
    # End _ Count how many times a row in csv file is used


  csvtable().CSVsummation(csvfilecounter,csvdelimiter,csvquotechar)
  ## OSM file builder -- print it
  
  # Format osm file
  tdoc.appendChild(txml_osm)
  tosmfile = tdoc.toxml(encoding='UTF-8')
  tosmfile = tosmfile.replace('><','>\n<')
  tosmfile = tosmfile.replace('\n<node','\n  <node')
  tosmfile = tosmfile.replace('\n<way','\n  <way')
  tosmfile = tosmfile.replace('\n<relation','\n  <relation')
  tosmfile = tosmfile.replace('\n</','\n  </')
  tosmfile = tosmfile.replace('\n<nd','\n    <nd')
  tosmfile = tosmfile.replace('\n<member','\n    <member')
  tosmfile = tosmfile.replace('\n<tag','\n    <tag')
  tosmfile = tosmfile.replace('\n  </osm>','\n</osm>')

  # Write osm into a file
  oposmfile =  outputdirectory + os.path.splitext(os.path.basename(osmfilesource))[0] + "_osmcsvappender_" + timenow + ".osm"
  f = open(oposmfile, 'w')
  f.write(tosmfile)
  f.close

  return [timenow,oposmfile,csvfilecounter]
