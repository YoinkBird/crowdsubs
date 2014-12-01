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
      thisRevisionDict = {"txt":line,"votes":1}
      # get current revisions
      try:
        tmpRevList = subtitleList[number]['rev']
      except:
        tmpRevList = [thisRevisionDict]
      # check if changed
      # simple check:
      if(len(subtitleList) == len(inputLineList)):
        # note: votes will be tallied when revisions are merged (to be implemented)
        if(tmpRevList[0]['txt'] != line):
          tmpRevList.insert(0, thisRevisionDict)
      tmpDict = {'line_id':str(number), 'rev' : tmpRevList}
      jsonList.append(tmpDict)

    jsonDict["subtitles"] = jsonList
    self.contentJson = jsonDict
    # update summary
    #<TODO>
    #TODO: fix this when final format is decided
    if(0):
      self.updateSummary(jsonList)
    #</TODO>
  
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

  # TODO: update summary from json in order to be called directly
  def updateSummary(self, jsonList):
    numLines = len(jsonList)
    # Name | Lines | Content
    lineDict = jsonList[ numLines/2 ]
    lineDictKeys = lineDict.keys()
    sampleText = lineDict[lineDictKeys[0]]
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

