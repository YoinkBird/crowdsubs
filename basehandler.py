#!/usr/bin/env python

################################################################################
# DESCRIPTION:
# This is the class-file for the BaseHandler
# The BaseHandler defines methods that are common to all request handlers
# this class is a template class and is not meant to be called directly
################################################################################

import webapp2
import logging
# project-specific files
import common_functions

class BaseHandler(webapp2.RequestHandler):
    def parse_options(self,**kwargs):
      postVarDict = {}
      # < read in options>
      try: # json input
        postVarDict = json.loads(self.request.body)
      except: # x-www-form
        if('paramList' in kwargs):
          for param in kwargs['paramList']:
            postVarDict[param] = self.request.get(param)
            #logging.info("BaseHandler::parse_options - param " + param + " - value " + postVarDict[param])
      return postVarDict
      #</read in options>
    # determine template based on (in order):
    # 1. passed-in filename, e.g. render_response(file='filename.html')
    # 2. current path
    # 3. index.html
    def render_response(self, **kwargs):
      paramDict = kwargs
      templateStr = ''
      path = self.request.path
      templateDir = 'templates'
      if('file' in paramDict):
        templatePath = templateDir + '/' + paramDict['file']
        paramDict['file'] = templatePath
        templateStr = common_functions.load_template(self, **paramDict)
      else:
        # Note: leaving out any additional params in paramDict
        #   this is because additional params are template-specific
        try:
          templatePath = templateDir + '/' + path
          templateStr = common_functions.load_template(self, file=templatePath)
        except:
          #TODO: 404 page for not-found templates instead of simply loading homepage
          path = "index.html"
          templatePath = templateDir + '/' + path
          templateStr = common_functions.load_template(self, file=templatePath)
      # print template
      self.response.write(templateStr)
