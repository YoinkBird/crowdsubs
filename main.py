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

class MainHandler(BaseHandler):
  def get(self):
    self.render_response()

app = webapp2.WSGIApplication([
    ('/.*', MainHandler),
], debug=True)


# Notes:
# Notes for imports:
# logging: logging.info()
