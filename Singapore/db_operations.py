import mysql.connector
import time
from datetime import datetime
from datetime import date, timedelta as delta_time


def get_db_config ():
   config = {
     'user': 'keith',
     'password': 'root',
     'host': '127.0.0.1',
     'database':'apireading',
     'raise_on_warnings': True}
   return config

#get-last-date-from-db
def initialize_db():
   config = get_db_config()   
   con = mysql.connector.connect(**config)
   cur = con.cursor()
   cur.execute('SELECT MAX(ReadingDate) from date_tablesg')
   rows = cur.fetchone()
   last_date_in_db =  rows[0]

   default_status = 0

   #get number of 
   todaysdate = date.today()
   delta = todaysdate - last_date_in_db

   #insert-up-to-current-date 
   for i in range(delta.days-1): #current date not taken, data for today is still being collected, so we'll skip today, and leave it for tomorrow.
       current_url_date = str(last_date_in_db + delta_time(days=(i+1)))
       print current_url_date
       cur.execute('''INSERT INTO date_tablesg (ReadingDate,ReadingDateStatus)
                                               VALUES(%s,%s)''',
                                               (current_url_date,
                                                default_status))

   con.commit()
   con.close()


def get_date():
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()
    
    
    while True:
        time.sleep(2)
        #get the earliest date from the ReadingDate table where status =0 (un-read)
        cur.execute('SELECT ReadingDate from date_tablesg ' +
                'WHERE ReadingDateStatus = 0 ' + 
                'ORDER BY ReadingDate asc ' +
                'Limit 1')
        rows = cur.fetchone()
        if rows == None:
            #re-initialize cursor, not sure why I have to do this, but it HAS to be done.
            con.close() 
            con = mysql.connector.connect(**config)
            cur = con.cursor()
            print "No Dates Available"
        else:
            con.close()
            
            return rows[0]


def convert_time (reading_time):
   reading_ascii = reading_time.encode('ascii','ignore')
   time_dict = {'12am':25, #set to 25 so that we can move this to the 'next day later'
                '1am':2,
                '2am':3,
                '3am':4,
                '4am':5,
                '5am':6,
                '6am':7,
                '7am':8,
                '8am':9,
                '9am':10,
                '10am':11,
                '11am':12,
                '12pm':13,
                '1pm':14,
                '2pm':15,
                '3pm':16,
                '4pm':17,
                '5pm':18,
                '6pm':19,
                '7pm':20,
                '8pm':21,
                '9pm':22,
                '10pm':23,
                '11pm':24}
   return time_dict[reading_ascii]


def get_reading_value_int (reading_value):

    value_length = len(reading_value)
    

    if reading_value.isdigit() :
        
        return reading_value
    else:
        new_value = reading_value[:(value_length -1)]
        if new_value.isdigit() :
            return new_value
        else:
            return "0"    
   
   

def write_list_to_db (datalist,current_url_date): #list of ApiReading objects to be written to database


    
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()
    print "Cursor setup"
    for ApiReading in datalist:
        cur.execute('''INSERT INTO readings (ReadingDate,
                                             ReadingTime,
                                             Region,
                                             ReadingValue,
                                             ReadingNote,
                                             ReadingValue_int,
                                             CountryCode
                                            )
                                            VALUES(%s,%s,%s,%s,%s,%s,%s)''',
                                            (ApiReading.reading_date,
                                             convert_time(ApiReading.reading_time),
                                             ApiReading.region,
                                             ApiReading.reading_value,
                                             "25",
                                             get_reading_value_int(ApiReading.reading_value),
                                             "SG")
                )
   #update list in current_instances & date_list
    
    cur.execute('''UPDATE date_tablesg
                     SET ReadingDateStatus = 3
                     WHERE ReadingDate = %s''',(current_url_date,))
   #to standardize with Malaysia, we take the 12:00am to be the 'next day' data
    
    cur.execute('''UPDATE readings
                    SET ReadingDate = DATE_ADD(readingDate,INTERVAL 1 DAY), ReadingTime = 1
                    WHERE ReadingTime = 25 AND readingDate = %s''',(current_url_date,))
        
    con.commit() #all or nothing approach
    print "Update DB for  " + current_url_date
    con.close()
