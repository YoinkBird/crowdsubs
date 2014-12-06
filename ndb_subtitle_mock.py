# DESCRIPTION:

import webapp2
import logging

###############################################################################
# <class_MockSubtitle>
class MockSubtitle():
  # <def get_table_config_dict>
  # Mock function to simulate data returned from ndb_classes.get_table_config_dict
  # usage: 
  '''
  from ndb_subtitle_mock import MockSubtitle
  templateConfigDict['values']['tableJson'] = json.dumps(MockSubtitle.get_table_config_dict(),indent=4)
  '''
  @classmethod
  def get_table_config_dict(self, **kwargs):
    # title of columns
    tableColHeaders = ["line_id", "time", "txt", "votes"]
    # columns to display + attribs
    tableColumns = [
        {
          "data" : "line_id",
          "readOnly" : "true"
          },
        {
          "data" : "time"
          },
        {
          "data" : "txt"
          },
        {
          "data" : "votes"
          }
        ]
    tableDataList = [
        {"line_id": "001", "time": "1:04", "txt": "black", "votes": 9},
        {"line_id": "002", "time": "1:06", "txt": "blue", "votes": -1},
        {"line_id": "003", "time": "1:08", "txt": "yellow", "votes": 3},
        {"line_id": "004", "time": "1:12", "txt": "white", "votes": 1},
        {"votes": 1, "line_id": "005", "time": "1:16", "txt": "dict-code out of order"},
        {"votes": 1, "line_id": "005", "txt": "dict-code missing time"},
        {"line_id": "006", "time": "1:12", "txt":"dict-code too many entries", "votes": 1, "rev_id":"001"}
        ]
    '''
    if(0):
      tableDataList = '[ {line_id: "001", time: "1:04", txt: "black", votes: 9},\n\
                    {line_id: "002", time: "1:06", txt: "blue", votes: -1},\n\
                    {line_id: "003", time: "1:08", txt: "yellow", votes: 3},\n\
                    {line_id: "004", time: "1:12", txt: "white", votes: 1},\n\
                    {line_id: "005", time: "1:12", txt: "static", votes: 1}\n\
          ]\
          '
    '''
    tableConfigDict = {
        'data'       : tableDataList,
        'colHeaders' : tableColHeaders,
        'columns'    : tableColumns,
        }
    return tableConfigDict
  # </def get_table_config_dict>
# </class_MockSubtitle>
###############################################################################
