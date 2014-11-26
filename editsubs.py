# DESCRIPTION:

import webapp2
import logging
# project-specific files
from basehandler import BaseHandler
from ndb_classes import Subtitle

class SubtitleEditHandler(BaseHandler):
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

    if(action):
      # if XsubInst && submit
      if(action == 'submit'):
        if(subtitle_id and subtitle_content):
          # HACK! but it unifies "post" and "get"
          # TODO: do this correctly somehow.
          logging.info("submitting sub")
          subInst = self.create_sub(subtitle_id, subtitle_content).get()
          logging.info("subInst is updated: " + subInst.content)
          self.redirect('/edit?subtitle_id=' + subtitle_id)
          subContentStr = subInst.content

    # view | trigger
    # ---------------
    # display | default
    # edit  | action=edit
    # save  | action=save
    import html_templates_subtitles
    pageContentStr = ''
    if(pageView):
      logging.info("pageView is:" + pageView)
      if(pageView == 'edit'):
        #TODO: self.showView_edit(subtitle_id)
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_edit(
            title=subtitle_id,
            action='edit?subtitle_id=' + subtitle_id + '&action=submit',
            displayText=subContentStr,
            )
      elif(pageView == 'create'):
        #TODO: self.showView_edit(subtitle_id)
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_create(
            title=subtitle_id,
            action='edit?subtitle_id=' + subtitle_id + '&action=edit',
            )
      else:
        pageContentStr = html_templates_subtitles.get_page_template_subtitle_display(
            title=subtitle_id,
            action='edit?subtitle_id=' + subtitle_id + '&action=edit',
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
    return newSub.put()

  def retrieve_sub(self, sub_id):
    foundSub = Subtitle.get(sub_id)
    return foundSub



