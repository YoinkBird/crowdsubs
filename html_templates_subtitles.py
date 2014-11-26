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

  displayText = '<p>The page for <strong>%s</strong> does not exist</p>' % title
  displayText += '<a href="%s">Create Page</a>' % action
  template = generateContainerDiv(divContent = displayText)
  return template
#</get_page_template_subtitle_create>
################################################################

################################################################
#< get_page_template_subtitle_edit>
def get_page_template_subtitle_edit(**kwargs):
  if(kwargs):
    if(not 'action' in kwargs):
      return

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']

  template = """\
  <div>
    <textarea name="subtitle_content" rows="40" cols="60">%s</textarea><br/>
  </div> 
  """
  template = template % displayText
  template = gen_html_form(
    action=kwargs['action'],
    method="post",
    #enctype="multipart/form-data",
    content=template,
    input_tag=gen_html_tag_input(type="submit", value="Save")
    )
  return template
#</get_page_template_subtitle_edit>
################################################################


################################################################
#< get_page_template_subtitle_display>
def get_page_template_subtitle_display(**kwargs):
  if(kwargs):
    if(not 'displayText' in kwargs):
      import logging
      logging.info("get_page_template_subtitle_display: displayText is not in kwargs")
      return

  displayText = ''
  if('displayText' in kwargs):
    displayText = kwargs['displayText']
  import logging
  logging.info("get_page_template_subtitle_display: displayText is:" + displayText)

  template = generateContainerDiv(divContent = displayText)
  import logging
  logging.info("get_page_template_subtitle_display: template is:" + template)
  return template
#</get_page_template_subtitle_display>
################################################################

