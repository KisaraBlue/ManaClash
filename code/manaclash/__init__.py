from flask import Flask

from flask_sqlalchemy import SQLAlchemy
#   Note: make sure you use flake8 or pylint-flask
#         because normal pylint will complain about
#         flask works
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_restplus import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

api = Api(app)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from manaclash import routes
from manaclash.models import Monster, Type, Archetype, Equipment, MonsterEffect
from manaclash.models import User, Game, Board
from manaclash.models import BoardMonster, BoardMonsterEffect
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Mana Clash Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Monster, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Archetype, db.session))
admin.add_view(ModelView(Equipment, db.session))
admin.add_view(ModelView(MonsterEffect, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Game, db.session))
admin.add_view(ModelView(Board, db.session))
admin.add_view(ModelView(BoardMonster, db.session))
admin.add_view(ModelView(BoardMonsterEffect, db.session))
# admin.add_view(ModelView(BoardEquipment, db.session))
