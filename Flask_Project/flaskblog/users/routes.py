from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, login_user, login_required, logout_user
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, AccountUpdate, RequestResetForm, ResetPasswordForm
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"your account have been created, you can able to login now ", "success")
            return redirect(url_for("users.login"))
    return render_template("register.html", form=form)

@users.route("/login",  methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit:
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, form.remember.data)
                next_page = request.args.get("next") 
                if next_page:
                    return redirect(next_page)
                else:
                    flash(f"you have successfully logged in", "success")
                    return redirect(url_for("main.home"))
            else:
                flash(f"login failed", "danger")            
    return render_template("login.html", form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home")) 

@users.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    form = AccountUpdate()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        current_user.username = form.username.data
        current_user.email = form.email.data #doubt in db
        db.session.commit()
        flash("Your account have been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET": 
        form.username.data = current_user.username
        form.email.data = current_user.email
        image_file = url_for("static", filename="default_image/" + current_user.image_file)
    return render_template("account.html", image_file = image_file, form=form) 

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)

@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect('main.home')
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email is sent with to reset your password check your inbox", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title = "reset_password",  form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("that is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")          
        user.password = hashed_password
        db.session.commit()
        flash(f"your password has successfully changed ", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="reset Password", form=form)
