import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import db
from .models import Post, User
from .utils import get_post

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    nb_posts = db.session.query(Post).filter(Post.user_id == current_user.id).count()
    posts = db.session.query(Post).filter(Post.user_id == current_user.id).all()
    return render_template(
        "profile.html", name=current_user.name, nb_posts=nb_posts, posts=posts
    )


@main.route("/blog")
@login_required
def blog():
    # join Post and User database
    join_db = db.session.query(Post, User).join(User, User.id == Post.user_id).all()
    return render_template("blog.html", join_db=join_db)


@main.route("/blog/<int:post_id>")
@login_required
def post(post_id):
    return render_template("post.html", post=get_post(post_id))


@main.route("/blog/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            new_post = Post(
                user_id=current_user.id,
                title=title,
                content=content,
                timestamp=datetime.datetime.now(),
            )
            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for("main.profile"))

    return render_template("create.html")


@main.route("/<int:id>/edit", methods=("GET", "POST"))
def edit(id):
    post = get_post(id)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]

        if not title:
            flash("Title is required!")
        else:
            db.session.query(Post).filter(Post.id == id).update(
                {"title": title, "content": content}
            )
            db.session.commit()
            return redirect(url_for("main.profile"))

    return render_template("edit.html", post=post)


@main.route("/blog/<int:id>/edit", methods=("GET", "POST"))
def delete(id):
    post = get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash('"{}" was successfully deleted!'.format(post.title))
    return redirect(url_for("main.profile"))
