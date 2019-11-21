from flask import Flask

from flask_sqlalchemy import SQLAlchemy
#   Note: make sure you use flake8 or pylint-flask
#         because normal pylint will complain about
#         flask works


app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


from manaclash import routes


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from manaclash.models import Monster, Type, Archetype, Equipment, MonsterEffect
# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Mana Clash Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Monster, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Archetype, db.session))
admin.add_view(ModelView(Equipment, db.session))
admin.add_view(ModelView(MonsterEffect, db.session))
