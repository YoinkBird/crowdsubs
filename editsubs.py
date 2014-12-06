# DESCRIPTION:

import webapp2
import logging
# project-specific files
from subtitle_api import SubtitleApiHandler
from ndb_classes import Subtitle

class SubtitleEditHandler(SubtitleApiHandler):
  # https://webapp-improved.appspot.com/guide/handlers.html?highlight=override#overriding-init
  def __init__(self, request, response):
    # Set self.request, self.response and self.app.
    self.initialize(request, response)
    self.pageRelUrl = 'subs'
  def post(self):
    self.get()
  def get(self):
    # TODO: add option parsing to BaseHandler
    # assume subtitle_id is required to get to this page
    paramDict = self.parse_options(paramList = ['subtitle_id','subtitle_content','action'])
    subtitle_id = paramDict['subtitle_id']
    subtitle_id = subtitle_id.lower()
    subtitle_content = paramDict['subtitle_content']
    action = paramDict['action']

    # </end argparsing>

    # retrieve subtitle entry and contents
    subContentStr = ''
    if(subtitle_id):
      subInst = self.retrieve_sub(subtitle_id)
      if(subInst):
        subContentStr = subInst.get_text()
    pageView = self.defineView(
        subtitle_id = subtitle_id,
        action      = action,
        )

    if(action):
      # if XsubInst && submit
      if(action == 'submit'):
        if(subtitle_id and subtitle_content):
          # HACK! but it unifies "post" and "get"
          # TODO: do this correctly somehow.
          subInst = self.create_sub(subtitle_id, subtitle_content).get()
          self.redirect("/" + self.pageRelUrl + "?subtitle_id=" + subtitle_id)
      if(action == 'vote'):
        if(subtitle_id):
          # get required params and submit
          voteDict = self.parse_options(paramList = Subtitle.get_voting_params())
          subInst = self.retrieve_sub(subtitle_id)
          subInst.updateVotes(**voteDict)
      # if XsubInst && translate
      if(action == 'translate'):
        if(subtitle_id and subContentStr):
          # http://crowdsubs.appspot.com/api?subtitle_id=test_deployment&action=translate
          respJson = self.process_json(
              subtitle_id = subtitle_id,
              subtitle_content = subContentStr,
              action = 'translate',
              )
          if(respJson):
            logging.info(respJson['subtitle_id'])
            self.redirect("/" + self.pageRelUrl + "?subtitle_id=" + respJson['subtitle_id'])
    pageConfigDict = self.showView(pageView, subtitle_id, subContentStr)

    # display page
    self.render_response(
        **pageConfigDict
        )
  # </def get>

  # <def defineView>
  def defineView(self, **kwargs):
    if(kwargs):
      if('subtitle_id' in kwargs):
        subtitle_id = kwargs['subtitle_id']
      if('action' in kwargs):
        action = kwargs['action']
    pageView = "display"
    if(subtitle_id):
      #subInst = Subtitle.get(subtitle_id)
      subInst = self.retrieve_sub(subtitle_id)
      ## set pageView based on state of subtitle AND 'action'
      ##  e.g. 'display' is invalid if sub does not exist
      ## if !subInst or action=edit -> action=edit
      ## if  subInst  -> action=display
      if(subInst):
        if(action):
          # if subInst && edit
          if(action == "vote"):
            pageView = "display"
          if(action == "edit"):
            pageView = "edit"
          if(action == "delete"):
            pageView = "delete"
      else:
        # if !subInst , show options for creation, suggestions, search, etc
        pageView = "create"
        if(action):
          # if !subInst && edit
          if(action == "edit"):
            pageView = "edit"
    elif(not subtitle_id):
      pageView = "overview"
    return pageView
  # </def defineView>


  # <def showView>
  # set template for each "view"
  # TODO: rename to 'def configureTemplate'
  def showView(self, pageView, subtitle_id, subContentStr):
    import html_templates_subtitles
    pageContentStr = ''
    templateConfigDict = {
        'file' : 'edit.html',
        'values' : {'page_content':pageContentStr}
        }
    pageContentStr = templateConfigDict['values']['page_content']
    if(pageView):
      logging.info("pageView is:" + pageView)
      requestUrl = self.pageRelUrl + '?subtitle_id=' + subtitle_id
      if(pageView == 'edit'):
        #TODO: self.showView_edit(subtitle_id)
        requestUrl = self.pageRelUrl + '?' # + 'subtitle_id=' + subtitle_id
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_edit(
            title=subtitle_id,
            pageName = self.pageRelUrl,
            action   = requestUrl + '&action=submit',
            displayText=subContentStr,
            )
      elif(pageView == 'create'):
        #TODO: self.showView_edit(subtitle_id)
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_create(
            title=subtitle_id,
            action = requestUrl + '&action=edit',
            )
      elif(pageView == "delete"):
        Subtitle.delete(subtitle_id)
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_delete(
            title=subtitle_id,
            )
      elif(pageView == "display"):
        # <debug>
        if(1):
          import html_templates
          contentStrJson = self.retrieve_sub(subtitle_id).get_json()
          import json
          contentStrJson = json.dumps(
              json.loads(contentStrJson),
              sort_keys=True, indent=4)
          contentStrJson = '<pre>' + contentStrJson + '</pre>'
          if(contentStrJson):
            contentStrJson = html_templates.generateContainerDiv(divContent = contentStrJson)
            contentStrJson = "TESTING INFO - json:<br/>\n" + contentStrJson
            contentStrJson = html_templates.generateContainerDivBlue(contentStrJson)
            #subContentStr = contentStrJson + subContentStr
        # </debug>
        # <gen html table>
        if(1):
          templateStrTableHtml = self.renderSubDisplayView(
              subtitle_id = subtitle_id,
              bodyList = self.retrieve_sub(subtitle_id).get_2d_list(),
              )
        # </gen html table>
        #<gen code for javascript table>
        if(1):
          tableConfigDict = self.retrieve_sub(subtitle_id).get_table_config_dict()
          # add up/downvote links
          tableConfigDict = self.modifySubtitleTable(tableConfigDict = tableConfigDict)
          #DEBUG: 'indent = 4' is for debugging generated JavaScript
          segmentContentStr =  json.dumps(tableConfigDict, indent=4)
          templateStrTableHandsonJS = self.render_template(
              file   = 'handsontable.html',
              values = {'tableJson':segmentContentStr},
              )
        #</gen code for javascript table>
        subContentStr = templateStrTableHandsonJS + templateStrTableHtml
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_display(
            title=subtitle_id,
            editUrl   = requestUrl + '&action=edit',
            deleteUrl = requestUrl + '&action=delete',
            translateUrl = requestUrl + '&action=translate',
            displayText=subContentStr,
            )
        pageContentStr = pageContentStr + contentStrJson
      else: # (pageView == 'overview'):
        import html_templates
        outString = html_templates.generateTableRow(["Name","Lines","Sample"])

        allModels = Subtitle.get_all().fetch()
        for model in allModels:
          subtitle_id = model.get_id_string()
          relUrl = self.pageRelUrl + '?subtitle_id=' + subtitle_id
          summaryList = []
          # generate table-row of links to subtitle page
          for hrefTxt in model.get_summary():
            summaryList.append(
                html_templates.gen_html_ahref(href = relUrl, content = hrefTxt)
                )
          outString += html_templates.generateTableRow(summaryList)

        # generate table
        outString = html_templates.generateTable(
            content = outString,
            attribs = "border=1 cellspacing=0 cellpadding=5  class=\"" + html_templates_subtitles.get_class_dict('overview_subtitle_table') + "\""
            )
        # generate page html
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_overview(
            title       ="Overview of Subtitles",
            displayText = outString,
            )

    templateConfigDict['values']['page_content'] = pageContentStr
    return templateConfigDict
  # </def showView>

  # <def renderSubDisplayView>
  def renderSubDisplayView(self, **kwargs):
    import html_templates
    import html_templates_subtitles
    bodyList = []
    subtitle_id = ''
    if(kwargs):
      if('bodyList' in kwargs):
        bodyList = kwargs['bodyList']
      if('subtitle_id' in kwargs):
        subtitle_id = kwargs['subtitle_id']
    # add voting buttons
    for row in bodyList:
      # modify 'rev_id' column
      if(subtitle_id):
        rev_id = row[4]
        voteLinkTxt = self.generateVoteLinks(
            subtitle_id = subtitle_id,
            line_id     = row[0],
            rev_id      = row[4],
            )
        row[4] = voteLinkTxt + " " + rev_id
    # generate table
    tableString = html_templates.generateTableFrom2dList(
        headerList = ["line_id","time","txt","votes","vote on rev"],
        bodyList = bodyList,
        attribs = "class=\"" + html_templates_subtitles.get_class_dict('display_subtitle_table') + "\""
        )
    subContentStr = tableString
    return tableString
  # </def renderSubDisplayView>

  # <def generateVoteLinks>
  def generateVoteLinks(self, **kwargs):
    import html_templates
    import html_templates_subtitles
    #<argparse>
    if(kwargs):
      for requiredParam in ('subtitle_id', 'line_id', 'rev_id'):
        if(requiredParam not in kwargs):
          return
    subtitle_id = kwargs['subtitle_id']
    line_id     = kwargs['line_id']
    rev_id      = kwargs['rev_id']
    #</argparse>
    #<generate html links>
    voteLinkTxt = ''
    baseVoteQueryParam = 'subs?subtitle_id=%s&action=vote&line_id=%s&rev_id=%s&vote=' % (kwargs['subtitle_id'], kwargs['line_id'], kwargs['rev_id'])
    voteLinkTxt += html_templates.gen_html_ahref(
        attribs = 'class = "' + html_templates_subtitles.get_class_dict('display_vote_up_btn') + '"',
        href = baseVoteQueryParam + "up", content = "[+]",)
    voteLinkTxt += ' / '
    voteLinkTxt += html_templates.gen_html_ahref(
        attribs = 'class = "' + html_templates_subtitles.get_class_dict('display_vote_down_btn') + '"',
        href = baseVoteQueryParam + "down", content = "[-]",)
    #</generate html links>
    return voteLinkTxt
  # </def generateVoteLinks>

  # <def modifySubtitleTable>
  def modifySubtitleTable(self, **kwargs):
    tableConfigDict = {} #self.retrieve_sub(subtitle_id).get_table_config_dict()
    if(kwargs):
      if('tableConfigDict' in kwargs):
        tableConfigDict = kwargs['tableConfigDict']
    #</argparse>
    #<do stuff>
    subtitle_id = tableConfigDict['subtitle_id']
    for lineDict in tableConfigDict['data']:
      #<check required vars>
      if(lineDict):
        for requiredParam in ('line_id', 'rev_id'):
          if(requiredParam not in lineDict):
            return
      line_id     = lineDict['line_id']
      rev_id      = lineDict['rev_id']
      #</check required vars>
      rev_id = lineDict['rev_id']
      voteLinkTxt = self.generateVoteLinks(
          subtitle_id = subtitle_id,
          line_id     = line_id,
          rev_id      = rev_id,
          )
      voteLinkTxt = voteLinkTxt + " " + rev_id
      lineDict['rev_id'] = voteLinkTxt
    return tableConfigDict
  # </def modifySubtitleTable>

  def create_sub(self, sub_id, content):
    sub_id = sub_id.lower()
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



