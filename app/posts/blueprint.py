from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import login_required, current_user

from app.models import Post, Tag, slugify
from .forms import PostForm
from app import db
from app import app

posts = Blueprint('posts', __name__, template_folder='templates')


@posts.route('/create', methods=('GET', 'POST'))
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        try:
            post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
        except:
            flash('Something went wrong')
            return render_template('posts/create_post.html', form=form)

        return redirect(url_for('posts.post_detail', slug=post.slug))
    return render_template('posts/create_post.html', form=form)


@posts.route('/<slug>/edit', methods=('GET', 'POST'))
@login_required
def edit_post(slug):
    post = Post.query.filter((Post.slug == slug) & (Post.user_id == current_user.id)).first_or_404()
    if request.method == 'POST':
        form = PostForm(formdata=request.form, obj=post)
        form.populate_obj(post)
        db.session.commit()
        return redirect(url_for('posts.post_detail', slug=slug))
    form = PostForm(obj=post)
    return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/')
def index():
    q = request.args.get('q')
    page = request.args.get('page', 1, type=int)
    followed_posts = request.args.get('followed_posts', 0, type=int)
    posts = Post.query
    if current_user.is_authenticated and followed_posts == 1:
        posts = current_user.followed_posts()
    if q:
        posts = posts.filter(Post.title.contains(q) | Post.body.contains(q))
    posts = posts.order_by(Post.created.desc())
    pages = posts.paginate(page=page, per_page=app.config['POSTS_PER_PAGE'])
    return render_template('posts/index.html', pages=pages)


@posts.route('/<slug>')
def post_detail(slug):
    post = Post.query.filter(Post.slug == slug).first_or_404()
    return render_template('posts/post_detail.html', post=post)


@posts.route('tag/<slug>')
def tag_detail(slug):
    tag = Tag.query.filter(Tag.slug == slug).first_or_404()
    return render_template('posts/tag_detail.html', tag=tag, posts=tag.posts)
