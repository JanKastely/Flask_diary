from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import logging

from diary.auth import login_required
from diary.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username, likes'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))


@bp.route('/<int:id>/like', methods=['POST'])
@login_required
def like(id):
    # Zde můžete provést zvýšení počtu "likes" pro příspěvek s ID=id v databázi
    # Po zpracování požadavku můžete poslat odpověď ve formátu JSON s aktuálním počtem "likes"

    db = get_db()

    try:
        db.execute('UPDATE post SET likes = likes + 1 WHERE id = ?', (id,))
        db.commit()
        post = db.execute('SELECT likes FROM post WHERE id = ?', (id,)).fetchone()

        # Zde přidáme print, který vypíše počet lajků do konzole serveru
        print(f"Počet lajků pro příspěvek s ID {id}: {post['likes']}")

        return jsonify({'like': post['likes']})
    except Exception as e:
        # Pokud dojde k chybě, zobrazíme ji v konzoli serveru
        print(f"Chyba při zpracování lajku pro příspěvek s ID {id}: {str(e)}")
        return jsonify({'error': 'Chyba při zpracování lajku'}), 500



