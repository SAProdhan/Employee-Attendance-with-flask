import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from attendance import app, db, bcrypt
from attendance.forms import RegistrationForm, LoginForm, UpdateAccountForm, EmployeeForm, OrganizationForm, ShiftForm
from attendance.models import User, Employee, Organization, Shift
from flask_login import login_user, current_user, logout_user, login_required
import json


posts = [
    {
        'author': 'Sakeef Ameer Prodhan',
        'title': 'Attendance System',
        'content': 'An Application of payroll',
        'date_posted': 'March 16, 2020'
    }
]


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def save_document(form_document):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_document.filename)
    doc_fn = random_hex + f_ext
    doc_path = os.path.join(app.root_path, 'static/document', doc_fn)
    form_document.save(doc_path)
    return doc_fn


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    form = EmployeeForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        if form.document.data:
            doc_file = save_document(form.document.data)
        user = Employee(id=form.eid.data, name=form.name.data, phone=form.phone.data, email=form.email.data, designation=form.designation.data,
                        department=form.department.data, cardno=form.cardno.data, image_file=picture_file, documents=doc_file)
        db.session.add(user)
        db.session.commit()
        flash(f'{form.name.data} has been added!', 'success')
        return redirect(url_for('employee'))
    # image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('employee.html', title='Employee', form=form)


@app.route('/employee', methods=['GET', 'POST'])
@login_required
def employee():
    image_file_path = 'static/profile_pics/'
    form = EmployeeForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        if form.document.data:
            doc_file = save_document(form.document.data)
        employee = Employee(id=form.id.data, name=form.name.data, phone=form.phone.data, email=form.email.data, designation=form.designation.data,
                            department=form.department.data, cardno=form.cardno.data, image_file=picture_file, documents=doc_file)
        db.session.add(employee)
        db.session.commit()
        flash(f'{form.name.data} has been added!', 'success')
        return redirect(url_for('employee'))
    employees = Employee.query.all()
    return render_template('employee.html', title='Employee', form=form, employees=employees, image_file_path=image_file_path)


@app.route('/report')
@login_required
def report():
    return render_template('report.html', title='Report')


def seperat_department_designation(d2_list):
    temp = {}
    for data in d2_list:
        if data.department not in temp:
            temp[data.department] = []
        if data.designation not in temp[data.department]:
            temp[data.department].append(data.designation)
    return temp


@app.route('/department', methods=['GET', 'POST'])
@login_required
def department():
    d_list = Organization.query.all()
    demo = seperat_department_designation(d_list)
    d2_list = json.dumps([{'department': key, 'designation': value}
                          for key, value in demo.items()])
    form = OrganizationForm()
    organization = Organization.query.all()
    if 'Add' in request.form:
        if form.department.data:
            if form.designation.data:
                temp = Organization.query.filter_by(
                    department=form.department.data, designation=form.designation.data).first()
                if temp:
                    flash(f'Data already exits!', 'warning')
                    return redirect(url_for('department'))
                else:
                    data = Organization(
                        department=form.department.data, designation=form.designation.data)
                    db.session.add(data)
                    db.session.commit()
                    flash(f'Data has been added!', 'success')
                    return redirect(url_for('department'))
            else:
                flash(f'Designation empty!', 'warning')
                return redirect(url_for('department'))
        else:
            flash(f'Department empty!', 'warning')
            return redirect(url_for('department'))
    if 'Delete' in request.form:
        if form.department.data:
            if form.designation.data:
                temp = Organization.query.filter_by(
                    department=form.department.data, designation=form.designation.data).first()
                if temp:
                    db.session.delete(temp)
                    db.session.commit()
                    flash(f'Data has been deleted!', 'success')
                    return redirect(url_for('department'))
                else:
                    flash(f'Data not found!', 'warning')
                    return redirect(url_for('department'))
            else:
                flash(f'Designation empty!', 'warning')
                return redirect(url_for('department'))
        else:
            flash(f'Department empty!', 'warning')
            return redirect(url_for('department'))

    return render_template('department.html', title='Department', form=form, organization=organization, d2_list=d2_list, demo=demo)


@app.route('/schedule')
@login_required
def schedule():
    return render_template('schedule.html', title='schedule')


@app.route('/shift', methods=['GET', 'POST'])
@login_required
def shift():
    s_list = Shift.query.all()
    form = ShiftForm()
    if 'Add' in request.form:
        user = Shift.query.filter_by(Name=form.name.data).first()
        if user:
            flash(f'Name already exits', 'warning')
            return redirect(url_for('shift'))
        shift = Shift(Name=form.name.data,
                      SatartDate=request.form["start"], EndDate=request.form["end"])
        db.session.add(shift)
        db.session.commit()
        flash(f'Shift created!', 'success')
        return redirect(url_for('shift'))
    if 'Delete' in request.form:
        if form.name.data:
            temp = Shift.query.filter_by(Name=form.name.data).first()
            if temp:
                db.session.delete(temp)
                db.session.commit()
                flash(f'Data has been deleted!', 'success')
                return redirect(url_for('shift'))
            else:
                flash(f'Data not found!', 'warning')
                return redirect(url_for('shift'))
        else:
            flash(f'Name is empty!', 'warning')
            return redirect(url_for('shift'))
    if 'Edit' in request.form:
        if form.name.data:
            admin = Shift.query.filter_by(Name=form.name.data).update(dict(SatartDate=request.form["start"], EndDate=request.form["end"]))
            db.session.commit()
            flash('Shift has been updated!', 'success')
            return redirect(url_for('shift'))
        else:
            flash(f'Name is empty!', 'warning')
            return redirect(url_for('shift'))
    return render_template('shift.html', title = 'Shift', s_list = s_list, form = form)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user=User(username = form.username.data,
                    email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for { form.username.data}!', 'success')
    return render_template('register.html', title = 'Register', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check Email and password', 'danger')
    return render_template('login.html', title = 'Login', form = form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file=url_for(
        'static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title = 'Account',
                           image_file = image_file, form = form)
