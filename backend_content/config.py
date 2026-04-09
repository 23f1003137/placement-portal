import os

class Config:

    SECRET_KEY = "placement-secret"

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))   #Ye current folder ka absolute path deta hai.

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "placement.db")  #Isse database correct folder me create hota hai.
                                                                                     # example:- sqlite:///E:\Placement_Portal_V2\backend\placement.db

    SQLALCHEMY_TRACK_MODIFICATIONS = False



#############


    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes


      # Celery
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


    # Mail — Gmail se bhejenge
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "shivam954886@gmail.com"   # apna email
    MAIL_PASSWORD = "slawklpqqegdrojl"         # app password
    MAIL_DEFAULT_SENDER = "shivam954886@gmail.com"


