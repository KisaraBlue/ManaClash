from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Monster(db.Model):
    __tablename__ = "monsters"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(25), unique=True, nullable=False)

    attack_points = db.Column(db.Integer, nullable=True, default=0)
    defense_points = db.Column(db.Integer, nullable=True, default=0)

    #   spirit = db.Column(db.BooleanField)
    #   humanoid = db.Column(db.BooleanField)
    #   beast = db.Column(db.BooleanField)

    #   archetype_id = db.Column(db.Integer,
    #                            db.ForeignKey('archetype.id'),
    #                            nullable=False)
    #   archetype = db.relationship('Archetype',
    #                               back_populates='monsters',
    #                               lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Monster('{self.name}')"


class Effect(db.Model):
    __tablename__ = "effects/equipment"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)
    #   type = db.Column()

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return f"Effect('{self.name}'), on '{self.type}'"


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
