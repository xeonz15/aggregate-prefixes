#!/usr/bin/python3

import sys
import os
import pymysql
from aggregate_prefixes import aggregate_prefixes

filepath = sys.argv[1]
SourceAS = sys.argv[2]
ASPrefixesFile = "Aggregated.txt"

dbhost = "localhost"
dbuser = "root"
dbpass = ""
dbname = "test"


def init_db():
  mydb = pymysql.connect(dbhost, dbuser, dbpass, dbname)

  mycursor = mydb.cursor()
  
  sql = "drop table prefixes"
  mycursor.execute(sql)
  sql = "create table prefixes(prefix_id INT NOT NULL AUTO_INCREMENT, prefix VARCHAR(100) NOT NULL, PRIMARY KEY (prefix_id));"
  mycursor.execute(sql)
  mydb.commit()


def upload_to_db(prefix):
  mydb = pymysql.connect('localhost', 'root','', 'test')

  mycursor = mydb.cursor()
  
  sql = "INSERT INTO prefixes (prefix) values ('"+prefix+"')"
  #print (sql)
  mycursor.execute(sql)

  mydb.commit()


def main():

   if len(sys.argv)<3:
       print("Usage: "+sys.argv[0]+" Source_File AS_Number")
       sys.exit()


   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()

   ASPrefixesList = []
   
   init_db()

   print("Reading input prefixes...\n")

   with open(filepath) as fp:
       cnt = 0
       for line in fp:
           words = line.strip().split()
           #print(line)
           if len(words)>2 and words[-2]==SourceAS:
              #print("prefix: "+words[1]+", Source AS: "+words[-2])
              ASPrefixesList.append(words[1])
              cnt += 1
              print("\rtotal found "+str(cnt)+", adding "+words[1]+"     ", end="")
              
  
   #print("Source prefix list:\n")
   #print(ASPrefixesList)
   print("\nAggregating...")

   AggrPList = aggregate_prefixes(ASPrefixesList)

   print("Saving...")
   with open(ASPrefixesFile, 'w') as fASPrefixes:
    for prefix in AggrPList:
        fASPrefixes.write("%s\n" % prefix)
        upload_to_db(prefix)

   print("Done\n")

if __name__ == '__main__':
    main()
