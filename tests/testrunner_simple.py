# TODO: clean up the remnant datastructures like 'testConfigDict'
import json
import httplib
import urllib

#  disable proxy settings if using urllib2
#import urllib2
#proxy_support = urllib2.ProxyHandler({})
#opener = urllib2.build_opener(proxy_support)
#print opener.open("http://localhost:8080/").read()
#

# documentation
# https://docs.python.org/release/2.6/library/httplib.html

# https://developers.google.com/appengine/docs/python/tools/localunittesting
# https://developers.google.com/appengine/docs/python/tools/handlertesting

# information
# https://webapp-improved.appspot.com/guide/request.html#registry
# https://appengine.cloudbees.com/index.html
# http://googleappengine.blogspot.com/2012/10/jenkins-meet-google-app-engine.html
 
globals = {
           "server": "localhost",
           "port"  : "8080",
           # prepare request header
           "headers": {"Content-type": "application/json", "Accept": "text/plain"},
           "userId": "honey_badger"
          }
 
horizline = ('#' * 32)
passedList = []
warnedList = []
failedList = []
def send_request(conn, url, req, **kwargs):
    #jsontest = 0  # dataprocess fail, form2json pass
    jsontest = 1  # dataprocess pass, form2json fail
    request_headers = globals["headers"]
    testname = url
    if(kwargs):
      if('headers' in kwargs):
        request_headers = kwargs['headers']
        if(request_headers['Content-type'] == 'application/json'):
          jsontest = 1
        if(request_headers['Content-type'] == 'application/x-www-form-urlencoded'):
          jsontest = 0
      if('testname' in kwargs):
        testname = kwargs['testname']
    params = ''
    #TODO: run with json first; if fail then run with x-www-form and/or others
    if(jsontest == 1):
      print "json request params:"
      params = json.dumps(req)
      print '%s' % params
    else:
      print "   request params (human readable): %s" % json.dumps(req)
      print "x-www-form-urlencoded request params:"
      params = urllib.urlencode(req)
      print '%s' % params
      request_headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/html"}

    print("headers: " + str(request_headers))
    conn.request("POST", url, params, request_headers)
    resp = conn.getresponse()
    print "status | reason"
    print "%s | %s" % (resp.status, resp.reason)
    response = resp.read()
    print "response:\n%s\n" % response
    print "json load:"
    try:
      jsonresp = json.loads(response)
      passedList.append(testname)
    except:
      if(jsontest == 1):
        jsonresp = 'testrunner_json.loads_fail'
        failedList.append(testname)
      else:
        jsonresp = '-I-: form header - skipping json load check'
        warnedList.append("form header:" + testname) # don't fail the test, but mark that it is not json
        passedList.append(testname)
    print '  %s' % jsonresp
    print "easy to read:"
    print '  %s' % json.dumps(jsonresp, indent=4)
    return jsonresp
 
def place_create_request(conn):
    # prepare create user request
    req = {"userId": globals["userId"]}
    # send request to server
    res = send_request(conn, "/api/user/create", req)
    return res
 
######################################################
#TODO: maybe just do this as json... then I can just have a json file to specify tests
# TODO: set defaults (e.g. user) otherwise this function doesn't have a purpose
# would need to read json intelligently, i.e. add a 'defaulttest' and allow inherit etc
def get_test_dict_pattern(**kwargs):
  testPatternDict = {} # this is returned
  if(kwargs):
    testPatternDict = kwargs
    params = ['request', 'service', 'headers','repeat']
    for param in params:
      if(param in kwargs):
        testPatternDict[param] = kwargs[param]
  if('service' not in testPatternDict):
    testPatternDict['service'] = 'api'
  return testPatternDict
######################################################
  
# many more functions like the above
################################################################ 
# TODO: should just translate normal subtitles...
def get_translation_tests():
  txlateTestList = []
  serviceName = 'api_translate_simple'
  testConfigDict[serviceName] = get_test_dict_pattern(
    serviceName = serviceName,
    request = {"subtitle_id":"test_translate_simple", "action":"translate", "subtitle_content":"should_not_be_here"},
    #repeat  = 15,
    )
  txlateTestList.append(testConfigDict[serviceName])
  import copy
  # default subtitle
  txlateDefault = copy.deepcopy(testConfigDict[serviceName])
  txlateDefault['serviceName'] = 'api_translate'
  txlateDefault['request']['subtitle_id'] = 'test_translate'
  txlateTestList.append(txlateDefault)
  # "demo" subtitle
  txlateDefault = copy.deepcopy(testConfigDict[serviceName])
  txlateDefault['serviceName'] = 'test_demo'
  txlateDefault['request']['subtitle_id'] = 'test_translate'
  txlateTestList.append(txlateDefault)

  return txlateTestList

if __name__ == '__main__':
  # < read args>
  # https://docs.python.org/2/library/optparse.html
  import optparse
  parser = optparse.OptionParser()
  options, args = parser.parse_args()
  # </read args>
  # < read from args>
  # path is first arg, port is second
  if len(args) >= 1:
    globals['server'] = args[0]
    if len(args) >= 2:
      globals['port'] = args[1]
    # don't check for 3, just assume away
    else:
      del(globals['port'])
  # </read from args>


  # < define server>
  # localhost
  if('port' in globals):
    conn = httplib.HTTPConnection(globals["server"],globals["port"])
  else:
    conn = httplib.HTTPConnection(globals["server"])
  # </define server>

  # TODO: define dict of services and tests in order to specify test-specific defaults
  # TODO: make that a list of dicts
  testConfigDict =  {
      'api_display' : {"subtitle_id" : "test1", "action" : "display", "subtitle_content" : "line1"},
      # http://localhost:8080/api?subtitle_id=test_translate_simple&action=translate
      #NO_WORK: 'api_translate_simple' : {"serviceName":"api_translate_simple", "service" : "api", "subtitle_id" : "test_translate_simple", "action" : "translate", "subtitle_content" : "should_not_be_here"},
      } 
  # easier
  serviceList = testConfigDict.keys()
  #< define request data>
  request = {"userId": globals["userId"]}
  #< define request data>

  if(1):
    ## default test
    import copy
    tmpRequestDict = {}
    serviceList = [] #clear out for this example
    defaulttest = {
        'service' : '/',
        'request' : {"userId": globals["userId"]}
    }


  '''
  # send as form:
  #  headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"},
  '''
  # set up crowdsubs tests
  if(1):
    serviceList = []
    if(1):
      ## display
      # url: api?subtitle_id=test2&action=update&subtitle_content=line2
      serviceName = 'api_display'
      testConfigDict[serviceName] = get_test_dict_pattern(
        serviceName = serviceName,
        request = {"subtitle_id":"test1", "action":"display", "subtitle_content":"line1"},
        #repeat  = 15,
        )
      serviceList.append(testConfigDict[serviceName])

    #issue: ValueError: No JSON object could be decoded
    if(1):
      ## create
      # url: api?subtitle_id=test2&action=update&subtitle_content=line2
      serviceName = 'test99_api_create'
      testConfigDict[serviceName] = get_test_dict_pattern(
        serviceName = serviceName,
        request = {"subtitle_id":"test_create_99", "action":"create", "subtitle_content":"line1\nline2"},
        #repeat  = 15,
        )
      # display newly created subtitle
      serviceName = 'test99_api_display'
      testConfigDict[serviceName] = get_test_dict_pattern(
        serviceName = serviceName,
        request = {"subtitle_id":"test_create_99", "action":"display", "subtitle_content":"line1"},
        #repeat  = 15,
        )
      serviceList.append(testConfigDict['test99_api_create'])
      # verify addition
      serviceList.append(testConfigDict['test99_api_display'])

    if(1):
      ## delete
      # url: api?subtitle_id=test2&action=update&subtitle_content=line2
      serviceName = 'test99_api_delete'
      testConfigDict[serviceName] = get_test_dict_pattern(
        serviceName = serviceName,
        request = {"subtitle_id":"test_delete_99", "action":"delete", "subtitle_content":"line1\nline2"},
        #repeat  = 15,
        )
      serviceList.append(testConfigDict[serviceName])

    if(1):
      serviceList.extend( get_translation_tests() )

  # RUN tests
  serviceRunList = testConfigDict.keys()
  serviceRunList = ['genericquery']
  import copy
  defaultrequest = copy.copy(request)
  # TODO: make hash where key is testname, hash is same as above with 'serviceList.append'
  # then the 'serviceRunList = testConfigDict.keys() could be used to disable a test on the fly
  #runOnlyTests = ('service',) # create a set, blah blah
  for testConfigDict in serviceList:
    # set vars
    service = testConfigDict['service']
    if 'request' in testConfigDict:
      request = testConfigDict['request']
    if not request:
      request = defaultrequest
    # run test <loop> times
    loop = 1
    if 'repeat' in testConfigDict:
      loop = testConfigDict['repeat']
    # print info
    print(horizline)
    serviceUrl = '/' + service
    print("testing '%s': %s:%s/%s\n" % (testConfigDict['serviceName'],conn.host,conn.port,service))
    if('testname' in testConfigDict):
      print("testname: %s" % testConfigDict['testname'])
    else:
      testname = testConfigDict['serviceName']
    for counter in range(loop):
      print("-I-: loop: %s/%s\n" % (counter,loop))
      if 'headers' in testConfigDict:
        testheaders = testConfigDict["headers"]
        send_request(conn,serviceUrl,request, testname = testname, headers=testConfigDict["headers"])
      else:
        send_request(conn,serviceUrl,request, testname = testname)
      print(horizline)
      print('\n')
  #</testrun loop>

  ################################################################ 
  # print results
  print("vvvvv passed vvvvvv")
  print(passedList)
  print('#' * 64)
  print("vvvvv failed vvvvv")
  print(failedList)

