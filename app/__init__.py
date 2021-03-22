from flask import Flask
from app.config import Config
from app.models import db
from flask_migrate import Migrate

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from app.books.routes import books_bp
    from app.home.routes import home_bp
    from app.members.routes import members_bp
    from app.transactions.routes import transactions_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(transactions_bp)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
