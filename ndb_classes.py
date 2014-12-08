import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import webapp2
import json

###############################################################################
# < class_Subtitle>
class Subtitle(ndb.Model):
  #<ndb fields>
  # json structure notes:
  # json format:
  # {"subtitles": [{"line_id": "0", "rev": [{"txt": "line1", "votes": 1}]},
  #                {"line_id": "1", "rev": [{"txt": "line2", "votes": 1}]}]}
  contentJson = ndb.JsonProperty()
  content     = ndb.StringProperty(required=True,indexed=False)
  # summary of subtitle
  subSummary  = ndb.StringProperty(repeated=True)
  #</ndb fields>

  #<class methods>
  @classmethod
  def get(cls, sub_id):
    return cls.get_by_id(sub_id)

  @classmethod
  def get_all(cls):
    return cls.query()

  @classmethod
  def delete(cls, sub_id):
    cls.get(sub_id).key.delete()

  @classmethod
  def get_voting_params(cls):
    requiredParams = ['line_id','rev_id','vote']
    return requiredParams
  #</class methods>

  #<instance accessors>
  # can't figure out how to override 'put'
  # this will have to be called before 'put'
  def customput(self, **kwargs):
    if(kwargs):
      if('content' in kwargs):
        self.content = kwargs['content']
    # experimental
    self.update_json_from_table()
    # if 'content' is a valid json string...
    self.update_content_from_table()
    # ... or just text
    self.updateJson()
    return self.put()

  def updateJson(self):
    # json format:
    # {"subtitles": [{"line_id": "0", "rev": [{"txt": "line1", "votes": 1}]},
    #                {"line_id": "1", "rev": [{"txt": "line2", "votes": 1}]}]}
    jsonDict = {}
    jsonList = []
    subtitleList = self.get_subtitle_list()
    # store subtitle content line-for-line in jsonDict
    inputLineList = self.content.splitlines()
    # split input into 2d list for processing
    inputLineList = self.parse_input_text(
        text = self.content
        )
    # format: lineList['line_id' , 'inputTxtLine']
    for number, lineList in enumerate(inputLineList):
      line    = lineList[1]
      line_id = lineList[0]
      # default values for first entry; may be overwritten or discarded
      thisRevisionDict = {"txt":line,"votes":1,"rev_id":"0000"}
      # get current revisions
      try:
        tmpRevList = subtitleList[number]['rev']
      except:
        tmpRevList = [thisRevisionDict]

      '''
      # generate revision_id to track specific revisions, e.g. for vote-url
      #  simple: just use the total number of revisions
           as string as per http://stackoverflow.com/a/13919632
      #  complex: use sha1 of line+entire text to avoid colliding sha1 if 2 lines are equal
      #    see notes at bottom '''
      revision_id = "%04d" % (len(tmpRevList))
      # check if changed
      # simple check:
      if(len(subtitleList) == len(inputLineList)):
        # note: votes will be tallied when revisions are merged (to be implemented)
        # verify that change is not already present
        #   impl: set flag 'rev_id_found' if line-version already present
        rev_id_found = 0
        for revDict in tmpRevList:
          if(revDict['txt'] == line):
            rev_id_found = 1
        # if line-version not already present, create new rev_id 
        if(rev_id_found == 0):
          thisRevisionDict['rev_id'] = revision_id
          tmpRevList.insert(0, thisRevisionDict)
      # finalise
      tmpLineDict = {'line_id' : line_id, 'rev' : tmpRevList}
      jsonList.append(tmpLineDict)

    jsonDict["subtitles"] = jsonList
    self.contentJson = jsonDict
    # update summary
    self.updateSummary()

  #<def load_json>
  # attempt to load input as json
  def load_json(self, **kwargs):
    suspectedJson = self.content
    if(kwargs):
      if('json' in kwargs):
        suspectedJson = kwargs['json']
    # hold return value
    jsonObject = ''
    try:
      jsonObject = json.loads(suspectedJson)
    except TypeError, e:
      dumpable = json.dumps(suspectedJson)
      if(dumpable):
        jsonObject = suspectedJson
    except ValueError, e: # No JSON object could be decoded
      import logging
      logging.info("load_json: " + str(e))
      logging.info(suspectedJson)
      logging.info(type(suspectedJson))
      return False
    return jsonObject
  #<def load_json>

  #<def update_content_from_table>
  # convert table to content format s.t. it can be processed by load_json
  # Note: intermediate function to bridge gap between table and textarea
  #       when textarea is gone, this function will no longer be needed
  # Note: this does not adhere to the one-line_id-per-line paradigm
  def update_content_from_table(self, **kwargs):
    tableList = self.load_json()
    if(kwargs):
      if('tableList' in kwargs):
        tableList = kwargs['tableList']
    if(not tableList):
      return
    # handsontable sample entry:
    # [{"line_id": "001", "time": "1:04", "txt": "black", "votes": 9},]

    # 'content' field only has the text
    contentStr = ''
    # track which lines are updated to avoid duplications
    #  won't be needed once 'update_json_from_table' is implemented
    last_line_id_list = []
    for line_id_dict in tableList:
      lineStr = line_id_dict['txt']
      line_id = line_id_dict['line_id']
      if(lineStr):
        # don't insert if line_id already taken
        if(line_id and (line_id not in last_line_id_list)):
          last_line_id_list.append(line_id)
          contentStr += lineStr + "\n"
    self.content = contentStr
    pass
  #</def update_content_from_table>

  #<def update_json_from_table>
  def update_json_from_table(self, **kwargs):
    import logging
    tableList = self.load_json()
    if(kwargs):
      if('tableList' in kwargs):
        tableList = kwargs['tableList']
    if(not tableList):
      return
    # loop through list and extract data 
    # handsontable sample entry:
    # [{"line_id": "001", "time": "1:04", "txt": "black", "votes": 9},]
    # contentJson format:
    # {"subtitles": [{"line_id": "001", "rev": [{"time": "1:04", "txt": "line1", "votes": 1}]},
    #                {"line_id": "002", "rev": [{"time": "2:07", "txt": "line2", "votes": 1}]}]}

    # values if line is new - TODO: determine line_id
    defaultValues = {"votes":1,"rev_id":"0000"}
    for line_id_dict in tableList:
      logging.info("looping through input:")
      logging.info(line_id_dict)
      # assign default values, e.g. new entry has no revision, votes
      for default in defaultValues:
        if(default not in line_id_dict):
          line_id_dict[default] = defaultValues[default]
      # create entry for contentJson:
      # find revision
      # first, get corresponding line_id_dict
      line_id_index = self.insert_line_id_dict(line_id_dict)
      logging.info("received line_id_index " + str(line_id_index))
      if(line_id_index):
        line_id_dict_old = self.contentJson['subtitles'][line_id_index]
        # now line_id_dict should match contentJson format if nothing was changed
        ### if(line_id_dict != contentJson['subtitles'][line_id])
        #rev_id_list = self.contentJson['subtitles'][line_id]['rev'].keys()


  #</def update_json_from_table>

  # add line_id dict to JsonProperty
  def insert_line_id_dict(self,line_id_dict):
    import logging
    logging.info("#" * 8 + "entering insert_line_id_dict")
    logging.info("passed in line_id_dict:")
    logging.info(line_id_dict)
    # extract line_id; delete because we need to subclass revisions by line_id
    line_id = line_id_dict.pop('line_id',None)

    # step1: create index if none exists
    if(not line_id):
      # TODO: generate line_id
      return

    # step2: get index of corresponding line_id_dict
    # first, get corresponding line_id_dict
    line_id_index = self.get_index_of_line_id(line_id)
    logging.info("received line_id_index " + str(line_id_index))
    # step3: get line_id_dict at line_id_index
    if(line_id_index):
      self.insert_rev_id_dict(line_id_index, line_id_dict)

    # step-final: return line_id_index
    logging.info("#" * 8 + "leaving insert_line_id_dict")
    return line_id_index

  def get_index_of_line_id(self,line_id):
    import logging
    logging.info("looking up line_id " + str(line_id))
    for index, line_id_dict in enumerate(self.contentJson['subtitles']):
      if(line_id_dict['line_id'] == line_id):
        logging.info("found line_id at " + str(index))
        logging.info(self.contentJson['subtitles'][index])
        return index

  # add rev_id dict to JsonProperty at given line_id_index
  def insert_rev_id_dict(self, line_id_index, line_id_dict):
    import logging
    logging.info("#" * 8 + "entering insert_rev_id_dict")
    logging.info("passed in line_id_dict:")
    logging.info(line_id_dict)
    line_id_dict_old = self.contentJson['subtitles'][line_id_index]
    # step4: create rev_id if none exists
    # note: this is also taken care of by the calling function
    if(not line_id_dict['rev_id']):
      line_id_dict['rev_id'] = '0000'

    # step5: get existing rev_id
    rev_id_list = self.contentJson['subtitles'][line_id_index]['rev']
    logging.info("existing rev_ids:" + str(len(rev_id_list)))
    logging.info(rev_id_list)
    logging.info("/existing rev_ids:")

    # step6: check if current rev equal to any in the list
    found_flag = 0
    new_rev_id = 0
    for rev_id_dict in rev_id_list:
      logging.info(line_id_dict)
      logging.info(rev_id_dict)
      if(line_id_dict == rev_id_dict):
        found_flag = 1
      else:
        new_rev_id = len(rev_id_list)
    if(found_flag == 0):
      logging.info("assigning " + str(new_rev_id))
      line_id_dict['rev_id'] = "%04d" % (new_rev_id)
      self.contentJson['subtitles'][line_id_index]['rev'].append(line_id_dict)
      self.put()
    
  #<def get_line_by_rev>
  # return False for bad inputs
  # return empty dict for 
  def get_line_by_rev(self, **kwargs):
    for reqParam in ['line_id','rev_id']:
      if(reqParam not in kwargs):
        return False

    # get all current revisions
    subtitleList = self.get_subtitle_list()
    pass
  #</def get_line_by_rev>
  
  #<parse_input_text>
  def parse_input_text(self, **kwargs):
    text = ''
    if(kwargs):
      if('text' in kwargs):
        text = kwargs['text']

    # convert input to list
    inputLineList = text.splitlines()
    # split input into 2d list for processing
    textList = []
    # simple conversion to begin
    for number, line in enumerate(inputLineList):
      line_id = "%05d" % (number)  # formatting for appearance, should be done in front-end, not here
      tmpList = [line_id, line]
      textList.append(tmpList)
    return textList
  #</parse_input_text>

  def get_subtitle_list(self):
    subList = []
    # first, store into dict 
    jsonDict = self.contentJson
    # get list
    try:
      if("subtitles" in jsonDict):
        subList = jsonDict["subtitles"]
    except:
      pass
    return subList

  #<def get_2d_list>
  def get_2d_list(self):
    subDataList = self.get_subtitle_list()

    # loop through subtitle line entries and extract data
    tableRows = []
    for lineIdDict in subDataList:
      tmpTableRow = []
      revKeys = ['time','txt','votes','rev_id']
      # get all revisions
      for revNum, revDict in enumerate(lineIdDict['rev']):
        tmpTableRow = [lineIdDict["line_id"]]
        for key in revKeys:
          if(key in revDict):
            tmpTableRow.append(revDict[key])
          else:
            tmpTableRow.append("&nbsp;")
        tableRows.append(tmpTableRow)
    return tableRows
  #</def get_2d_list>

  #<def get_table_config_dict>
  # mainly for the JavaScript 'handsontable' data-grid editor
  #  doc: http://handsontable.com/
  # define table for displaying subtitles:
  # * table headers (for display)
  # * column-names to display
  # ** optional attribs: e.g. 'readOnly' for 'handsontable'
  # * table data
  # ** list of dicts with {colName1 : data1, colName2 : data2}
  #
  # handsontable sample entry:
  # [{"line_id": "001", "time": "1:04", "txt": "black", "votes": 9},]
  def get_table_config_dict(self):
    subDataList = self.get_subtitle_list()
    # title of columns
    tableColHeaders = ["line_id", "time", "txt", "votes", "rev_id"]
    # columns to display + attribs
    tableColumns = [
        {
          "data" : "line_id",
          "readOnly" : "true"
          },
        {
          "data" : "time"
          },
        {
          "data" : "txt"
          },
        {
          "data" : "votes",
          "readOnly" : "true"
          },
        {
          "data" : "rev_id",
          "readOnly" : "true",
          "renderer" : "html"
          }
        ]

    # loop through subtitle line entries and extract data
    tableDataList = []
    for lineIdDict in subDataList:
      revKeys = ['time','txt','votes','rev_id']
      # get all revisions
      for revNum, revDict in enumerate(lineIdDict['rev']):
        tmpTableDict = {}
        tmpTableDict['line_id'] = lineIdDict["line_id"]
        for key in revKeys:
          if(key in revDict):
            tmpTableDict[key] = revDict[key]
          else:
            tmpTableDict[key] = ''
        tableDataList.append(tmpTableDict)
    tableConfigDict = {
        'data'       : tableDataList,
        'colHeaders' : tableColHeaders,
        'columns'    : tableColumns,
        }
    tableConfigDict['subtitle_id'] = self.get_id_string()
    return tableConfigDict
  # </def get_table_config_dict>

  #<def updateVotes>
  def updateVotes(self, **kwargs):
    requiredParams = ['line_id','rev_id','vote']
    if(kwargs):
      for param in requiredParams:
        if(param not in requiredParams):
          return
    else:
      return
    subDataList = self.get_subtitle_list()

    # loop through subtitle lines, find matching line_id and rev_id
    for lineNum, lineIdDict in enumerate(subDataList):
      # find matching line_id
      if(lineIdDict["line_id"] == kwargs["line_id"]):
        # find matching rev_id
        for revNum, revDict in enumerate(lineIdDict['rev']):
          if(revDict["rev_id"] == kwargs["rev_id"]):
            # json structure:
            # curVotes = self.contentJson["subtitles"][lineNum]['rev'][revNum]["votes"]
            if(kwargs["vote"] == "up"):
              revDict["votes"] += 1
            elif(kwargs["vote"] == "down"):
              revDict["votes"] -= 1
    # save results
    self.put()
    return
  #</def updateVotes>


  # TODO: update summary from json in order to be called directly
  def updateSummary(self):
    subtitleList = self.get_subtitle_list()
    numLines = len(subtitleList)
    # Name | Lines | Content
    sampleText = subtitleList[ numLines/2 ]['rev'][0]['txt']
    if(sampleText == ''):
      sampleText = subtitleList[ numLines/3 ]['rev'][0]['txt']
    self.subSummary = [
        self.get_id_string(),
        str(numLines),
        sampleText,
        ]

  def get_id_string(self):
    subtitle_id = str(self.key.string_id())
    return subtitle_id

  def get_text(self):
    contentStr = self.content
    return contentStr

  def get_summary(self):
    return self.subSummary

  def get_json(self):
    jsonStr = ''
    try:
      jsonStr = json.dumps(self.contentJson)
    except:
      pass
    return jsonStr

  #</instance accessors>

# </class_Subtitle>
###############################################################################

# NOTES
#  http://blog.devzero.com/2013/01/28/how-to-override-a-class-method-in-python/
#  @classmethod
#  def put(cls):
#    super(Subtitle, cls).put(cls)

# sha1
#  see http://stackoverflow.com/a/552725 and concisely http://stackoverflow.com/questions/1869885/calculating-sha1-of-a-file
