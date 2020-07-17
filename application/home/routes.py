from flask import Blueprint, render_template, url_for, redirect, request, flash, abort
from application import db, Config, mail
from flask_login import login_required, current_user, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash
from application.model import User, Social, Design, About, Education, Category, Hobbies, Portfolio, Skill, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
from flask_mail import Message as EMessage
from re import search

home = Blueprint('home', __name__, static_folder='static', template_folder='templates')

sendMail = URLSafeTimedSerializer(Config.SECRET_KEY)


@home.route('/')
def main():
    title = ['Resume', '']
    user = db.session.query(User, Social, About).filter(User.id == Social.user_id).filter(User.id == About.user_id).filter(User.id == Design.user_id, Design.published == 'yes').all()
    return render_template('home.html', title=title, data=user)


@home.route('/dbcreate')
def dbcreate():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return '<h1>DB Created</h1>'


@home.route('/cv')
@home.route('/cv/<name>', methods=['GET', 'POST'])
def cv(name='admin'):
    title = ['Resume', '']
    user = User.query.filter_by(username=name).first()
    if request.method == 'POST':
        print(request.form)
        uid = request.form['id']
        getmessage = request.form['message']
        check_exist = Message.query.filter_by(sender_id=current_user.id, user_id=uid).first()
        if not check_exist:
            new_message = Message(message=getmessage, sender_id=current_user.id, user_id=uid)
            db.session.add(new_message)
            db.session.commit()
            flash('Send Message Successfully', 'success')
        else:
            flash('Already Sent the feedback', 'danger')

        return redirect(url_for('home.main'))

    if user:
        design = Design.query.filter(Design.published != 'no', Design.user_id == user.id).first()
        if design:
            if design.published == 'onedit':
                if current_user.is_authenticated:
                    if user.id != current_user.id:
                        abort(404)
                else:
                    abort(404)
        else:
            abort(404)
    else:
        abort(404)

    about = About.query.filter_by(user_id=user.id).first()
    education = Education.query.filter_by(user_id=user.id, category='education').order_by('position').all()
    experience = Education.query.filter_by(user_id=user.id, category='experience').all()
    hobbies = Hobbies.query.filter_by(user_id=user.id).all()
    sc = Category.query.filter_by(user_id=user.id, ctype='skill').order_by('position').all()
    pc = Category.query.filter_by(user_id=user.id, ctype='portfolio').order_by('position').all()
    portfolio = Portfolio.query.filter_by(user_id=user.id).all()
    skill = Skill.query.filter_by(user_id=user.id).order_by('position').all()
    social = Social.query.filter_by(user_id=user.id).first()
    if not about and not education and not hobbies and not skill:
        design.published = 'no'
        db.session.commit()
        abort(404)
    return render_template('cv.html', title=title, user=user, about=about, design=design, education=education, experience=experience, hobbies=hobbies, portfolio=portfolio, skill=skill, social=social, scategory=sc, pcategory=pc)


@home.route('/login', methods=['GET', 'POST'])
def login():
    title = ['Login', '']
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if 'remember' in request.form:
            remember = True if request.form['remember'] == 'on' else False
        else:
            remember = False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Please check email and try again.', 'danger')
            return redirect(url_for('home.login'))

        if not check_password_hash(user.password, password):
            flash('Please check your password and try again', 'danger')
            return redirect(url_for('home.login'))

        if not user.confirmation:
            flash('Please Confirm your mail', 'danger')
            return redirect(url_for('home.login'))

        login_user(user, remember=remember)
        return redirect(url_for('user.dashboard'))

    return render_template('login.html', title=title)


@home.route('/register', methods=['GET', 'POST'])
def register():
    title = ['Register', '']
    if request.method == 'POST':
        username = (request.form['username']).lower()
        name = request.form['name']
        email = (request.form['email']).lower()
        password = request.form['password']
        user_email = User.query.filter_by(email=email).first()
        user_name = User.query.filter_by(username=username).first()

        if user_email or user_name:
            flash('Email or Username already Exist', 'danger')
            return redirect(url_for('home.login'))
        if not search('@gmail.com', email):
            flash('Sorry Temp mail not allowed, use Gmail', 'danger')
            return redirect(url_for('home.register'))

        token = sendMail.dumps(email, salt=Config.SECRET_SALT)
        msg = EMessage('Confirm Email from OnCV', sender=Config.MAIL_USERNAME, recipients=[email])
        link = url_for('home.confirm_email', token=token, _external=True)
        msg.body = 'Your Confirmation link valid for 30 minutes only. Click the link to login, {}'.format(link)
        mail.send(msg)
        new_user = User(username=username, name=name, email=email, password=generate_password_hash(password, method='sha256'), level='user')
        db.session.add(new_user)
        db.session.commit()

        user = User.query.filter_by(email=email).first()

        if user:
            social_link = Social(user_id=user.id)
            design = Design(user_id=user.id)
            db.session.add(social_link)
            db.session.add(design)
            db.session.commit()
        else:
            flash('Something Went Wrong', 'danger')
            return redirect(url_for('home.register'))

        flash('Thanks for Registration. Please confirm your mail', 'success')
        return redirect(url_for('home.login'))

    return render_template('register.html', title=title)


@home.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home.login'))


@home.route('/icons')
def icons():
    title = ['Icons', '']
    return render_template('icons.html', title=title)


@home.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = sendMail.loads(token, salt=Config.SECRET_SALT, max_age=3600)
    except SignatureExpired:
        flash('Link Expired Please Try again', 'danger')
        return redirect(url_for('home.login'))
    except BadTimeSignature:
        flash('Link is not valid', 'danger')
        return redirect(url_for('home.login'))
    except BadSignature:
        flash('Link is not valid', 'danger')
        return redirect(url_for('home.login'))

    user = User.query.filter_by(email=email).first()
    if not user.confirmation:
        user.confirmation = True
        db.session.commit()
        flash('Verified successfully', 'success')
        return redirect(url_for('home.login'))
    else:
        flash('Already Verified', 'warning')
        return redirect(url_for('home.login'))
