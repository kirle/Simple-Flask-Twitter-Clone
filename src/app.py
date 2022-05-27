from crypt import methods
from click import edit
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from importlib_metadata import files, method_cache
from numpy import true_divide
from flask import send_from_directory, send_file
from werkzeug.utils import secure_filename
import uuid as uuid
from datetime import date

from config import config

#Models
from models.User import User
from models.Tweet import Tweet

import os 
#Entities
#from models.entities.User import User

#Variables

from modules.modules import app
from modules.modules import mysql
login_manager_app = LoginManager(app)
csrf = CSRFProtect(app) 

@login_manager_app.user_loader
def load_user(id):
    return User.get_by_id(id)


# --------
# > MAIN ROUTING
# --------

@app.route('/')
def root():  
    if(current_user.is_authenticated):
        return redirect(url_for('home'))
    return redirect(url_for('login'))


# --------
# > AUTHENTICATION ROUTING
# -------- 

#Register
@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        file = request.files['photo']
        
        if (file.content_type == 'image/png'):
            #save image
            pic_name = file.filename
            filename = secure_filename(pic_name)

            pic_name = str(uuid.uuid1()) + "_" + filename
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
           
        else:
            pic_name = None


        to_register_user = User(0,name,password,pic_name)
        if(to_register_user.register_user()):
            flash("User register OK")
        else:
            flash("Not a valid user")

        return render_template('auth/login.html')
   
    else:
        return render_template('auth/register.html')

#Login
@app.route('/login' , methods = ['GET', 'POST'])
def login():  
    if request.method == 'POST':
        logged_user = User(0,request.form['username'],request.form['password'],None)
        has_logged = logged_user.login()
        if (has_logged):
            if logged_user.password: 
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Wrong password")
                return render_template('auth/login.html')
        else:
            flash("User not found")
            return render_template('auth/login.html')
    else: #Form with GET
        return render_template('auth/login.html')

#Logout
@app.route('/logout') 
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# --------
# > TWEET ROUTING
# --------  


#List tweet (Home) 
@app.route('/home')
@login_required
def home():
    print(current_user.picture)
    data = Tweet.getTweets()
    data2 = []
    for tweet in data:
        tweet += Tweet.getTweetLikes(tweet[0])
        tweet += Tweet.getTweetReplies(tweet[0])
        data2.append(tweet)

    return render_template('home.html', data=data2)

#CRUD Tweets
@app.route('/tweet', methods = ['GET', 'POST'])
@login_required
def tweet():
    if request.method == 'POST':
        text = request.form['inputText']
        replies_to = request.form['replies_to']
        today = date.today()

        if(text != "" and len(text) <= 150):
            Tweet.addTweet(text, replies_to, today)
            flash('Tweet published succesfully')
        else:
            flash('Not a valid tweet')
        return redirect(url_for('home'))
    else:
        _method = request.args['_method']

        if(_method == 'DELETE'):
            tweet_id = request.args['tweet_id']
            if(Tweet.deleteTweet(tweet_id)):
                flash("Tweet removed ok" )
            else:
                flash("Error al eliminar tweet")
            return redirect(url_for('home'))    
       
        if (_method == 'PUT'):
            tweet_id = request.args['tweet_id']
            tweet_text = request.args['tweet_text']
            if(Tweet.editTweet(tweet_id,tweet_text)):
                flash("Tweet edited")
            else:
                flash("Error editing tweet")
            return redirect(url_for('home'))

        return redirect(url_for('error'))


@app.route('/edit_tweet', methods=['GET'])
@login_required
def editTweet():
    tweet_id = request.args['tweet_id']
    tweet_text = request.args['tweet_text']
    data = [tweet_id, tweet_text]    
    return render_template('edit_tweet.html', data=data )

@app.route('/tweet_reply', methods= ['GET'])
@login_required
def tweet_reply():
    tweet_id = request.args['tweet_id']
    tweet_text = request.args['tweet_text']
    tweet_author = request.args['tweet_author']
    replies = Tweet.getTweetsReplyingTo( tweet_id)
    flash(replies)
    data = [tweet_id, tweet_text, tweet_author]    
    return render_template('tweet_replies.html', data=data )
    
@app.route('/like_action', methods= ['POST'])
@login_required
def like_action():
    tweet_id = request.form['tweet_id']
    action = request.form['__action']
    if (action == 'LIKE'):
        Tweet.likeTweet(tweet_id)
        return redirect(url_for('home'))
    else:
        Tweet.unlikeTweet(tweet_id)
        return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    #from os.path import join, dirname, realpath
    #UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads/')
    #data= send_file(os.path.join(UPLOADS_PATH, current_user.picture), as_attachment=True)
    #data= send_from_directory(UPLOADS_PATH, current_user.picture)
    if (request.method == 'POST'):
        username = request.form['username']
        password = request.form['password']
        file = request.files['avatar']
        edited = False
        if file.content_type == 'image/png':
            pic_name = file.filename
            if pic_name != "":
            #Edit photo
                filename = secure_filename(pic_name)
                pic_name = str(uuid.uuid1()) + "_" + filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
                current_user.picture = pic_name
                current_user.editPhoto(pic_name)
                edited = True
        if username != '':
            has_been_edited = current_user.editUsername(username)
            if(has_been_edited): 
                current_user.username = username
                edited=True
            else:
                flash("Invalid username")
        if password != '':
            current_user.editPassword(password)
            edited = True

        if(edited): flash("User edited")
        else: flash("Not changed")
    
    return render_template('profile.html')



# --------
# > ERROR  
# -------- 

# 401 not authorized (login required)
def status_400(error):
    return """
    <h1> Pagina no encontrada </h1> 
    <input type="button" value="Go Back" 
    onclick="history.back(-1)" /> """, 404
def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return """
    <h1> Pagina no encontrada </h1> 
    <input type="button" value="Go Back" 
    onclick="history.back(-1)" /> """, 404

@app.route("/error")
def error():
    return """
    <h1> Pagina no encontrada </h1> 
    <input type="button" value="Go Back" 
    onclick="history.back(-1)" /> """, 404

# ------------
# > Main
# ------------
if __name__ == '__main__':
    
    app.config.from_object(config['development']) #Load configuration
    csrf.init_app(app) # For safe forms
    # Error handlers
    app.register_error_handler(400, status_400)

    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    app.run()
else: #Debugger only works with this
    app.config.from_object(config['development']) #Load configuration
    csrf.init_app(app) # For safe forms
    # Error handlers
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)

    app.run()