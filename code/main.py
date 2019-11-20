from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

from flask_sqlalchemy import SQLAlchemy
#   Note: make sure you use flake8 or pylint-flask
#         because normal pylint will complain about
#         flask works

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


"""
    monster_type is an association table between the tables Monster and Type.
    The basic logic is:
        1.  Create a Monster
        2.  Create a Type
        3.  Add to monster_type to signify a given monster having any type.
"""
monster_type = db.Table('type-association', db.metadata,
                        db.Column('type_id',
                                  db.Integer,
                                  db.ForeignKey('type.id')),
                        db.Column('monster_id',
                                  db.Integer,
                                  db.ForeignKey('monster.id'))
                        )

monster_archetype = db.Table('archetype-association', db.metadata,
                             db.Column('archetype_id',
                                       db.Integer,
                                       db.ForeignKey('archetype.id')),
                             db.Column('monster_id',
                                       db.Integer,
                                       db.ForeignKey('monster.id'))
                             )


class Monster(db.Model):
    __tablename__ = "monster"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(25), unique=True, nullable=False)

    attack_points = db.Column(db.Integer, nullable=True, default=0)
    defense_points = db.Column(db.Integer, nullable=True, default=0)

    types = db.relationship("Type",
                            secondary=monster_type,
                            back_populates="monsters",
                            lazy=True)
    archetypes = db.relationship("Archetype",
                                 secondary=monster_archetype,
                                 back_populates="monsters",
                                 lazy=True)

    def __init__(self, name, attack_points, defense_points):
        self.name = name
        self.attack_points = attack_points
        self.defense_points = defense_points

    def __repr__(self):
        return (f"Monster('{self.name}', Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}')")


class Type(db.Model):
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    monsters = db.relationship("Monster",
                               secondary=monster_type,
                               back_populates="types",
                               lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Type('{self.name}')"


class Archetype(db.Model):
    __tablename__ = "archetype"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    monsters = db.relationship("Monster",
                               secondary=monster_archetype,
                               back_populates="archetypes",
                               lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Archetype('{self.name}')"


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Mana Clash Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Monster, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Archetype, db.session))


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register",
           methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created! Use {form.email.data} to log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login",
           methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if (form.email.data == "admin@example.com"
                and form.password.data == "password"):
            flash("You logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful!", 'danger')

    return render_template('login.html',
                           title='Log in',
                           form=form)


if __name__ == '__main__':
    app.run(debug=True)
