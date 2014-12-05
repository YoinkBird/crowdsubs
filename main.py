#!/usr/bin/env python

################################################################################
# DESCRIPTION:
# This file defines the MainHandler as well as the request-handler
# The MainHandler is the default request handler
################################################################################
import os

import webapp2
import logging
# project-specific files
from basehandler import BaseHandler
import editsubs
import subtitle_api

class MainHandler(BaseHandler):
  def get(self):
    self.render_response()

# http://webapp-improved.appspot.com/guide/routing.html#lazy-handlers
app = webapp2.WSGIApplication([
    ('/api',  subtitle_api.SubtitleApiHandler),
    ('/subs', editsubs.SubtitleEditHandler),
    # default - leave at end of list as a catch-all
    ('.*', MainHandler),
], debug=True)


# Notes:
# Notes for imports:
# logging: logging.info()
