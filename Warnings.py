import pandas as pd
import sqlite3
from datetime import datetime,timedelta
#sqlite> CREATE TABLE warnings(warning_id integer primary key, user_id integer, time DATETIME, reason TEXT);
#sqlite> CREATE TABLE muted(user_id integer primary key, unmute_time DATETIME);


class DataBaseManagement:
    def __init__ (self):
        self.con =  sqlite3.connect("Data Files/database.sqlite3")


    def query_user_warnings(self,user_id):
         warnings = pd.read_sql_query("SELECT * from warnings WHERE user_id= ?", self.con,params={str(user_id)})
         return warnings

    def insert_user_warnings(self,user_id,reason):
        
        sql = "insert into warnings(user_id,time,reason) values(?,?,?);"
        cur = self.con.cursor()
        cur.execute(sql,(user_id,datetime.utcnow().strftime('%Y-%m-%d-%H:%M'),str(reason)))
        self.con.commit()

    
    def get_to_unmute(self):
        sql = "select * from muted where muted.unmute_time <= date('now')"
        users = pd.read_sql_query(sql, self.con)

        return users

    def delete_muted_users(self):
        sql = "delete from muted where muted.unmute_time <= date('now')"
        cur = self.con.cursor()

        cur.execute(sql)
        self.con.commit()

    def insert_user_muted(self,user_id,mute_length = 4):
        
        sql = "insert into muted(user_id,unmute_time) values(?,?);"
        cur = self.con.cursor()
        
        time = datetime.utcnow() # get date and time today
        delta = timedelta(hours=mute_length) #initialize delta
        
        future_time = time + delta # add the delta days
        
        cur.execute(sql,(user_id,future_time.strftime('%Y%m%d%H%M')))
        self.con.commit()
        return future_time.strftime('%Y-%m-%d-%H:%M') 

'''
def unmute_users():
        db = DataBaseManagement()
        db.insert_user_muted(334434,mute_length=0)
        
        to_unmute = db.get_to_unmute()
        print(to_unmute)
        for i in to_unmute["user_id"]:
            print(i)
        #db.delete_muted_users()
unmute_users()
'''