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

  @classmethod
  def get(cls, sub_id):
    return cls.get_by_id(sub_id)
  def delete(self, sub_id):
    Subtitle.query(id = sub_id).key.delete()



# </class_Subtitle>
###############################################################################

