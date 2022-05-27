from tkinter import E
import flask_login
from pyrfc3339 import generate 
import werkzeug.security as safe
from werkzeug.security import generate_password_hash
from flask_login import current_user

from modules.modules import mysql

from werkzeug.security import check_password_hash , generate_password_hash

class User(flask_login.UserMixin):
    def __init__(self, id, username, password, picture) -> None:
        self.id = id
        self.username = username
        self.password = password
        self.picture = picture
    

    def hasPicture(self):
        return self.picture is not None

    @classmethod
    def check_password(cls, hashed_password, password):
        return check_password_hash(hashed_password, password)

    
    def editPhoto(self,pic):
        c = mysql.connection.cursor()
        c.execute("""
            UPDATE user 
            SET
                picture = %s
            WHERE id = %s 
            """, [pic,str(self.id)])        
        mysql.connection.commit()


    def editUsername(self,username):
        c = mysql.connection.cursor()
        c.execute("""
            SELECT username FROM user WHERE username=%s
            """, [username])
        rows = c.fetchall()     
        print(c.rowcount)   
        if c.rowcount > 0:
            return False
        
        c.execute("""
            UPDATE user 
            SET
                username = %s
            WHERE id = %s 
            """, [username,str(self.id)])        
        mysql.connection.commit()
        return True

    def editPassword(self,password):
        hashed_pass = generate_password_hash(password)
        c = mysql.connection.cursor()
        c.execute("""
            UPDATE user 
            SET
                password = %s
            WHERE id = %s 
            """, [hashed_pass,str(self.id)])        
        mysql.connection.commit()

    @classmethod
    def hasLikedTweet(cls, tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
            SELECT COUNT(*) FROM likes 
            WHERE likes.user_id = %s and likes.tweet_id = %s
            """, [current_user.id,tweet_id])        
        result=c.fetchone()
        mysql.connection.commit()

        return result[0] > 0


    def login(self):
        """
        > Function login()
        > Fetch first row on mysql equals to the username of the User object passed
        > as parameter and returns new User object with true/false on password field
        """
        try:
            c = mysql.connection.cursor()
            sql = """
                SELECT id, username, password, picture 
                FROM user 
                WHERE username=%s
                """ 
            c.execute(sql,[self.username] )
            row = c.fetchone()
            if(row != None):
                self.password = self.check_password(row[2],self.password)
                self.id = row[0]
                self.username = row[1]
                self.picture = row[3]
                #user = User(row[0], row[1], self.check_password(row[2],self.password))
                return True
            else:
                return False
        except Exception as e:
            raise Exception(e)


    @classmethod
    def get_by_id(cls, id):
        try:
            c = mysql.connection.cursor()
            sql = """
                SELECT id, username, picture
                FROM user 
                WHERE id='{0}'
                """.format(id)
            c.execute(sql)
            row = c.fetchone()
            if(row != None):
                logged_user = User(row[0], row[1], None, row[2])
                return logged_user
            else:
                return None
        except Exception as e:
            raise Exception(e)
 
    def register_user(self):
        try:
            hashed_pass = generate_password_hash(self.password)
            c = mysql.connection.cursor()        
            c.execute("""
            SELECT username FROM user WHERE username=%s
            """, [self.username])
            rows = c.fetchall()     
            print(c.rowcount)   
            if c.rowcount > 0:
                return False
        
            c.execute("INSERT INTO user(username,password,picture) VALUES(%s,%s,%s);", (self.username,hashed_pass,self.picture))
            mysql.connection.commit()
            return True
        except Exception as e:
            raise Exception(e) 

  