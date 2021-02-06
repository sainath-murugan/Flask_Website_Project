from flask import render_template, request, url_for, flash, redirect, abort, Blueprint
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if request.method == "POST":        
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            flash("your have created a new post", "success")
            return redirect(url_for("main.home"))
    return render_template("create_post.html", form=form, legend="New Post")

@posts.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template("post.html", post=post)

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"]) # we want to use methods to submit the form even though request is not used
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

