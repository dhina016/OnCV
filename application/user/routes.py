import os
import uuid
from flask import Blueprint, render_template, jsonify, url_for, redirect, request, flash
from flask_login import login_required, current_user
from application.model import User, Message, Social, About, Education, Category, Skill, Portfolio, Hobbies, Design
from application import Config, db
from hashids import Hashids

hashids = Hashids(salt=Config.SECRET_URLSALT, min_length=16)
user = Blueprint('user', __name__)


# Upload Helper Function
def allowed_image(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_docs(filename):
    ALLOWED_EXTENSIONS = {'doc', 'docx', 'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(file, name, location):
    filename = name
    if file.filename == '':
            filename = name
    if file and allowed_image(file.filename):
        filename = str(uuid.uuid4())+file.filename
        file.save(os.path.join(Config.BASE_DIR, Config.UPLOAD_FOLDER+location, filename))
    return filename


# Dashboard and Tutorial
@user.route('/dashboard')
@login_required
def dashboard():
    title = ['Dashboard', 'Check your sent and recieved message status']
    color = ['card text-white bg-dark', 'card text-white bg-primary', 'card text-white bg-danger', 'card text-white bg-warning', 'card text-white bg-info', 'card text-white bg-success']
    sendbyme = db.session.query(Message, User).filter(Message.sender_id == User.id).filter(User.id==current_user.id).all()
    mymessage = db.session.query(Message, User).filter(Message.user_id == User.id).filter(User.id==current_user.id).all()
    print(mymessage, sendbyme, current_user.id)
    if current_user.utype == 'new':
        user = User.query.get(current_user.id)
        user.utype = 'old'
        db.session.commit()
        return redirect(url_for('user.tutorial'))
    if mymessage:
        for message, user in mymessage:
            message.seen = True
        db.session.commit()
    return render_template('dashboard.html', title=title, data=sendbyme, data2=mymessage, color=color)


@user.route('/tutorial')
@login_required
def tutorial():
    title = ['Get Started', 'Follow these steps to get amazing OnCV(Online Curriculum Vitae)']

    return render_template('tutorial.html', title=title)


# About Section
@user.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    title = ['About', 'Tell about yourself..']
    if request.method == 'POST':
        check_exist = About.query.filter_by(user_id=current_user.id).first()
        if not check_exist:
            aoi = request.form['aoi']
            dob = request.form['dob']
            age = request.form['age']
            phone = request.form['phone']
            state = request.form['state']
            city = request.form['city']
            co = request.form['co']
            if 'file' not in request.files:
                filename = 'no'
            file = request.files['file']
            if file.filename == '':
                filename = 'no'
            if file and allowed_docs(file.filename):
                filename = str(uuid.uuid4())+file.filename
                file.save(os.path.join(Config.BASE_DIR, Config.UPLOAD_FOLDER+'/resume', filename))

            new_about = About(aoi=aoi, dob=dob, age=age, phone=phone, state=state, city=city, career=co, resume=filename, user_id=current_user.id)
            db.session.add(new_about)
            db.session.commit()
            flash('Created About Successfully', 'success')
            return redirect(url_for('user.about'))
        else:
            flash('Already Exist', 'danger')
            return redirect(url_for('user.about'))

    return render_template('about.html', title=title)


@user.route('/editabout', methods=['GET', 'POST'])
@login_required
def editabout():
    title = ['Edit About', 'Change your about detail']
    about = About.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        print(request.form)
        about.aoi = request.form['aoi']
        about.dob = request.form['dob']
        about.age = request.form['age']
        about.phone = request.form['phone']
        about.state = request.form['state']
        about.city = request.form['city']
        about.career = request.form['co']
        db.session.commit()

        flash('Updated Successfully', 'success')
        return redirect(url_for('user.editabout'))

    return render_template('edit_about.html', title=title, data=about)


# Education Section
@user.route('/education', methods=['GET', 'POST'])
@login_required
def education():
    title = ['Education', 'Fill Your Education and Experience Details']
    if request.method == 'POST':
        category = request.form['category']
        position = request.form['position']
        year = request.form['year']
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']
        new_education = Education(category=category, position=position, year=year, name=name, location=location, description=description, user_id=current_user.id)
        db.session.add(new_education)
        db.session.commit()

        flash('Created {} Successfully'.format(category), 'success')
        return redirect(url_for('user.education'))

    return render_template('education.html', title=title)


@user.route('/manageeducation', methods=['GET'])
@login_required
def manageeducation():
    title = ['Manage Education', 'Choose which want to update']
    education = Education.query.filter_by(user_id=current_user.id).all()

    return render_template('manage_education.html', title=title, data=education)


@user.route('/editeducation/<name>', methods=['GET', 'POST'])
@login_required
def editeducation(name):
    title = ['Edit Education', 'Update your education details']
    value = hashids.decode(name)
    try:
        name = value[0]
        education = Education.query.filter_by(user_id=current_user.id, id=name).first()
    except IndexError:
        education = None
    if request.method == 'POST':
        if Education:
            education.position = request.form['position']
            education.year = request.form['year']
            education.name = request.form['name']
            education.location = request.form['location']
            education.description = request.form['description']
            db.session.commit()

        flash('Updated Successfully', 'success')
        return redirect(url_for('user.manageeducation'))

    return render_template('edit_education.html', title=title, data=education)


# Skill Section
@user.route('/skill', methods=['GET', 'POST'])
@login_required
def skill():
    title = ['Skill', 'Tell your skills to the world']
    data = Category.query.filter_by(ctype='skill', user_id=current_user.id).all()
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        percent = request.form['percent']
        position = request.form['position']
        new_skill = Skill(cid=category, name=name, percentage=percent, position=position, user_id=current_user.id)
        db.session.add(new_skill)
        db.session.commit()

        flash('Created Successfully', 'success')
        return redirect(url_for('user.skill'))

    return render_template('skill.html', title=title, data=data)


@user.route('/manageskill', methods=['GET'])
@login_required
def manageskill():
    title = ['Manage Skill', 'Choose which you want to update']
    data = db.session.query(Skill, Category).filter(Skill.cid == Category.id).filter_by(user_id=current_user.id).all()

    return render_template('manage_skill.html', title=title, data=data)


@user.route('/editskill/<name>', methods=['GET', 'POST'])
@login_required
def editskill(name):
    title = ['Edit Skill', 'Update your skills']
    data = Category.query.filter_by(ctype='skill', user_id=current_user.id).all()
    value = hashids.decode(name)
    try:
        name = value[0]
        skill = Skill.query.filter_by(user_id=current_user.id, id=name).first()
    except IndexError:
        skill = None
    if request.method == 'POST':
        if skill:
            skill.cid = request.form['category']
            skill.name = request.form['name']
            skill.percentage = request.form['percent']
            skill.position = request.form['position']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.manageskill'))

        flash('Something Went Wrong', 'danger')
        return redirect(url_for('user.manageskill'))

    return render_template('edit_skill.html', title=title, data=data, dataskill=skill)


# Skill Category Section
@user.route('/skillcategory', methods=['GET', 'POST'])
@login_required
def skillcategory():
    title = ['Skill Category', 'Specify your skills']
    if request.method == 'POST':
        selection = request.form['category']
        name = request.form['name']
        icon = request.form['icon']
        position = request.form['position']
        new_skillcategory = Category(ctype='skill', selection=selection, name=name, icon=icon, position=position, user_id=current_user.id)
        db.session.add(new_skillcategory)
        db.session.commit()

        flash('Created Successfully', 'success')
        return redirect(url_for('user.skillcategory'))

    return render_template('skill_category.html', title=title)


@user.route('/manageskillcategory', methods=['GET'])
@login_required
def manageskillcategory():
    title = ['Manage Skill Category', 'Choose which you want to update']
    skill = Category.query.filter_by(ctype='skill', user_id=current_user.id).all()
    return render_template('manage_skill_category.html', title=title, data=skill)


@user.route('/editskillcategory/<name>', methods=['GET', 'POST'])
@login_required
def editskillcategory(name):
    title = ['Edit Skill Category', 'Update your skills here']
    value = hashids.decode(name)
    try:
        name = value[0]
        skill = Category.query.filter_by(ctype='skill', user_id=current_user.id, id=name).first()
    except IndexError:
        skill = None
    if request.method == 'POST':
        if skill:
            skill.selection = request.form['category']
            skill.name = request.form['name']
            skill.icon = request.form['icon']
            skill.position = request.form['position']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.manageskillcategory'))

        flash('Something Went Wrong', 'danger')
        return redirect(url_for('user.manageskillcategory'))

    return render_template('edit_skill_category.html', title=title, data=skill)


# Hobbies Section
@user.route('/hobbies', methods=['GET', 'POST'])
@login_required
def hobbies():
    title = ['Hobbies', 'Add your hobbies']
    if request.method == 'POST':
        print(request.form)
        name = request.form['name']
        icons = request.form['icons']
        new_hobby = Hobbies(name=name, icon=icons, user_id=current_user.id)
        db.session.add(new_hobby)
        db.session.commit()
        flash('Created Successfully', 'success')
        return redirect(url_for('user.hobbies'))

    return render_template('hobbies.html', title=title)


@user.route('/managehobbies', methods=['GET'])
@login_required
def managehobbies():
    title = ['managehobbies', 'Choose which you want to update']
    hobbies = Hobbies.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_hobbies.html', title=title, data=hobbies)


@user.route('/edithobby/<name>', methods=['GET', 'POST'])
@login_required
def edithobby(name):
    title = ['Edit Hobby', 'Update Your Hobby']
    value = hashids.decode(name)
    try:
        name = value[0]
        hobbies = Hobbies.query.filter_by(user_id=current_user.id, id=name).first()
    except IndexError:
        hobbies = None
    if request.method == 'POST':
        if hobbies:
            hobbies.name = request.form['name']
            hobbies.icon = request.form['icons']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.managehobbies'))

        flash('Something Went Wrong', 'danger')
        return redirect(url_for('user.managehobbies'))

    return render_template('edit_hobbies.html', title=title, data=hobbies)


# Portfolio Section
@user.route('/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():
    title = ['Portfolio', 'Showcase skill with proof']
    data = Category.query.filter_by(ctype='portfolio', user_id=current_user.id).all()
    if request.method == 'POST':
        category = request.form['category']
        name = request.form['name']
        description = request.form['description']
        filename = 'default.jpg'
        if 'iamge' not in request.files:
            filename = 'default.jpg'
        file = request.files['image']
        filename = upload_file(file, filename, '/portfolio')

        new_portfolio = Portfolio(cid=category, name=name, description=description, image=filename, user_id=current_user.id)
        db.session.add(new_portfolio)
        db.session.commit()

        flash('Created Successfully', 'success')
        return redirect(url_for('user.portfolio'))

    return render_template('portfolio.html', title=title, data=data)


@user.route('/manageportfolio', methods=['GET', 'POST'])
@login_required
def manageportfolio():
    title = ['Manage Portfolio', 'Choose which you want to update']
    data = Portfolio.query.filter_by(user_id=current_user.id).all()

    return render_template('manage_portfolio.html', title=title, data=data)


@user.route('/editportfolio/<name>', methods=['GET', 'POST'])
@login_required
def editportfolio(name):
    title = ['Edit Portfolio', 'Update your portfolio']
    value = hashids.decode(name)
    try:
        name = value[0]
        portfolio = Portfolio.query.filter_by(user_id=current_user.id, id=name).first()
    except IndexError:
        portfolio = None
    if request.method == 'POST':
        if portfolio:
            portfolio.name = request.form['name']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.manageportfolio'))

        flash('Something Went Wrong', 'danger')
        return redirect(url_for('user.manageportfolio'))

    return render_template('edit_portfolio_category.html', title=title, data=portfolio)


# Portfolio Category Section
@user.route('/portfoliocategory', methods=['GET', 'POST'])
@login_required
def portfoliocategory():
    title = ['Portfolio Category', 'Add category for portfolio']
    if request.method == 'POST':
        name = request.form['name']
        new_skillcategory = Category(ctype='portfolio', name=name, user_id=current_user.id)
        db.session.add(new_skillcategory)
        db.session.commit()
        flash('Created Successfully', 'success')
        return redirect(url_for('user.portfoliocategory'))

    return render_template('portfolio_category.html', title=title)


@user.route('/manageportfoliocategory', methods=['GET'])
@login_required
def manageportfoliocategory():
    title = ['Manage Portfolio Category', 'Choose which you want to edit']
    portfolio = Category.query.filter_by(ctype='portfolio', user_id=current_user.id).all()
    return render_template('manage_portfolio_category.html', title=title, data=portfolio)


@user.route('/editportfoliocategory/<name>', methods=['GET', 'POST'])
@login_required
def editportfoliocategory(name):
    title = ['Edit Portfolio Category', 'Update portfolio category']
    value = hashids.decode(name)
    try:
        name = value[0]
        portfolio = Category.query.filter_by(ctype='portfolio', user_id=current_user.id, id=name).first()
    except IndexError:
        portfolio = None
    if request.method == 'POST':
        if portfolio:
            portfolio.name = request.form['name']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.manageportfoliocategory'))

        flash('Something Went Wrong', 'danger')
        return redirect(url_for('user.manageportfoliocategory'))

    return render_template('edit_portfolio_category.html', title=title, data=portfolio)


# Social Links Section
@user.route('/sociallink', methods=['GET', 'POST'])
@login_required
def sociallink():
    title = ['Social Links', 'Add your social media links']
    user = Social.query.filter_by(user_id=current_user.id).first()
    if request.method == 'POST':
        if user:
            user.dribble = request.form['dribble']
            user.twitter = request.form['twitter']
            user.github = request.form['github']
            user.facebook = request.form['facebook']
            user.instagram = request.form['instagram']
            user.linkedin = request.form['linkedin']
            user.whatsapp = request.form['whatsapp']
            user.stackoverflow = request.form['stackoverflow']
            user.website = request.form['website']
            user.youtube = request.form['youtube']
            db.session.commit()
            flash('Updated Successfully', 'success')
            return redirect(url_for('user.sociallink'))
        else:
            flash('Something Went Wrong', 'danger')
            return redirect(url_for('user.sociallink'))

    return render_template('sociallink.html', title=title, data=user)


# Design Section
@user.route('/design', methods=['GET', 'POST'])
@login_required
def design():
    title = ['Update Design', 'Change CV design anytime with in a minute']
    about = About.query.filter_by(user_id=current_user.id).first()
    education = Education.query.filter_by(user_id=current_user.id).first()
    skill = Skill.query.filter_by(user_id=current_user.id).first()
    hobbies = Hobbies.query.filter_by(user_id=current_user.id).first()
    design = Design.query.filter_by(user_id=current_user.id).first()
    publish = 'no'
    if about and education and skill and hobbies:
        publish = 'yes'
    if request.method == 'POST':
        color = request.form['color']
        theme = request.form['theme']
        animation = request.form['animation']
        print(publish)
        if publish == 'no' and request.form['status'] != 'no':
            status = 'no'
            warning = True
        else:
            status = request.form['status']
            warning = False
        print(warning)
        print(status)
        if warning:
            flash('Fill all mandatory fields to activate', 'warning')

        design.color = color
        design.theme = theme
        design.animation = animation
        design.published = status
        print(request.form)
        db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect(url_for('user.design'))

    return render_template('design.html', title=title, data=design)


@user.route('/picture', methods=['GET', 'POST'])
@login_required
def picture():
    title = ['Update Details', 'Update Name, Pictures']
    user = User.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        user = User.query.get(current_user.id)
        profile = user.profile_pic
        background = user.background_pic
        if 'profile' not in request.files:
            profile = user.profile_pic
        if 'background' not in request.files:
            background = user.background_pic
        profile_pict = request.files['profile']
        background_pict = request.files['background']
        profile = upload_file(profile_pict, user.profile_pic, '/profile')
        background = upload_file(background_pict, user.background_pic, '/background')

        user.profile_pic = profile
        user.name = request.form['name']
        user.background_pic = background
        db.session.commit()

        flash('Updated Successfully', 'success')
        return redirect(url_for('user.picture'))

    return render_template('picture.html', title=title, data=user)


@user.route('/delete/<section>/<name>',  methods=['DELETE'])
@login_required
def delete(section, name):
    value = hashids.decode(name)
    try:
        name = value[0]
    except IndexError:
        return jsonify(message="failed"), 404
    if section == 'education':
        Education.query.filter_by(id=name, user_id=current_user.id).delete()
    elif section == 'skillcategory':
        Category.query.filter_by(ctype='skill', id=name, user_id=current_user.id).delete()
    elif section == 'skill':
        Skill.query.filter_by(id=name, user_id=current_user.id).delete()
    elif section == 'portfoliocategory':
        Category.query.filter_by(ctype='portfolio', id=name, user_id=current_user.id).delete()
    elif section == 'portfolio':
        Portfolio.query.filter_by(id=name, user_id=current_user.id).delete()
    elif section == 'hobbies':
        Hobbies.query.filter_by(id=name, user_id=current_user.id).delete()
    db.session.commit()

    return jsonify(section=section, value=name), 200
