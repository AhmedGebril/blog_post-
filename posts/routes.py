from flask import Blueprint,request,render_template,url_for,redirect,flash,abort
from flask_login import login_required,current_user
from run import db,Post
from posts.forms import Post_form


posts=Blueprint('posts',__name__)


@posts.route('/posts',methods=['POST','GET'])
@login_required
def Posts_Page():
    form = Post_form()
    if form.validate_on_submit():
        post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('your post has been created successfully','success')
        return redirect(url_for('home'))
    return render_template('create_post.html',form=form)


@posts.route('/post/<int:post_id>')
def show_post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',post=post)

@posts.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
def update_post(post_id):
    form = Post_form()
    post=Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('you post have been updated','success')
        return redirect(url_for('show_post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html',post=post,form=form)

@posts.route('/Delete_Post/<int:post_id>',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted','success')
    return redirect(url_for('home'))

@posts.route('/follow/user/<int:post_id>',methods=['POST'])
@login_required
def Follow_user(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.author
    if request.method =='POST':
        user.followers=user.followers+1
        db.session.commit()
        return redirect(url_for('show_post',post_id=post.id))
    else:
        flash("Couldn't follow the account",'danger')
        return redirect(url_for('show_post', post_id=post.id))
