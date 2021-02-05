import pandas as pd
import sqlite3
from datetime import datetime
#sqlite> CREATE TABLE warnings(warning_id integer primary key, user_id integer, time DATETIME);


class DataBaseManagement:
    def __init__ (self):
        self.con =  sqlite3.connect("Data Files/database.sqlite3")


    def query_user_warnings(self,user_id):
         warnings = pd.read_sql_query("SELECT * from warnings WHERE user_id="+str(user_id), self.con)
         return warnings

    def insert_user_warnings(self,user_id):
        
        sql = "insert into warnings(user_id,time) values(?,?);"
        print(sql)
        cur = self.con.cursor()
        cur.execute(sql,(user_id,datetime.utcnow().strftime('%Y-%m-%d-%H:%M')))
        self.con.commit()

        