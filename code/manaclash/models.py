from manaclash import db, login_manager
from flask_login import UserMixin

card_type = db.Table('type-association', db.metadata,
                        db.Column('type_id',
                                  db.Integer,
                                  db.ForeignKey('type.id')),
                        db.Column('card_id',
                                  db.Integer,
                                  db.ForeignKey('card.id'))
                        )

card_archetype = db.Table('archetype-association', db.metadata,
                             db.Column('archetype_id',
                                       db.Integer,
                                       db.ForeignKey('archetype.id')),
                             db.Column('card_id',
                                       db.Integer,
                                       db.ForeignKey('card.id'))
                             )

card_deck = db.Table('deck-association', db.metadata,
                             db.Column('deck_id',
                                       db.Integer,
                                       db.ForeignKey('deck.id')),
                             db.Column('card_id',
                                       db.Integer,
                                       db.ForeignKey('card.id'))
                             )

user_deck = db.Table('deck-user-association', db.metadata,
                             db.Column('deck_id',
                                       db.Integer,
                                       db.ForeignKey('deck.id')),
                             db.Column('user_id',
                                       db.Integer,
                                       db.ForeignKey('user.id'))
                             )


class Card(db.Model):
    __tablename__ = "card"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(25), unique=True, nullable=False)

    attack_points = db.Column(db.Integer, nullable=True, default=0)
    defense_points = db.Column(db.Integer, nullable=True, default=0)
    duration = db.Column(db.Integer, nullable=True, default=1000)

    types = db.relationship("Type",
                            secondary=card_type,
                            back_populates="cards",
                            lazy=True)
    archetypes = db.relationship("Archetype",
                                 secondary=card_archetype,
                                 back_populates="cards",
                                 lazy=True)
    decks = db.relationship("Deck",
                                 secondary=card_deck,
                                 back_populates="cards",
                                 lazy=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id'))
    category = db.relationship("Category", foreign_keys=[category_id], back_populates="cards")
    in_game = db.relationship("CardsInGame",
                             back_populates="card",
                             lazy=True)


    def __init__(self, name, attack_points, defense_points, duration):
        self.name = name
        self.attack_points = attack_points
        self.defense_points = defense_points
        self.duration = duration

    def __repr__(self):
        return (f"Card('{self.name}', Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}', Duration: {self.duration}, ID: '{self.id}')")


class Type(db.Model):
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    cards = db.relationship("Card",
                               secondary=card_type,
                               back_populates="types",
                               lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Type('{self.name}')"

class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    cards = db.relationship("Card",
                               back_populates="category",
                               lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Category('{self.name}')"

class Archetype(db.Model):
    __tablename__ = "archetype"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    cards = db.relationship("Card",
                               secondary=card_archetype,
                               back_populates="archetypes",
                               lazy=True)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Archetype('{self.name}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    wins = db.Column(db.Integer, unique=False, nullable=True, default=0)
    losses = db.Column(db.Integer, unique=False, nullable=True, default=0)
    ties = db.Column(db.Integer, unique=False, nullable=True, default=0)

    decks = db.relationship("Deck",
                                 secondary=user_deck,
                                 back_populates="users",
                                 lazy=True)

    playing = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return (f"User('{self.username}'), ID: {self.id}")


class Deck(db.Model):
    __tablename__="deck"

    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User",
                                 secondary=user_deck,
                                 back_populates="decks",
                                 lazy=True)
    cards = db.relationship("Card",
                                 secondary=card_deck,
                                 back_populates="decks",
                                 lazy=True)

class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)

    turn = db.Column(db.Integer, unique=False, nullable=True, default=0)

    player_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    player_one = db.relationship("User", foreign_keys=[player_one_id])
    player_two = db.relationship("User", foreign_keys=[player_two_id])

    health_one = db.Column(db.Integer, unique=False, nullable=True, default=10)
    health_two = db.Column(db.Integer, unique=False, nullable=True, default=10)

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

    def __repr__(self):
        return (f"Game: Player 1('{self.player_one}') "
                f"Player 2('{self.player_two}') "
                f"Turn: '{self.turn}'")


class CardsInGame(db.Model):
    __tablename__ = "cardsingame"

    id = db.Column(db.Integer, primary_key=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    player = db.Column(db.Integer, unique=False, nullable=True, default=0)
    state = db.Column(db.Integer, unique=False, nullable=True, default=0)
    duration = db.Column(db.Integer, unique=False, nullable=True, default=1000)

    """linked_to = db.relationship("CardsInGame",
                backref=db.backref('equiped_with', remote_side=[id])
            )"""
    linked_to_id = db.Column(db.Integer,
                            db.ForeignKey('cardsingame.id'))
    linked_to = db.relationship("CardsInGame", foreign_keys=[linked_to_id], backref=db.backref('equiped_with', remote_side=[id]), lazy=True)

    card_id = db.Column(db.Integer,
                            db.ForeignKey('card.id'))
    card = db.relationship("Card", foreign_keys=[card_id], back_populates="in_game", lazy=True)

    def __init__(self, game_id, player, card, state, duration):
        self.game_id = game_id
        self.player = player
        self.card = card
        self.state = state
        self.duration = duration

    def __repr__(self):
        return (f"Card in Game: Player('{self.player}') "
                f"Game('{self.game_id}') "
                f"Card('{self.card}') "
                f"State('{self.state}') "
                f"Duration: '{self.duration}'")
