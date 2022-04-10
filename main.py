import app.routes


from app import app

from app.posts.blueprint import posts


app.register_blueprint(posts, url_prefix='/blog')


from app.models import db, User, Post, Tag


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Tag': Tag}


if __name__ == '__main__':
    app.run()
