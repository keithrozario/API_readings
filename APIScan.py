from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import time
import sys

#custom scripts
from db_operations import initialize_db, get_date , write_list_to_db

from html_operations import getHeaders, strip_html,create_url_list,get_html


class ApiReading(object):
   def __init__(self, y0, y1, y2, y3, y4):
      self.reading_date = y0
      self.state = y1
      self.region = y2
      self.reading_time = y3
      self.reading_value = y4


def get_datalist(html_output, current_url_date):
    class_of_table = "table1" #div class of table with the data
    data_list = []
    soup = BeautifulSoup(html_output)
    table_html =soup.find('table', attrs={'class':class_of_table})
    # grabs the top row
    rows = table_html.findAll('tr')
    is_Header_Row = True #set this to true, before entering for loop below, the first row is the header row
    #loop through al the rows
    for tr in rows:
          if is_Header_Row:
                  headers = getHeaders(tr) #get the headers from the first row
                  is_Header_Row = False #set it to fail the if check before all data rows (only first row is header row)
          else:
                  cols = tr.findAll('td')
                  location_columns = []
                  data_row = ''
                  column_count = 0
                  
                  for td in cols:
                        if column_count < 2 :
                                location_columns.append( td.text.strip() )
                                                                                        
                        else:
                                data = ApiReading(current_url_date, 
                                                  location_columns[0], #State
                                                  location_columns[1], #Region/Town..etc
                                                  str(headers[column_count]), #Time--taken from the header of the column -- modified before insertion into DB
                                                  strip_html(td.text.strip())) #reading itself -- modified before insertion into DB
                                data_list.append(data)
                                
                        column_count = column_count + 1
    return data_list

def main():
        
        initialize_db()             
        met_dept_api_url_list = create_url_list() #get the url_list (refer to html_operations.py for the hardcoded values)
                       
        while True:
            current_url_date = get_date() #looks for a data assigned to this process id, repeats every 2 seconds till there is an assignment
            data_list = []
            webpage_htmls = get_html (met_dept_api_url_list, current_url_date) #gets the webpage of the url in url_list          

            if (webpage_htmls == None):
                print "There was an error getting the html files, retrying in 1 minute"
                time.sleep(60)
            else: #successfully got the html of the 4 urls
                for html_output in webpage_htmls:
                    html_datalist = get_datalist(html_output, current_url_date)
                    data_list = data_list + html_datalist
                print "Great Stuff--writing this to the DB"
                write_list_to_db(data_list,current_url_date)
        
       
if __name__ == "__main__":
   main()




