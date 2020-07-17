import os
from datetime import timedelta


class Config:
    SECRET_KEY = 'lb*zkn=t0cmxqi$9u@i#7guv9p)lxij@su^44_#v2lwk&6aw12'
    SECRET_SALT = 'b21dq@*!xe-t240rjz-fvuor2+1sxop6k48h@ggbqis1b#4o69'
    SECRET_URLSALT = 'p@^79!_amvn6s6#(xvou)$4#1l#o!88qhqe97nz+obqt3@q1vd'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/cv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    REMEMBER_COOKIE_DURATION = timedelta(minutes=30)
    UPLOAD_FOLDER = 'static/files'
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = 'logesh732116104026@gmail.com'
    MAIL_PASSWORD = 'nandhatech2020'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
