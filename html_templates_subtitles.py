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
  displayText += '<a href="%s">Create Page</a>' % action
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
    <textarea name="subtitle_content" rows="40" cols="60">%s</textarea><br/>
  </div> 
  """
  template = template % (title.title(), displayText)
  template = gen_html_form(
    action=action,
    method="post",
    #enctype="multipart/form-data",
    content=template,
    input_tag=gen_html_tag_input(type="submit", value="Save")
    )
  template += '<a href="%s">Cancel</a>' % (pageName + '?subtitle_id=' + title)
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
  template += '<a href="%s">Edit Page</a>' % editUrl
  template += " | "
  template += '<a href="%s">Delete Page</a>' % deleteUrl
  template += generateContainerDiv(divContent = displayText)
  return template
#</get_page_template_subtitle_display>
################################################################

