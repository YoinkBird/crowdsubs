#!/usr/bin/env python

################################################################################
# DESCRIPTION:
# This is the class-file for the BaseHandler
# The BaseHandler defines methods that are common to all request handlers
# this class is a template class and is not meant to be called directly
################################################################################

import webapp2
import logging
import json
# project-specific files
import common_functions

class BaseHandler(webapp2.RequestHandler):
    def parse_options(self,**kwargs):
      postVarDict = {}
      # < read in options>
      try: # json input
        postVarDict = json.loads(self.request.body)
      # TODO: catch ValueError: No JSON object could be decoded
      except: # x-www-form
        if('paramList' in kwargs):
          for param in kwargs['paramList']:
            postVarDict[param] = self.request.get(param)
            #logging.info("BaseHandler::parse_options - param " + param + " - value " + postVarDict[param])
      return postVarDict
      #</read in options>

    #<def render_template>
    # determine template based on (in order):
    # 1. passed-in filename, e.g. render_template(file='filename.html')
    # 2. current path
    # 3. index.html
    def render_template(self, **kwargs):
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
      return templateStr
    #</def render_template>

    #<def render_response>
    # render_template and write out
    def render_response(self, **kwargs):
      templateStr = self.render_template(**kwargs)
      # print template
      self.response.write(templateStr)
    #</def render_response>

    ################################################################
    # < def_sendJson>
    # TODO: split into two functions:
    #     - one purely for setting up url, args, etc
    #     - one purely for sending json/retrieving result
    def sendJson(self,**kwargs):
      from google.appengine.api import urlfetch
      urlfetch.set_default_fetch_deadline(60)
      # define URL as current host
      url = self.request.host_url + '/'
      if(kwargs):
        #TODO: for loop, defaults, error checkign
        if('url' in kwargs):
          url = kwargs['url']
      formDict = kwargs
      jsondata = formDict['jsondata']

      # check if input data is json
      # if not, convert to json - this makes calling the function much simpler
      try:
        json.loads(jsondata)
      except:
        jsondata = json.dumps(jsondata)

      # get "service name", i.e. the url sub-path
      if('service_name' in formDict):
        url += formDict['service_name']
      # src: https://developers.google.com/appengine/docs/python/appidentity/#Python_Asserting_identity_to_Google_APIs
      result = urlfetch.fetch(
          url,
          payload = jsondata,
          method=urlfetch.POST,
          headers = {'Content-Type' : "application/json"},
          )
      # store return string
      jsonRetStr = 'the_if_else_broke_in_def_sendjson'
      if(result.status_code == 200):
        jsonRetStr = result.content
      else:
        jsonRetStr = ("Call failed. Status code %s. Body %s" % (result.status_code, result.content))
        # Note on error-handling from above google page: # raise Exception(jsonRetStr)
        jsonRetStr = json.dumps({'error':jsonRetStr})
      #TODO: validate response with "try: ... except: ..." etc #jsonRetStr = json.loads(result.content)
      return jsonRetStr
    # </def_sendJson>
    ################################################################

    ################################################################
    # < def_sendUrlGet>
    # TODO: split into two functions:
    #     - one purely for setting up url, args, etc
    #     - one purely for sending json/retrieving result
    def sendUrlGet(self,**kwargs):
      from google.appengine.api import urlfetch
      urlfetch.set_default_fetch_deadline(60)
      # define URL as current host
      url = self.request.host_url + '/'
      if(kwargs):
        #TODO: for loop, defaults, error checkign
        if('url' in kwargs):
          url = kwargs['url']
      formDict = kwargs
      jsondata = formDict['jsondata']

      # encode params for URL GET request
      import urllib
      requestParams = urllib.urlencode(jsondata)

      url += '/'
      # get "service name", i.e. the url sub-path
      if('service_name' in formDict):
          url += formDict['service_name']
      if(requestParams):
        url += '?'
        url += requestParams
      # src: https://developers.google.com/appengine/docs/python/appidentity/#Python_Asserting_identity_to_Google_APIs
      result = urlfetch.fetch(
          url,
          #payload = jsondata,
          method=urlfetch.GET,
          headers = {'Content-Type' : "application/json"},
          )
      # store return string
      jsonRetStr = 'the_if_else_broke_in_def_sendjson'
      if(result.status_code == 200):
        jsonRetStr = result.content
      else:
        jsonRetStr = ("Call failed. Status code %s. Body %s" % (result.status_code, result.content))
        # Note on error-handling from above google page: # raise Exception(jsonRetStr)
        jsonRetStr = json.dumps({'error':jsonRetStr})
      #TODO: validate response with "try: ... except: ..." etc #jsonRetStr = json.loads(result.content)
      return jsonRetStr
    # </def_sendUrlGet>
    ################################################################
