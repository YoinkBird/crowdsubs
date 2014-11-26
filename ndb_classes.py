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
  # key for subtitle content : "subtitles"
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
    jsonDict = {}
    jsonList = []
    # store subtitle content line-for-line in jsonDict
    for number, line in enumerate(self.content.splitlines()):
      tmpList = [number, line]
      jsonList.append(tmpList)

    jsonDict["subtitles"] = jsonList
    self.contentJson = jsonDict
    # update summary
    self.updateSummary(jsonList)

  # TODO: update summary from json in order to be called directly
  def updateSummary(self, jsonList):
    numLines = len(jsonList)
    # Name | Lines | Content
    self.subSummary = [
        self.get_id_string(),
        str(numLines),
        jsonList[ numLines/2][1],
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

