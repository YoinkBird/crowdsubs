# DESCRIPTION:

import webapp2
import logging
# project-specific files
from basehandler import BaseHandler
from ndb_classes import Subtitle

class SubtitleEditHandler(BaseHandler):
  def post(self):
    subtitle_id = self.request.get('subtitle_id')
    action = self.request.get('action')
    subtitle_content = self.request.get('subtitle_content')
    if(subtitle_id and subtitle_content):
      self.create_sub(subtitle_id, subtitle_content)
  def get(self):
    # TODO: add option parsing to BaseHandler
    # assume subtitle_id is required to get to this page
    subtitle_id = self.request.get('subtitle_id')
    action = self.request.get('action')
    # maybe put this somewhere else
    subtitle_content = self.request.get('subtitle_content')

    # </end argparsing>

    # retrieve subtitle entry and contents
    subInst = Subtitle.get(subtitle_id)
    subContentStr = ''
    ## set pageView based on state of subtitle AND 'action'
    ##  e.g. 'display' is invalid if sub does not exist
    ## if !subInst or action=edit -> action=edit
    ## if  subInst  -> action=display
    pageView = "display"
    if(subInst):
      if(action):
        # if subInst && edit
        if(action == "edit"):
          pageView = "edit"
      subContentStr = subInst.content
    else:
      # if !subInst , show options for creation, suggestions, search, etc
      pageView = "create"
      #pageView = "edit" #TODO: temporary just to establish logic
      if(action):
        # if !subInst && edit
        if(action == "edit"):
          pageView = "edit"

    # view | trigger
    # ---------------
    # display | default
    # edit  | action=edit
    # save  | action=save
    import html_templates
    pageContentStr = ''
    if(pageView):
      logging.info("pageView is:" + pageView)
      if(pageView == 'edit'):
        #TODO: self.showView_edit(subtitle_id)
        pageContentStr = html_templates.get_page_template_subtitle_edit(
            action='edit?subtitle_id=' + subtitle_id + '&action=submit',
            displayText=subContentStr,
            )
      elif(pageView == 'create'):
        #TODO: self.showView_edit(subtitle_id)
        pageContentStr = html_templates.get_page_template_subtitle_create(
            title=subtitle_id,
            action='edit?subtitle_id=' + subtitle_id + '&action=edit',
            )
      else:
        pageContentStr = html_templates.get_page_template_subtitle_display(
            pageView = pageView,
            displayText=subContentStr,
            )
    #else:
      #TODO: self.showView_display(subtitle_id)

    # display page
    self.render_response(
        file='edit.html',
        values={'page_content':pageContentStr}
        )

  def create_sub(self, sub_id, content):
    newSub = Subtitle(
        id = sub_id,
        content = content,
        )
    newSub.put()

  def retrieve_sub(self, sub_id):
    foundSub = Subtitle.get(sub_id)
    return foundSub



