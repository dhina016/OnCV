from datetime import datetime
from application import db
from sqlalchemy.orm import backref
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    level = db.Column(db.Enum('admin', 'user'), default='user')
    status = db.Column(db.Enum('active', 'inactive', 'terminate'), default='active')
    utype = db.Column(db.Enum('old', 'new'), default='new')
    confirmation = db.Column(db.Boolean, default=False)
    profile_pic = db.Column(db.String(250), nullable=True, default='profile.jpg')
    background_pic = db.Column(db.String(250), nullable=True, default='background.jpg')
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow, default=datetime.utcnow)
    about = db.relationship('About', backref='user_about', passive_deletes=True, lazy=True)
    message = db.relationship('Message', backref='user_message', passive_deletes=True, lazy=True)
    education = db.relationship('Education', backref='user_education', passive_deletes=True, lazy=True)
    hobbies = db.relationship('Hobbies', backref='user_hobbies', passive_deletes=True, lazy=True)
    category = db.relationship('Category', backref='user_category', passive_deletes=True, lazy=True)
    portfolio = db.relationship('Portfolio', backref='user_portfolio', passive_deletes=True, lazy=True)
    skill = db.relationship('Skill', backref='user_skill', passive_deletes=True, lazy=True)
    social = db.relationship('Social', backref='user_social', passive_deletes=True, lazy=True)
    design = db.relationship('Design', backref='user_design', passive_deletes=True, lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}', '{self.level}', '{self.status}')"


class About(db.Model):
    __tablename__ = 'about'
    id = db.Column(db.Integer, primary_key=True)
    aoi = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(10), nullable=True, default='Not Available')
    state = db.Column(db.String(50), nullable=True, default='Not Available')
    city = db.Column(db.String(50), nullable=True, default='Not Available')
    resume = db.Column(db.String(250), nullable=True, default='no')
    career = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, unique=True)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"About('{self.id}', '{self.user_id}')"


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(50), nullable=False)
    sender_id = db.Column(db.String(50), nullable=False)
    seen = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Message('{self.id}', '{self.message}', '{self.sender_id}', '{self.user_id}')"


class Education(db.Model):
    __tablename__ = 'education'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Enum('education','experience'))
    year = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    position = db.Column(db.Integer, nullable=True, default=1)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Education('{self.id}', '{self.user_id}')"


class Hobbies(db.Model):
    __tablename__ = 'hobbies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    icon = db.Column(db.String(50))
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Hobbies('{self.id}', '{self.user_id}')"


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    ctype = db.Column(db.Enum('skill', 'portfolio', ''))
    name = db.Column(db.String(50), nullable=False)
    selection = db.Column(db.String(50))
    icon = db.Column(db.String(50))
    position = db.Column(db.Integer, nullable=False, default=1)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Category('{self.id}', '{self.user_id}')"


class Portfolio(db.Model):
    __tablename__ = 'portfolio'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Portfolio('{self.id}', '{self.user_id}')"


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=1)
    percentage = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    createat = db.Column(db.DateTime, default=datetime.utcnow)
    updateat = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"Skill('{self.id}', '{self.user_id}')"


class Social(db.Model):
    __tablename__ = 'social'
    id = db.Column(db.Integer, primary_key=True)
    dribble = db.Column(db.String(250), nullable=True)
    twitter = db.Column(db.String(250), nullable=True)
    github = db.Column(db.String(250), nullable=True)
    facebook = db.Column(db.String(250), nullable=True)
    instagram = db.Column(db.String(250), nullable=True)
    linkedin = db.Column(db.String(250), nullable=True)
    whatsapp = db.Column(db.String(250), nullable=True)
    youtube = db.Column(db.String(250), nullable=True)
    stackoverflow = db.Column(db.String(250), nullable=True)
    website = db.Column(db.String(250), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False, unique=True)

    def __repr__(self):
        return f"Social('{self.id}', '{self.user_id}')"


class Design(db.Model):
    __tablename__ = 'design'
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.Enum('blue', 'green', 'orange', 'pink', 'purple', 'red'), default='blue')
    theme = db.Column(db.Enum('dark', 'light'), default='light')
    animation = db.Column(db.Enum('ltr', 'btt', 'ttb', 'pop', 'fade', 'swipe'), default='ltr')
    published = db.Column(db.Enum('yes', 'no', 'onedit'), default='no')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        return f"Design('{self.id}', '{self.user_id}')"
