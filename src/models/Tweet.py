
from flask_login import current_user
from modules.modules import mysql



class Tweet():

    @classmethod
    def getTweets(cls):
        c = mysql.connection.cursor()
        c.execute("""
            SELECT tweet.tweet_id,tweet.tweet_text ,tweet.author_id, tweet.replies_to, user.username, user.picture, tweet.publish_date  
            FROM tweet INNER JOIN user 
            ON tweet.author_id = user.id  
            """)
        data = c.fetchall() 
        return data

    @classmethod
    def getTweetLikes(cls,tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
            SELECT COUNT(*) FROM likes WHERE likes.tweet_id = %s
            """, [tweet_id])
        likes = c.fetchone()
        return likes

    @classmethod
    def getTweetReplies(cls, tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
            SELECT COUNT(*) FROM tweet WHERE tweet.replies_to = %s
            """, [tweet_id])
        comments = c.fetchone()
        return comments

    @classmethod
    def getTweetsReplyingTo(cls,tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
                SELECT user.username, tweet.tweet_text 
                FROM user, tweet 
                WHERE tweet.replies_to = %s AND user.id = tweet.author_id
                """, [tweet_id])
        rows = c.fetchall()
        mysql.connection.commit()
        return rows

    @classmethod
    def addTweet(cls, text, replies_to,today):
        """
        > Function addTweet()
        """
        c = mysql.connection.cursor()
        if (replies_to == 'None'):
            c.execute('INSERT INTO tweet(tweet_text,author_id, publish_date) VALUES (%s,%s,%s)', [
                text, current_user.id,today])
        else:
            c.execute('INSERT INTO tweet(tweet_text,author_id,replies_to,publish_date) VALUES (%s,%s,%s,%s)', [
                text, current_user.id, replies_to,today])
        mysql.connection.commit()
            
 

    @classmethod
    def deleteTweet(cls,tweet_id):
        c = mysql.connection.cursor()
        rows_deleted = c.execute('DELETE FROM tweet WHERE tweet_id = %s and author_id =%s ',[tweet_id,current_user.id] )
        mysql.connection.commit()
        return rows_deleted != 0

    @classmethod
    def editTweet(cls,tweet_id, tweet_text):
        c = mysql.connection.cursor()
        rows_updated = c.execute("""
            UPDATE tweet 
            SET tweet_text = %s
            WHERE tweet_id = %s
            """, (tweet_text, tweet_id))
        mysql.connection.commit()
        return rows_updated != 0
     
    @classmethod
    def likeTweet(cls, tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
            INSERT IGNORE INTO likes(user_id, tweet_id)
            VALUES (%s, %s) 
            """, [current_user.id,tweet_id])        
        mysql.connection.commit()

    @classmethod
    def unlikeTweet(cls, tweet_id):
        c = mysql.connection.cursor()
        c.execute("""
            DELETE FROM likes
            WHERE user_id = %s and tweet_id = %s 
            """, [current_user.id,tweet_id])        
        mysql.connection.commit()        