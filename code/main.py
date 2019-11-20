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

equipment_type = db.Table('equipment-type-association', db.metadata,
                          db.Column('type_id',
                                    db.Integer,
                                    db.ForeignKey('type.id')),
                          db.Column('equipment_id',
                                    db.Integer,
                                    db.ForeignKey('equipment.id'))
                          )
equipment_archetype = db.Table('equipment-archetype-association', db.metadata,
                               db.Column('archetype_id',
                                         db.Integer,
                                         db.ForeignKey('archetype.id')),
                               db.Column('equipment_id',
                                         db.Integer,
                                         db.ForeignKey('equipment.id'))
                               )

monster_effect_type = db.Table('monster_effect-type-association', db.metadata,
                               db.Column('type_id',
                                         db.Integer,
                                         db.ForeignKey('type.id')),
                               db.Column('monster_effect_id',
                                         db.Integer,
                                         db.ForeignKey('monster_effect.id'))
                               )

monster_effect_archetype = db.Table('monster_effect-archetype_association',
                                    db.metadata,
                                    db.Column('archetype_id',
                                              db.Integer,
                                              db.ForeignKey('archetype.id')),
                                    db.Column('monster_effect_id',
                                              db.Integer,
                                              db.ForeignKey('monster_effect.id'))
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
    equipment = db.relationship("Equipment",
                                secondary=equipment_type,
                                back_populates="types",
                                lazy=True)
    monster_effects = db.relationship("MonsterEffect",
                                      secondary=monster_effect_type,
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
    equipment = db.relationship("Equipment",
                                secondary=equipment_archetype,
                                back_populates="archetypes",
                                lazy=True)
    monster_effects = db.relationship("MonsterEffect",
                                      secondary=monster_effect_archetype,
                                      back_populates="archetypes",
                                      lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Archetype('{self.name}')"


class Equipment(db.Model):
    __tablename__ = "equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    #   SQLAlchemy supports JSON as a data type in a column
    #   However: adding using our current admin panel would be annoying,
    #   because users would have to write in JSON format.
    #   We need to modify the Update operator for this specific class
    #   if we want probabilistic modification of monster attributes.
    attack = db.Column(db.Integer, unique=False, nullable=False)
    defense = db.Column(db.Integer, unique=False, nullable=False)

    types = db.relationship("Type",
                            secondary=equipment_type,
                            back_populates="equipment",
                            lazy=True)
    archetypes = db.relationship("Archetype",
                                 secondary=equipment_archetype,
                                 back_populates="equipment",
                                 lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Equipment('{self.name}'), Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}')")


class MonsterEffect(db.Model):
    __tablename__ = "monster_effect"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    #   SQLAlchemy supports JSON as a data type in a column
    #   However: adding using our current admin panel would be annoying,
    #   because users would have to write in JSON format.
    #   We need to modify the Update operator for this specific class
    #   if we want probabilistic modification of monster attributes.
    attack = db.Column(db.Integer, unique=False, nullable=False)
    defense = db.Column(db.Integer, unique=False, nullable=False)

    types = db.relationship("Type",
                            secondary=monster_effect_type,
                            back_populates="monster_effects",
                            lazy=True)
    archetypes = db.relationship("Archetype",
                                 secondary=monster_effect_archetype,
                                 back_populates="monster_effects",
                                 lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Equipment('{self.name}'), Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}')")


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Mana Clash Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(Monster, db.session))
admin.add_view(ModelView(Type, db.session))
admin.add_view(ModelView(Archetype, db.session))
admin.add_view(ModelView(Equipment, db.session))
admin.add_view(ModelView(MonsterEffect, db.session))


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
