from flask import Flask, request, redirect, url_for, render_template, flash, session
from model import User, db , bcrypt , login_manager
from form import UserForm, RegistrationForm, LoginForm , ReviewForm
from flask_login import  login_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this not secret'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:p@ssword@localhost/flaskProject'
login_manager.init_app(app)
db.init_app(app)


@app.route("/edit")
def users():
    if 'email' in session:
        users = User.query.order_by(User.name).all()
        return render_template('table.html', users=users)
    return redirect(url_for('dashboard'))

@app.route("/")
def dashboard():
    return render_template('dashboard.html')

@app.route("/users/delete", methods=('POST',))
def users_delete():
    try:
        user_index = User.query.filter_by(id=request.form['id']).first()
        db.session.delete(user_index)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  contact.', 'danger')

    return redirect(url_for('users'))

@app.route("/edit_user/<id>", methods=('GET', 'POST'))
def edit_user(id):
    edit_user= User.query.filter_by(id=id).first()
    form = UserForm(obj=edit_user)
    if form.validate_on_submit():
        try:
            # Update user
            form.populate_obj(edit_user)
            db.session.add(edit_user)
            db.session.commit()
            # User info
            flash('Saved successfully', 'success')
            return redirect(url_for('users'))
        except:
            db.session.rollback()
            flash('Error update contact.', 'danger')
    return render_template(
        'edit.html',
        form=form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data, form.password.data, form.address.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/review')
def review():
    form = ReviewForm(request.form)
    return render_template('review.html', form=form)

@app.route('/login', methods=('GET','POST'))
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user= User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_hash(form.password.data):
            login_user(user)
            session['email']=user.email
            return redirect(url_for('users'))
        else:
            flash("Email or password incorrect", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    session.pop('email',None)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run()
