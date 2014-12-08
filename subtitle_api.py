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


  # <def validate_options>
  # lint options based on rules hard-coded in this method
  def validate_options(self,**kwargs):
    if(kwargs):
      # RuleXXX: only check 'subtitle_content' , not all parameters
      if('subtitle_content' in kwargs):
        kwargs['subtitle_content'] = self.json_dump(kwargs['subtitle_content'])
        import logging
        logging.info("dumping 'subtitle_content' to string")
    return kwargs
  # </def validate_options>

  def post(self):
    self.get()
  def get(self):
    # assume subtitle_id is required to get to this page
    paramDict = self.parse_options(paramList = ['subtitle_id','subtitle_content','action'])
    paramDict = self.validate_options(**paramDict)
    self.process_json(**paramDict)
  def process_json(self, **kwargs):
    # TODO: add option parsing to BaseHandler
    if(kwargs):
      paramDict = kwargs
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
      elif(action == "translate"):
        # Doc: http://mymemory.translated.net/doc/spec.php
        # URL: http://api.mymemory.translated.net/get?q=Hello%20World!&langpair=en|it
        ##########
        translateUrl = 'http://api.mymemory.translated.net'
        # TODO: user-select language
        targetLang = 'it'
        subtitle_id_lang = subtitle_id + '_lang_' + targetLang
        jsonSendDict = {'q':subContentStr, 'langpair':'en|' + targetLang}
        translateJson = json.loads(self.sendUrlGet(jsondata = jsonSendDict, service_name = 'get', url = translateUrl))
        if(0): #debug
          jsonDict['translate_repsonse'] = translateJson
        jsonDict['translated_text'] = translateJson['responseData']['translatedText']
        jsonDict['subtitle_id'] = subtitle_id_lang
        self.create_or_update_sub(subtitle_id_lang, jsonDict['translated_text'])

    self.response.write(json.dumps(jsonDict))
    debug = 0
    if(debug):
      self.response.write('<pre>' + json.dumps(jsonDict, indent=4) + '</pre>')
    return jsonDict
  # </def get>



  # <def create_or_update_sub>
  def create_or_update_sub(self, subtitle_id, subtitle_content):
    jsonDict = {}
    jsonDict['status'] = {'code':10, 'msg': "no content provided"}
    if(subtitle_id and subtitle_content):
      subInst = self.create_sub(subtitle_id, subtitle_content).get()
      # return success/fail
      # TODO: un-hardcode the value, use the return of self.create_sub
      jsonDict['status'] = {'code':15, 'msg': "unable to store OR retrieve"}
      if(subInst is not None):
        jsonDict['status'] = {'code':0, 'msg': "successful store AND retrieve"}
    return jsonDict
  # </def create_or_update_sub>


  def create_sub(self, sub_id, content):
    # get subtitle (will be "None" if this is a new subtitle)
    newSub = self.retrieve_sub(sub_id)
    # assume valid type
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



