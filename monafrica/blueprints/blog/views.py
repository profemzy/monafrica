from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc
from monafrica.extensions import db
from monafrica.blueprints.blog.forms import PostForm
from monafrica.blueprints.blog.models import Post
from monafrica.blueprints.user.decorators import role_required

blog = Blueprint('blog', __name__, template_folder='templates')


@blog.route('/blog', defaults={'page': 1})
@blog.route('/blog/page/<int:page>')
@login_required
def read_blog(page):
    """
    List All Posts
    :return:
    """
    paginated_posts = Post.query.paginate(page, 50, True)

    # posts = Post.query.order_by(desc('created_on')).all()
    return render_template('blog/read_blog.html',
                           posts=paginated_posts, title='Tech Gists')


@blog.route('/blog/manage', defaults={'page': 1})
@blog.route('/blog/page/<int:page>')
@login_required
@role_required('admin')
def list_posts(page):
    """
    List All Posts
    :return:
    """

    paginated_posts = Post.query.paginate(page, 50, True)
    return render_template('blog/index.html',
                           posts=paginated_posts, title='Tech Gists')


@blog.route('/blog/posts/add', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def add_post():
    """
    Add a new post to the database
    :return:
    """

    add_post = True

    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data,
                    user_id=current_user.id)
        try:
            # add post to the database
            db.session.add(post)
            db.session.commit()
            flash('You have successfully added a new post.')
        except:
            # in case post name already exists
            flash('Error: there was an error while creating post.', 'success')

        # redirect to posts page
        return redirect(url_for('blog.list_posts'))

        # load post template
    return render_template('blog/new.html', action="Add",
                           add_post=add_post, form=form,
                           title="Add Post")


@blog.route('/blog/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def edit_post(id):
    """
    Edit a post
    :param id:
    :return:
    """
    add_post = False

    post = Post.query.get_or_404(id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        form.populate_obj(post)

        post.save()
        flash('You have successfully updated the post.', 'success')

        # redirect to the posts page
        return redirect(url_for('blog.list_posts'))

    return render_template('blog/edit.html',
                           action="Edit", add_post=add_post, post=post,
                           form=form, title="Edit Post")


@blog.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def delete_post(id):
    """
    Delete a post from the database
    """
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash('You have successfully deleted the post.')

    # redirect to the posts page
    return redirect(url_for('blog.list_posts'))

    return render_template(title="Delete Post")


@blog.route('/blog/posts/read/<int:id>')
def read_post(id):
    """
    Read a post
    :param id:
    :return:
    """

    post = Post.query.get_or_404(id)

    return render_template('blog/read_post.html', post=post)
