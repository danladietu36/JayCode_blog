from flask import (render_template, flash, url_for, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from top_tech import db
from top_tech.models import Post
from top_tech.posts.forms import Post_form

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def new_post():
    form = Post_form()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post was succesful", "success")
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

@posts.route('/post/<int:post_id>', strict_slashes=False)
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'], strict_slashes=False)
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = Post_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update post', form=form, legend='Updated Post')

@posts.route("/post/<int:post_id>/delete", methods=['GET', 'POST'], strict_slashes=False)
def delete_post():
    post = Post.query.get_or_404()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')
    return redirect(url_for(main.home))