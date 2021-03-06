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
  textareaContent  = kwargs['textareaContent']

    
  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template_subtitle_id = """\
  <h1>Editing %s</h1>
  """
  template_json_table = """\
  <div id="subtitle_id">
    %s
  </div> 
  """

  # generate input field for subtitle name
  subtitle_id_input = gen_html_tag_input(
      type  = "text",
      # attribs = 'size=15',
      attribs = "name=subtitle_id",
      name  = title,
      value = title.title(),
      )
  template_subtitle_id = template_subtitle_id % (subtitle_id_input)

  # generate json input table
  template_json_table = template_json_table % (displayText)


  # generate plain text area
  # not sure how to make an empty table, so a textarea has to suffice for starting the subtitle
  textAreaTemplateStr = """\
  <div>
    <textarea name="subtitle_content" rows="10" cols="60">%s</textarea><br/>
  </div> 
  """
  template = textAreaTemplateStr % textareaContent

  # generate buttons for form
  buttonRow = gen_html_tag_input(type="submit", value="Save",
      css_class= get_class_dict('edit_save_btn')
      )
  buttonRow += " | "
  hrefAttribs = 'class="' + get_class_dict('edit_cancel_btn') + '"'
  buttonRow += '<a href="%s" %s>Cancel</a>' % (pageName + '?subtitle_id=' + title, hrefAttribs)

  # generate form
  form_part_subtitle_content = gen_html_form(
    action=action,
    method="post",
    #enctype="multipart/form-data",
    content= template_subtitle_id + template,
    input_tag = buttonRow,
    )
  template = template_json_table + form_part_subtitle_content
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
  translateUrl = kwargs['translateUrl']

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
  template += " | "
  hrefAttribs = 'class="' + get_class_dict('display_translate_page_btn') + '"'
  template += '<a href="%s" %s>Translate Page</a>' % (translateUrl, hrefAttribs)
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
  editUrl   = kwargs['editUrl']

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template = """\
  <h1>%s</h1>
  """
  # render buttons
  hrefAttribs = 'class="' + get_class_dict('display_translate_page_btn') + '"'
  template += '<a href="%s" %s>Create Subtitle</a>' % (editUrl, hrefAttribs)
  template += " | "
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
      'create_btn'              : button_green,
      'display_edit_page_btn'   : button_blue,
      'display_delete_page_btn' : button_red,
      'display_translate_page_btn' : button_green,
      'display_container_div'   : 'well',
      'edit_save_btn'           : button_green,
      'edit_cancel_btn'         : button_red,
      'create_create_page_btn'  : button_blue,
      'overview_subtitle_table' : "table table-striped",
      'display_subtitle_table'  : "table table-bordered table-condensed",
      'display_vote_up_btn'     : 'btn btn-xs btn-success',
      'display_vote_down_btn'   : 'btn btn-xs btn-danger',
      }

  retVal = classDict
  #if(args):
  for tagName in args:
    if(tagName in classDict):
      retVal = classDict[tagName]
  return retVal
#<def get_class_dict>
################################################################
