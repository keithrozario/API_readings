from __future__ import generators    # needs to be at the top of your module
import mysql.connector
import time

# This code require Python 2.2.1 or later

def ResultIter(cursor, arraysize=100):
    'An iterator that uses fetchmany to keep memory usage down'
    while True:
        results = cursor.fetchmany(arraysize)
        if not results:
            break
        for result in results:
            yield result

def get_db_config ():
   config = {
     'user': 'keith',
     'password': 'root',
     'host': '127.0.0.1',
     'database':'apireading',
     'raise_on_warnings': True,
     'buffered' : True}
   return config


def get_data_from_db(rowid):
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor(buffered = True)
    print "Getting data for : " + str(rowid)
    query = 'SELECT * FROM apireading WHERE regioncode = ' + str(rowid)
    cur.execute(query,rowid)
    rows = list()
    
##    for result in ResultIter(cur):
##       con.ping(True)
##       rows.append(result)
    rows = cur.fetchall()
    
    con.close()
    return rows

def get_regions():
    config = get_db_config()
    con = mysql.connector.connect(**config)
    cur = con.cursor()
    cur.execute('SELECT Region,ROWID from ref_region')
    rows = cur.fetchall()
    con.close()
    return rows

def write_file(rows,region):
    output_file_name = region + ".csv"
    output_file = open(output_file_name, 'w')
    delimiter = ":"
    output_file.write("Region Code" + delimiter +
                      "Region Name" + delimiter +
                      "Date" + delimiter +
                      "Hour (1-24)" + delimiter +
                      "Reading Value" + delimiter +
                      "Reading Note" +
                      "\n")
    for each_row in rows:
        output_string = ""
        for each_element in each_row:
            output_string = output_string + str(each_element) + delimiter
        output_file.write(output_string + "\n")
        #print output_string


region_list = get_regions()
print "starting"
for each_region in region_list:
    rows = get_data_from_db(each_region[1])
    print "Now writing to file"
    write_file(rows, each_region[0])


