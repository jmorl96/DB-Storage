# -*- coding: utf-8 -*-
"""
Created on Sun Feb  14 21:20:13 2021

@author: jmorl96
"""

#libraries

import os
import cx_Oracle
import csv
from google.cloud import storage

## GCP project access credentials. You can delete this two lines if you have already configure this credentials in your machine.
credential_path = "service_account_key.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path



#Oracle Database Connection
host = 'myhost.com'
port = 'myport'
sid = 'mySid'
user = 'myUsername'
password = 'myPassword'
encoding = 'UTF-8' # encoding of the database


dsn_tns = cx_Oracle.makedsn(host, port, sid)
orcl = cx_Oracle.connect(user = user, password= password, encoding = encoding, dsn=dsn_tns)

printHeader = True # Include table headers


#In this variable we have to write the name of the tables we want to export from Oracle DB to GC Storage
tables = [
        "Table1",
        "Table2",
        "Table3",
        "Table4",
        "Table5",
        "Table6"
          ]

for tableName in tables: # We are going to loop the tables in the variable
    print(tableName)
    # Its created a .csv file to store the table locally untill we upload it to Storage
    csv_file_dest = tableName + ".csv"
    outputFile = open(csv_file_dest,'w',newline='',encoding='utf-8') # 'wb'
    output = csv.writer(outputFile, dialect='excel')
    #SQL Consult for downloading the table
    sql = "select * from " + tableName
    curs2 = orcl.cursor()
    curs2.execute(sql)

    if printHeader: # Insert Headers
        cols = []
        for col in curs2.description:
            cols.append(col[0])
        output.writerow(cols)

    for row_data in curs2: # Insert Rows
        output.writerow(row_data)

    outputFile.close()

    #Open Google Cloud Storage client
    storage_client = storage.Client()
    #Specify your the name of your Bucket
    bucket = storage_client.get_bucket('Bucket')
    #Specify your the path where you want to upload the file
    folder = 'path/'
    blob = bucket.blob(folder + csv_file_dest)
    #Specify your project's name
    project_name = 'gcp_project'
    
    #Upload
    blob.upload_from_filename(csv_file_dest)

    print('File {} uploaded to {}.'.format(csv_file_dest,project_name))
