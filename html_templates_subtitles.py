import json

from html_templates import *
################################################################
#< get_page_template_subtitle_create>
def get_page_template_subtitle_create(**kwargs):
  if(kwargs):
    if(not 'action' in kwargs):
      return
  title = kwargs['title']
  action = kwargs['action']

  template = """\
  <h1>%s Not Found</h1>
  """
  template = template % title.title()

  displayText = '<p>The page for <strong>%s</strong> does not exist</p>' % title
  hrefAttribs = 'class="' + get_class_dict('create_create_page_btn') + '"'
  displayText += '<a href="%s" %s>Create Page</a>' % (action , hrefAttribs)
  template += generateContainerDiv(divContent = displayText)
  return template
#</get_page_template_subtitle_create>
################################################################

################################################################
#< get_page_template_subtitle_delete>
def get_page_template_subtitle_delete(**kwargs):
  if(kwargs):
    if(not 'title' in kwargs):
      return
  title = kwargs['title']

  template = """\
  <h1>%s Not Found</h1>
  """
  template = template % title.title()

  displayText = '<p>The page for <strong>%s</strong> has been deleted.</p>' % title
  template += generateContainerDiv(divContent = displayText)
  return template
#</get_page_template_subtitle_delete>
################################################################


################################################################
#< get_page_template_subtitle_edit>
def get_page_template_subtitle_edit(**kwargs):
  if(kwargs):
    if(not 'action' in kwargs):
      return
  title = kwargs['title']
  pageName=kwargs['pageName']
  action=kwargs['action']

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template = """\
  <h1>Editing %s</h1>
  <div>
    <textarea name="subtitle_content" rows="10" cols="60">%s</textarea><br/>
  </div> 
  """
  template = template % (title.title(), displayText)
  buttonRow = gen_html_tag_input(type="submit", value="Save",
      css_class= get_class_dict('edit_save_btn')
      )
  buttonRow += " | "
  hrefAttribs = 'class="' + get_class_dict('edit_cancel_btn') + '"'
  buttonRow += '<a href="%s" %s>Cancel</a>' % (pageName + '?subtitle_id=' + title, hrefAttribs)
  template = gen_html_form(
    action=action,
    method="post",
    #enctype="multipart/form-data",
    content=template,
    input_tag = buttonRow,
    )
  return template
#</get_page_template_subtitle_edit>
################################################################

################################################################
#< get_page_template_subtitle_display>
def get_page_template_subtitle_display(**kwargs):
  if(kwargs):
    if(not 'displayText' in kwargs):
      return
  title     = kwargs['title']
  editUrl   = kwargs['editUrl']
  deleteUrl = kwargs['deleteUrl']

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template = """\
  <h1>%s</h1>
  """
  template = template % title.title()
  # render buttons
  hrefAttribs = 'class="' + get_class_dict('display_edit_page_btn') + '"'
  template += '<a href="%s" %s>Edit Page</a>' % (editUrl, hrefAttribs)
  template += " | "
  hrefAttribs = 'class="' + get_class_dict('display_delete_page_btn') + '"'
  template += '<a href="%s" %s>Delete Page</a>' % (deleteUrl, hrefAttribs)
  # surround in div
  template += generateContainerDiv(
      divContent = displayText,
      css_class = get_class_dict('display_container_div')
      )
  return template
#</get_page_template_subtitle_display>
################################################################

################################################################
#< get_page_template_subtitle_overview>
def get_page_template_subtitle_overview(**kwargs):
  if(kwargs):
    if(not 'displayText' in kwargs):
      return
  title = kwargs['title']

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template = """\
  <h1>%s</h1>
  """
  template = template % title.title()
  template += displayText
  return template
#</get_page_template_subtitle_overview>
################################################################

################################################################
#<def get_class_dict>
def get_class_dict(*args):
  # http://getbootstrap.com/examples/theme/
  button_blue  = 'btn btn-primary'
  button_red   = 'btn btn-danger'
  button_green = 'btn btn-success'
  classDict = {
      'display_edit_page_btn'   : button_blue,
      'display_delete_page_btn' : button_red,
      'display_container_div'   : 'well',
      'edit_save_btn'           : button_green,
      'edit_cancel_btn'         : button_red,
      'create_create_page_btn'  : button_blue,
      'overview_subtitle_table' : "table table-striped",
      }

  retVal = classDict
  #if(args):
  import logging
  logging.info(args)
  for tagName in args:
    if(tagName in classDict):
      retVal = classDict[tagName]
  return retVal
#<def get_class_dict>
################################################################
