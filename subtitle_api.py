# DESCRIPTION:

import webapp2
import json
import logging
# project-specific files
from basehandler import BaseHandler
from ndb_classes import Subtitle

class SubtitleApiHandler(BaseHandler):
  # https://webapp-improved.appspot.com/guide/handlers.html?highlight=override#overriding-init
  def __init__(self, request, response):
    # Set self.request, self.response and self.app.
    self.initialize(request, response)
    self.pageRelUrl = 'subs'
  def post(self):
    self.get()
  def get(self):
    self.process_json()
  def process_json(self):
    # TODO: add option parsing to BaseHandler
    # assume subtitle_id is required to get to this page
    paramDict = self.parse_options(paramList = ['subtitle_id','subtitle_content','action'])
    subtitle_id = paramDict['subtitle_id']
    subtitle_content = paramDict['subtitle_content']
    action = paramDict['action']

    # </end argparsing>
    if(not action):
      action = "display"
      if(not subtitle_id):
        action = "overview"

    # retrieve subtitle entry and contents
    subContentStr = ''
    if(subtitle_id):
      subInst = self.retrieve_sub(subtitle_id)
      if(subInst):
        subContentStr = subInst.get_text()
    jsonDict = {}

    logging.info("api: processing action" + '#' * 8)
    if(action):
      logging.info("action is %s" % action)
      # if XsubInst && submit
      # update is for create new sub and edit old sub
      # use aliases to allow for future growth (e.g. if 'create' needs to be separate)
      # status code 1x
      if(action == 'update' or action=='create' or action == 'submit'):
        # return code default is pessimistic
        # IDEA: add return codes like 'no content' or 'unable to store'
        jsonDict['status'] = {'code':10, 'msg': "no content provided"}
        if(subtitle_id and subtitle_content):
          # HACK! but it unifies "post" and "get"
          # TODO: do this correctly somehow.
          subInst = self.create_sub(subtitle_id, subtitle_content).get()
          #self.redirect("/" + self.pageRelUrl + "?subtitle_id=" + subtitle_id)
          # return success/fail
          # TODO: un-hardcode the value, use the return of self.create_sub
          jsonDict['status'] = {'code':15, 'msg': "unable to store OR retrieve"}
          if(subInst is not None):
            jsonDict['status'] = {'code':0, 'msg': "successful store AND retrieve"}
      # status code 2x
      elif(action == "display"):
        #STUB: jsonDict['status'] = {'code':25, 'msg': "unable to retrieve"}
        jsonDict = {subtitle_id:subContentStr}
      # status code 6x
      elif(action == "delete"):
        jsonDict['status'] = {'code':60, 'msg': "unable to delete"}
        # broken, not working
        if(0):
          Subtitle.delete(subtitle_id)
          #TODO: figure out what the return code is
          jsonDict['status'] = {'code':0, 'msg': "successful delete"}
      #TODO: finalise this
      elif(action == "overview"):
        jsonDict = {'overview' : 'TODO'}

    self.response.write(json.dumps(jsonDict))
  # </def get>





  def create_sub(self, sub_id, content):
    newSub = self.retrieve_sub(sub_id)
    if(not newSub):
      newSub = Subtitle(
          id = sub_id,
          content = content,
          )
    else:
      newSub.content = content
    return newSub.customput()

  def retrieve_sub(self, sub_id):
    foundSub = Subtitle.get(sub_id)
    return foundSub



