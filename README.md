# Flask_Website_Project

This project is developed with python library Flask, this is a mini social media website. I have used HTML, CSS, Bootstrap classes for Frontend and Python for Backend.
Readdown the specification of the website given below :point_down:

![alt text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/home.JPG)

 # **Features of the website**
 
 * Secured Registration
 * Privacy protection
 * Password reset capability by Email
 * Deleting and updating Post
 * Upgrading Profile
 * Good Pagination in Pages
 
 # Secured Registration
   In this project i have used `Flask-WTF` form for form validation and `Email-Validator` for email validation. so by default the form does not acccepts the email with improper validation and username less than 5 charactors.
   
   I have used `FLASK-SQLAlchemy` for database as the result  the author of the post can be viewed by `Relationship` function in `Flask-SQLAlchemy`, and this function also gives the flexibility to view how many post is posted by an individual account. And each individual account have given a default image  `common.jpg `
 ```python
 class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="common.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)


 class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
 ```
 
 ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/register.JPG)
 
 
 # Privacy Protection
 I have used  `Flask-Bcrypt ` to secure secret key of  this website from  `CSRF ` attack. And the User Account Password in the dataBase is also Protected by  `secret ` module in python the database only stores the  `hash ` value of the password. so the password is fully protected from extenal source
  ```python
 if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
  ```
 Each User's Privacy in the account is Protected, so the user of the current account cannot update or delete post in another account
 
 ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/403.JPG)
 
 # Password reset capability by Email
 
 If the user forgot his password it can be reseted by the email. And the `Email-Validator` verifies the email and `FLASK-SQLAlchemy` checks whether the email already exists in the database
 
  ```python
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
  ```
  ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/password%20reset.JPG)
  ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/email.JPG)
  ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/password%20reseted.JPG)
  
  # Deleting and updating Post
   The current User can delete and edit the post his account, but the user of another account cannot edit or delete the post of another account as it for secured as mentioned above
  
  ![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/Update_Delete_Post.JPG)
  
  
 ```python  
@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"]) 
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
       abort(403)
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()
            flash("your have updated your post", "success")
            return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form=form, legend = "Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["GET"]) 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    elif post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash("your post have been deleted", "success")
    return redirect(url_for('main.home'))
 ```
Any User in the website cannot view His/Her account untill they were logged in, this function is builded by `login_required`

# Upgading Profile

The User in the account can edit his info by chancing his account password, Email and profile picture and I have Used `Pillow` library for good flexibility in images. 
the users images also protected by the database by `hashing` method so only the hash name is stored in database

 ```python  
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/default_image", picture_fn) 
```

![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/Profile%20Update.JPG)


# Good Pagination in Pages
  I have used pagination in pages so it will be look nice to see maximum 5 post in a single page.This feature is also used in individual profiles
![alt_text](https://github.com/sainath-murugan/Flask_Website_Project/blob/main/Flask_Project/web/pagination.JPG)

# Some Extra Features
   I have use Blue Prints in this Project, so the future development can be done in the website very easily

# copyright :copyright:
   The idea for this project was inspired by [Corey shafer](https://www.youtube.com/user/schafer5), a thanks for him :pray:
