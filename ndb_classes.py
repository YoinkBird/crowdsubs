import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

import webapp2

###############################################################################
# < class_Subtitle>
class Subtitle(ndb.Model):
#  id          = ndb.StringProperty(required=True)
  content     = ndb.StringProperty(required=True)

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
  def get_id_string(self):
    subtitle_id = str(self.key.string_id())
    return subtitle_id

  def get_text(self):
    return self.content
  #</instance accessors>

# </class_Subtitle>
###############################################################################

