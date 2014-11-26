# DESCRIPTION:

import webapp2
import logging
# project-specific files
from basehandler import BaseHandler
from ndb_classes import Subtitle

class SubtitleEditHandler(BaseHandler):
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
    pageContentStr = self.showView(pageView, subtitle_id, subContentStr)

    # display page
    self.render_response(
        file='edit.html',
        values={'page_content':pageContentStr}
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
  def showView(self, pageView, subtitle_id, subContentStr):
    import html_templates_subtitles
    pageContentStr = ''
    if(pageView):
      logging.info("pageView is:" + pageView)
      requestUrl = self.pageRelUrl + '?subtitle_id=' + subtitle_id
      if(pageView == 'edit'):
        #TODO: self.showView_edit(subtitle_id)
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
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_display(
            title=subtitle_id,
            editUrl   = requestUrl + '&action=edit',
            deleteUrl = requestUrl + '&action=delete',
            displayText=subContentStr,
            )
      else: # (pageView == 'overview'):
        outString = "Name | Content<br/>\n"
        allModels = Subtitle.get_all().fetch()
        import html_templates

        for model in allModels:
          subtitle_id = model.get_id_string()
          relUrl = self.pageRelUrl + '?subtitle_id=' + subtitle_id
          aHrefUrl1 =  html_templates.gen_html_ahref(href = relUrl, content = subtitle_id)
          aHrefUrl2 = html_templates.gen_html_ahref(href = relUrl, content = model.get_text())
          outString += aHrefUrl1 + " | " + aHrefUrl2 + "<br/>\n"

        pageContentStr = html_templates_subtitles.get_page_template_subtitle_overview(
            title       ="Overview of Subtitles",
            displayText = outString,
            )

    return pageContentStr
  # </def showView>

  def create_sub(self, sub_id, content):
    newSub = Subtitle(
        id = sub_id,
        content = content,
        )
    return newSub.put()

  def retrieve_sub(self, sub_id):
    foundSub = Subtitle.get(sub_id)
    return foundSub



