from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_bootstrap import Bootstrap


app = Flask(__name__)


app.config.from_object('config')


db = SQLAlchemy(app)


migrate = Migrate(app, db)


Bootstrap(app)


from app.shop.views import shop


app.register_blueprint(shop, url_prefix='/')
