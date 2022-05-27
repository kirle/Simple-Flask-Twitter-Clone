class DevelopmentConfig():
    SECRET_KEY = 'kirle'
    DEBUG = True
    PORT = 5000
    #Database connection
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'admin'
    MYSQL_DB = 'ALS'
    UPLOAD_FOLDER = 'static/uploads'



config = {
    'development' : DevelopmentConfig
}