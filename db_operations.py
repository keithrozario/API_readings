import mysql.connector
import time
from datetime import date, timedelta as delta_time
from datetime import datetime


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
   cur.execute('SELECT MAX(ReadingDate) from date_table')
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
       cur.execute('''INSERT INTO date_table (ReadingDate,ReadingDateStatus)
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
        cur.execute('SELECT ReadingDate from date_table ' +
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
       time_dict = {'12:00AM':1,
                '01:00AM':2,
                '02:00AM':3,
                '03:00AM':4,
                '04:00AM':5,
                '05:00AM':6,
                '06:00AM':7,
                '07:00AM':8,
                '08:00AM':9,
                '09:00AM':10,
                '10:00AM':11,
                '11:00AM':12,
                '12:00PM':13,
                '01:00PM':14,
                '02:00PM':15,
                '03:00PM':16,
                '04:00PM':17,
                '05:00PM':18,
                '06:00PM':19,
                '07:00PM':20,
                '08:00PM':21,
                '09:00PM':22,
                '10:00PM':23,
                '11:00PM':24}
       return time_dict[reading_time]


def get_reading_note (reading_value):
   #API is given int he format dddx (where ddd is a 1-3 digit number, and x is a character symbolizing the pollutant)
   #This function returns the pollutant as a single character, returning 0 if none is found
   defined_notes =["*","a","b","c","d","&"]

   if len(reading_value) == 0:
        return "0"
   
   last_char =  reading_value[-1]
   if last_char in defined_notes:
      return last_char
   else:
      return "0"

def get_reading_value_int (reading_value):
    #API is given int he format dddx (where ddd is a 1-3 digit number, and x is a character symbolizing the pollutant)
    #This function returns the xxx as an integer value
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
                                             get_reading_note(ApiReading.reading_value),
                                             get_reading_value_int(ApiReading.reading_value),
                                             "MY")
                )
        #update list in current_instances & date_list
        cur.execute('''UPDATE date_table
                        SET ReadingDateStatus = 3
                        WHERE ReadingDate = %s''',(current_url_date,))
    con.commit() #all or nothing approach
    con.close()


