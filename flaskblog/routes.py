from flaskblog.model import User , Post
from flask import render_template,url_for, flash,redirect, request
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from flaskblog import app,db,bcrypt
from flask_login import login_user, current_user, logout_user, login_required
posts=[{
'author':"Purvansh",
'date_posted' : 19,
'title':'run for it',
'content':'bhag'
}]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html",posts=posts) 

@app.route("/about")
def about():
    return render_template("about.html") 

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pass= bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user= User(username=form.username.data,email=form.email.data.lower(),password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.username.data}!You can now login!!!!",'success')
        return redirect(url_for('login'))
    return render_template("register.html",title="Register",form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user=  User.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get("next")
            
            return redirect(next_page)if next_page else  redirect(url_for('home'))
        else:
            flash("Login Unsuccessful. Plase check email and password",'danger')
    return render_template("login.html",title="Login",form= form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email= form.email.data
        db.session.commit()
        flash("Your account has been updated" , 'Success')
        return redirect(url_for('home'))
    elif request.method== 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file= url_for('static',filename='profile_pics/'+current_user.image_file)
    return render_template("account.html",title='Account',
                            image_file=image_file,form=form)