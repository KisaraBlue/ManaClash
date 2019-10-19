from manaclash import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cards = db.relationship('Card', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.Enum('Creature', 'Enchantment'), nullable=False)
    creature_type = db.Column(db.Enum('Humanoid', 'Beast', 'Spirit'))
    enchantment_type = db.Column(db.Enum('Ephemeral', 'Ongoing'))
    effect = db.Column(db.Text, nullable=False, default='No effect')
    mana_cost = db.Column(db.Integer, nullable=False, default=0)
    attack = db.Column(db.Integer, nullable=False, default=0)
    defense = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"Card('{self.name}', '{self.category}', '{self.date}')"
