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
  content     = ndb.StringProperty(required=True)
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
    for number, line in enumerate(inputLineList):
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
        if(tmpRevList[0]['txt'] != line):
          thisRevisionDict['rev_id'] = revision_id
          tmpRevList.insert(0, thisRevisionDict)
      tmpDict = {'line_id':str(number), 'rev' : tmpRevList}
      jsonList.append(tmpDict)

    jsonDict["subtitles"] = jsonList
    self.contentJson = jsonDict
    # update summary
    self.updateSummary()
  
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
