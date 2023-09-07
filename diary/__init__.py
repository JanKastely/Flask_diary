import os
import sqlite3
from flask import Flask, jsonify, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',DATABASE=os.path.join(app.instance_path, 'diary.sqlite'),)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return "Hello, World!"

    @app.route('/blog/like/<int:post_id>', methods=['POST'])
    def like(post_id):
        if request.method == 'POST':
            # Otevřít spojení s databází
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor()

            # Získat aktuální počet "like" pro příspěvek
            cursor.execute("SELECT likes FROM post WHERE id = ?", (post_id,))
            current_likes = cursor.fetchone()[0]

            # Zvýšit hodnotu "like" pro příspěvek o 1
            new_likes = current_likes + 1

            # Aktualizovat hodnotu "like" v databázi
            cursor.execute("UPDATE post SET likes = ? WHERE id = ?", (new_likes, post_id))
            conn.commit()
            conn.close()

            return jsonify({'message': 'Liked successfully', 'likes': new_likes})

    from diary import db
    db.init_app(app)

    from diary import auth
    app.register_blueprint(auth.bp)

    from diary import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)