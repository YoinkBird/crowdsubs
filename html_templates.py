import json

################################################################
#< def generateContainerDiv>
#TODO: add kwargs and a 'header' option
#TODO: convert all calls to use kwargs style
def generateContainerDiv(**kwargs):
  bgcolor = ''
  divContent = ''
  divStyle = "border-style:solid;border-width:1px;padding:0.5em 0.5em 0.5em 0.5em;"
  html_attrib_list = []
  if(kwargs):
    if('divContent' in kwargs):
      divContent = kwargs['divContent']
    if('title' in kwargs):
      titleP = '<p style="font-weight:bold">%s</p>' % kwargs['title']
      divContent = titleP + divContent
    if('bgcolor' in kwargs):
      bgcolor = kwargs['bgcolor']
    if('css_class' in kwargs):
      html_attrib_list.append('class="%s"' % kwargs['css_class'])
      divStyle = ''
  if(bgcolor):
    divStyle += "background-color:%s;" % bgcolor
  if(divStyle):
    html_attrib_list.append('style="%s"' % divStyle)
  tagAttribs = ' '.join(html_attrib_list)
  handlerContainer = '<div %s>%s</div>' % (tagAttribs, divContent )
  return handlerContainer
#</def generateContainerDiv>
################################################################

################################################################
#< def generateContainerDivBlue>
#TODO: add kwargs and a 'header' option
#TODO: i guess this means inheritance would be nice
def generateContainerDivBlue(divContent):
  divColor = 'lightsteelblue' # reference: http://www.w3schools.com/html/html_colornames.asp
  return generateContainerDiv(divContent = divContent, bgcolor = divColor)
#</def generateContainerDivBlue>
################################################################

################################################################
#< generateTableRow>
def generateTableRow(list):
  tableRow = ''
  for td in list:
    #tmplink = '<a href=%s>%s</a>' % (navDict[param], param)
    tmptd   = '<td>%s</td>' % td
    tableRow += tmptd
    #del tmplink
    del tmptd
  tableRow = '<tr>\n  %s\n</tr>' % tableRow
  return tableRow
#</generateTableRow>
################################################################

################################################################
#< generateTable>
def generateTable(**kwargs):
  attribs = "border=1 cellspacing=0"
  if(kwargs):
    if('content' in kwargs):
      tableRows = kwargs['content']
    if('attribs' in kwargs):
      attribs = kwargs['attribs']
  template = """\
    <table %s>
        %s
    </table>
      """
  return template % (attribs, tableRows)
#</generateTable>
################################################################

################################################################
#<generateTableFrom2dList>
# render table to display table and revisions
def generateTableFrom2dList(**kwargs):
  bodyList = []
  headerList  = []
  if(kwargs):
    if('headerList' in kwargs):
      headerList = kwargs['headerList']
    if('bodyList' in kwargs):
      bodyList = kwargs['bodyList']
  import html_templates
  import html_templates_subtitles
  tableRows = ""
  tableRows = html_templates.generateTableRow(headerList)
  for tmpTableRow in bodyList:
    tableRows += html_templates.generateTableRow(tmpTableRow)
  tableString = html_templates.generateTable(
      content = tableRows,
      **kwargs
      )
  return tableString
#<generateTableFrom2dList>
################################################################

################################################################
#< def html_generate_body_template>
# TODO: kwargs, make title optional, etc
def gen_html_body_template(titleText,bodyHtml):
  html = \
    '''
    <html>
      <head>
        <title>%s</title>
      </head>
      <body>
        %s
      </body>
    </html>
    '''
  htmlOutPut = (html % (titleText,bodyHtml))
  return htmlOutPut
#</def html_generate_body_template>
################################################################


################################################################


################################################################
#<def gen_html_ahref>
def gen_html_ahref(**kwargs):
  content = ''
  html_attrib_list = []
  if(kwargs):
    if('href' in kwargs):
      html_attrib_list.append('href="%s"' % kwargs['href'])
    if('content' in kwargs):
      content = kwargs['content']

  tagName = "a"
  tagAttribs = tagName + " " + ' '.join(html_attrib_list)
  html = '<%s>%s</%s>' % (tagAttribs, content, tagName)
  return html
#</def gen_html_ahref>
################################################################


#< def gen_html_tag_input>
def gen_html_tag_input(**kwargs):
  html_attrib_list = []
  if(kwargs):
    if('type' in kwargs):
      html_attrib_list.append('type="%s"' % kwargs['type'])
    if('css_class' in kwargs):
      html_attrib_list.append('class="%s"' % kwargs['css_class'])
    if('value' in kwargs):
      html_attrib_list.append('value="%s"' % kwargs['value'])
  inputTagAttribs = ' '.join(html_attrib_list)
  html_input = '<input %s>' % (inputTagAttribs)
  return html_input
#</def gen_html_tag_input>
################################################################


################################################################
# < def_gen_html_tag_input_submit>
def gen_html_tag_input_submit(name,value):
  inputTagSubmit = gen_html_tag_input(type="submit", name=name, value=value)
  return inputTagSubmit 
# </def_gen_html_tag_input_submit>
################################################################

################################################################
# < def_gen_html_tag_input_checkbox>
def gen_html_tag_input_checkbox(name,value):
  inputTagCheckbox = gen_html_tag_input(type="checkbox", name=name, value=value)
  return inputTagCheckbox
# </def_gen_html_tag_input_checkbox>
################################################################


################################################################
#< def gen_html_form>
# gen_html_form(
#   action="<formprocessor>",
#   method="post",
#   enctype="multipart/form-data",
#   content=<form fields>
#   input_tag=gen_html_tag_input(value='Subscribe', css_class='btn btn-primary')
#   )
def gen_html_form(**kwargs):
  html_attrib_list = []
  input_tag = ''
  if(kwargs):
    if('action' in kwargs):
      html_attrib_list.append('action="%s"' % kwargs['action'])
    if('method' in kwargs):
      html_attrib_list.append('method="%s"' % kwargs['method'])
    if('enctype' in kwargs):
      html_attrib_list.append('enctype="%s"' % kwargs['enctype'])
    if('css_class' in kwargs):
      html_attrib_list.append('class="%s"' % kwargs['css_class'])
    if('content' in kwargs):
      content = kwargs['content']
    if('input_tag' in kwargs):
      input_tag = kwargs['input_tag']
  formAttribs = ' '.join(html_attrib_list)
 
  html_form = '<form %s>\n  %s\n  %s\n</form>\n' % (formAttribs, content,input_tag)
  return html_form
#</def gen_html_form>
################################################################

