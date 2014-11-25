import json
import os
import jinja2
################################################################
# < def_sendJson>
# TODO: split into two functions:
#     - one purely for setting up url, args, etc
#     - one purely for sending json/retrieving result
def sendJson(self,**kwargs):
  from google.appengine.api import urlfetch
  urlfetch.set_default_fetch_deadline(60)
  #TODO: for loop, defaults, error checkign
  formDict = kwargs
  jsondata = formDict['jsondata']

  # check if input data is json
  # if not, convert to json - this makes calling the function much simpler
  try:
    json.loads(jsondata)
  except:
    jsondata = json.dumps(jsondata)
  # define URL as current host
  url = self.request.host_url + '/'

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
# < def_load_template>
# returns valid html, sample usage: self.response.write(load_template(<filepath>))
def load_template(self, **kwargs):
  paramDict = kwargs
  templateStr = ''
  # jinja setup
  jinja_loader_instance = jinja2.Environment(
      loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
      extensions=['jinja2.ext.autoescape'],
      autoescape=True)
  if('file' in paramDict):
    # check for file existence, modify if needed
    templateFile = locate_template(self, paramDict['file'])
    # default case if 'type' not specified
    if(not 'type' in paramDict):
      paramDict['type'] = 'jinja'
    if('type' in paramDict):
      # load file as jinja template
      if(paramDict['type'] == 'jinja'):
        templateInst = jinja_loader_instance.get_template(templateFile)
        valuesDict = {}
        #TODO: add param for 'template_values'
        if('values' in paramDict):
          valuesDict = paramDict['values']
        templateStr = templateInst.render(valuesDict)
      # load file as plain-text, no parsing 
      elif(paramDict['type'] == 'html'):
        # normal open file
        indexTemplateHandler = open(templateFile, 'r')
        templateStr = indexTemplateHandler.read()
        indexTemplateHandler.close()
  return templateStr
# </def_load_template>
################################################################


################################################################
# < def_locate_template>
# really simple for now:
#  if template not found just add '.html' and be done with it
def locate_template(self, filename):
  if(not os.path.isfile(filename)):
    filename += '.html'
  return filename
# < def_locate_template>
################################################################
