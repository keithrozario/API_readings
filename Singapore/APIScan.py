from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
import time
import sys

#custom scripts
from db_operations import  initialize_db, get_date, write_list_to_db
from html_operations import getHeaders, strip_html,get_html


class ApiReading(object):
   def __init__(self, y0, y1, y2, y3, y4):
      self.reading_date = y0
      self.state = y1
      self.region = y2
      self.reading_time = y3
      self.reading_value = y4

def print_ApiReading (data):
   print str(data.reading_date) + " " + data.state + " " + data.region + " " + data.reading_time + " " + data.reading_value

def get_datalist(html_output, current_url_date):
    class_of_table = "table1" #div class of table with the data
    data_list = []
    location_columns = []
    soup = BeautifulSoup(html_output)
    table_html =soup.find('table', attrs={'class':'text_psinormal'})
    #grabs all tr in table 'text_psinormal'
    rows = table_html.findAll('tr')
    #rows[0] is useless header
    
    #rows[1], second row i table, contains location names
    locations = rows[1].findChildren('th')
    for each_location in locations:
          location_columns.append(each_location.text.strip())

    #rows[2] to rows[26] is the 24 hour readings :)   
    for count in range(2,26):
       #grab all columns from each row
       cols = rows[count].findAll('td')
       #cols[0] is the time
       spans = cols[0].find_all('span')
       time = spans[0].text
       #cols[1] to cols[6] is the actual reading data (neglect column 7)
       for nested_count in range (1,6):
          data = ApiReading (current_url_date, 
                             "Singapore", #State
                             location_columns[nested_count-1], #Region/Town..etc
                             time, #Time--taken from the header of the column -- modified before insertion into DB
                             strip_html(cols[nested_count].text.strip())) #reading itself -- modified before insertion into DB
          #print_ApiReading(data)
          data_list.append(data)
       
               
    return data_list

def main():
        
        initialize_db()     
        met_dept_api_url = "http://www.haze.gov.sg/haze-updates/historical-psi-readings/" 
       
        while True:
            current_url_date = get_date() #gets the first date unprocessed in the db
            
            data_list = []
            webpage_html = get_html (met_dept_api_url, current_url_date) #gets the webpage of the url in url_list
            if (webpage_html == None):
                print "There was an error getting the html files, retrying in 1 minute"
                time.sleep(60)
            else: #successfully got the html of the url
                data_list = get_datalist(webpage_html, current_url_date)
                print "Great Stuff--writing this to the DB"
                write_list_to_db(data_list,current_url_date) #this marks the date as processed in the db
                print "Done"
       
if __name__ == "__main__":
   main()




