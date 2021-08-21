import pandas as pd
import sqlite3
from datetime import datetime,timedelta
#sqlite> CREATE TABLE warnings(warning_id integer primary key, user_id integer, time DATETIME, reason TEXT);
#sqlite> CREATE TABLE muted(user_id integer primary key, unmute_time DATETIME);

#sqlite> CREATE TABLE forbidden_reactions(user_id integer primary key, clown_count integer, middlefinger_count integer);


class DataBaseManagement:
    def __init__ (self):
        self.con =  sqlite3.connect("Data Files/database.sqlite3")


    def query_user_reactions(self,user_id):
         warnings = pd.read_sql_query("SELECT * from forbidden_reactions WHERE user_id= ?", self.con,params={str(user_id)})
         return warnings


    def update_clown_count(self,user_id):
        sql = "INSERT INTO forbidden_reactions VALUES(?,1,1) ON CONFLICT DO UPDATE SET  clown_count = clown_count +1;"
        
        cur = self.con.cursor()
        
        cur.execute(sql,(user_id,))
        self.con.commit()
        

    def update_middlefinger_count(self,user_id):
        sql = "INSERT INTO forbidden_reactions VALUES(?,1,1) ON CONFLICT DO UPDATE SET  middlefinger_count = middlefinger_count +1;"
        
        cur = self.con.cursor()
        cur.execute(sql,(user_id,))
        self.con.commit()


    '''
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
