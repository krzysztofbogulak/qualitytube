from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from qualitytube import db
from flask_login import current_user, login_required
from qualitytube.models import Post
from qualitytube.posts.forms import PostForm
import pafy


posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        video = form.video.data.split('watch?v=')[1]
        video = video.split('&')[0]
        post = Post(title=form.title.data,
                    description=form.description.data,
                    author=current_user,
                    video=video)

        db.session.add(post)
        db.session.commit()

        flash('Post został dodany', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html',
                           title='Dodaj nowy materiał',
                           form=form,
                           legend='Dodaj nowy materiał')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)

    url = "https://www.youtube.com/watch?v=" + post.video
    video = pafy.new(url)
    best = video.getbest()
    streams = video.streams
    streams_url_list = []
    streams_res_list = []
    streams_ext_list = []
    for stream in streams:
        streams_url_list.append(stream.url)
        streams_res_list.append(stream.resolution)
        streams_ext_list.append(stream.extension)

    return render_template('post_detail.html',
                           title=post.title,
                           post=post,
                           best_url=best.url,
                           ext=best.extension,
                           yid=post_id,
                           views=video.viewcount,
                           li_do=zip(streams_url_list, streams_res_list, streams_ext_list))


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.video = form.video.data
        db.session.commit()
        flash('Post został zaktualizowany',
              'success')

        return redirect(url_for('posts.post',
                                post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.video.data = post.video
    return render_template('create_post.html',
                           title='Aktualizuj wpis',
                           form=form,
                           legend='Aktualizuj wpis')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post został usunięty', 'success')
    return redirect(url_for('main.home'))
