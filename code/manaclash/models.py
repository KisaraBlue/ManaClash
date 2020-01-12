from manaclash import db, login_manager
from flask_login import UserMixin
from sqlalchemy.ext.associationproxy import association_proxy

"""
    table1_table2: many-to-many relationship between
                   table1 and table 2.
    monster_type: a monster can have many types (archetypes...)
    equipment_type: a piece of equipment can be applied to one or several types

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

deck_monster = db.Table('deck_monster-association', db.metadata,
                        db.Column('monster_id',
                                  db.Integer,
                                  db.ForeignKey('monster.id')),
                        db.Column('user_id',
                                  db.Integer,
                                  db.ForeignKey('user.id'))
                        )

deck_monster_effect = db.Table('deck_monster_effect-association', db.metadata,
                               db.Column('monster_effect_id',
                                         db.Integer,
                                         db.ForeignKey('monster_effect.id')),
                               db.Column('user_id',
                                         db.Integer,
                                         db.ForeignKey('user.id'))
                               )

deck_equipment = db.Table('deck_equipment-association', db.metadata,
                          db.Column('equipment_id',
                                    db.Integer,
                                    db.ForeignKey('equipment.id')),
                          db.Column('user_id',
                                    db.Integer,
                                    db.ForeignKey('user.id'))
                          )


class Monster(db.Model):
    __tablename__ = "monster"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

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
    users = db.relationship("User",
                            secondary=deck_monster,
                            back_populates="monsters",
                            lazy=True)

    def __init__(self, name, attack_points, defense_points):
        self.name = name
        self.attack_points = attack_points
        self.defense_points = defense_points

    def __repr__(self):
        return (f"Monster('{self.name}', Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}', ID: '{self.id}')")


class Type(db.Model):
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    users = db.relationship("User",
                            secondary=deck_equipment,
                            back_populates="equipment",
                            lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Equipment('{self.name}'), Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}')")


class MonsterEffect(db.Model):
    __tablename__ = "monster_effect"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    attack_points = db.Column(db.Integer, unique=False, nullable=True)
    defense_points = db.Column(db.Integer, unique=False, nullable=True)

    types = db.relationship("Type",
                            secondary=monster_effect_type,
                            back_populates="monster_effects",
                            lazy=True)
    archetypes = db.relationship("Archetype",
                                 secondary=monster_effect_archetype,
                                 back_populates="monster_effects",
                                 lazy=True)
    users = db.relationship("User",
                            secondary=deck_monster_effect,
                            back_populates="monster_effects",
                            lazy=True)

    def __init__(self, name, attack_points, defense_points):
        self.name = name
        self.attack_points = attack_points
        self.defense_points = defense_points

    def __repr__(self):
        return (f"Monster Effect('{self.name}'), Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}'), ID: '{self.id}'")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    wins = db.Column(db.Integer, unique=False, nullable=True, default=0)
    losses = db.Column(db.Integer, unique=False, nullable=True, default=0)
    ties = db.Column(db.Integer, unique=False, nullable=True, default=0)

    monsters = db.relationship("Monster",
                               secondary=deck_monster,
                               back_populates="users",
                               lazy=True)
    monster_effects = db.relationship("MonsterEffect",
                                      secondary=deck_monster_effect,
                                      back_populates="users",
                                      lazy=True)
    equipment = db.relationship("Equipment",
                                secondary=deck_equipment,
                                back_populates="users",
                                lazy=True)
    boards = db.relationship("Board")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return (f"User('{self.username}'), ID: {self.id}")


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    turn = db.Column(db.Integer, unique=False, nullable=True, default=0)

    player_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    player_one = db.relationship("User", foreign_keys=[player_one_id])
    player_two = db.relationship("User", foreign_keys=[player_two_id])

    boards = db.relationship("Board")

    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

    def __repr__(self):
        return (f"Game: Player 1('{self.player_one}') "
                f"Player 2('{self.player_two}') "
                f"Turn: '{self.turn}'")


class Board(db.Model):
    __tablename__ = "board"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    #   The below restriction is only temporary:
    #   with it, we restrict every player to a single game
    #   without it, it would be possible for admins to create
    #   several boards per player per game.
    #   suggested fix: make Board{Monster, MonsterEffect, Equipment}
    #   inherit game_id and user_id; this would resolve the problem.
    #   Doing this, however, is not trivial and would introduce some
    #   headache, so for now we will just avoid it and accept the restriction.
    #   Note: this might be an SQLite problem. Members of composite primary keys
    #   cannot be auto-incremented.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)

    game = db.relationship("Game", foreign_keys=[game_id])
    user = db.relationship("User", foreign_keys=[user_id])

    health = db.Column(db.Integer, nullable=True, default=10)

    monsters = association_proxy('board_monsters',
                                 'board')

    monster_effects = association_proxy('board_monster_effects',
                                        'board')
    equipment = association_proxy('board_equipment',
                                  'board')

    def __init__(self, game_id, user_id, health=10):
        self.game_id = game_id
        self.user_id = user_id
        self.health = health

    def __repr__(self):
        return (f"Board: Player('{self.user_id}') "
                f"Game('{self.game_id}') "
                f"Health: '{self.health}'")


import enum


class State(enum.Enum):
    Hand = 0
    Active = 1
    Discarded = 2


class BoardMonster(db.Model):
    __tablename__ = 'board_monster'
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board.id'),
                         primary_key=True)
    #   need to reference deck_monster.id, but can stay like this for now
    monster_id = db.Column(db.Integer,
                           db.ForeignKey('monster.id'),
                           primary_key=True)
    monster = db.relationship("Monster",
                              foreign_keys=[monster_id])

    state = db.Column(db.Enum(State), nullable=True, default=State.Hand)

    board = db.relationship(Board,
                            backref=db.backref("board_monsters",
                                               cascade="all, delete-orphan"))

    def __init__(self, monster):
        self.monster = monster


class BoardMonsterEffect(db.Model):
    __tablename__ = 'board_monster_effect'
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board.id'),
                         primary_key=True)
    #   need to reference deck_monster_effect.id, but can stay like this for now
    monster_effect_id = db.Column(db.Integer,
                                  db.ForeignKey('monster_effect.id'),
                                  primary_key=True)
    state = db.Column(db.Enum(State), nullable=True, default=0)

    board = db.relationship(Board,
                            backref=db.backref("board_monster_effects",
                                               cascade="all, delete-orphan"))

    monster_effect = db.relationship("MonsterEffect")

    def __init__(self, board, monster_effect, state=0):
        self.board = board
        self.monster_effect = monster_effect
        self.state = state


class BoardEquipment(db.Model):
    __tablename__ = 'board_equipment'
    board_id = db.Column(db.Integer,
                         db.ForeignKey('board.id'),
                         primary_key=True)
    #   need to reference deck_equipment.id, but can stay like this for now
    equipment_id = db.Column(db.Integer,
                             db.ForeignKey('equipment.id'),
                             primary_key=True)
    #   a piece of equipment needs a monster to be active
    monster_id = db.Column(db.Integer,
                           db.ForeignKey('monster.id'),
                           nullable=True)
    state = db.Column(db.Enum(State), nullable=True, default=0)

    board = db.relationship(Board,
                            backref=db.backref("board_equipment",
                                               cascade="all, delete-orphan"))

    equipment = db.relationship("Equipment")
    monster = db.relationship("Monster")

    def __init__(self, board, monster, equipment, state=0):
        self.board = board
        self.monster = monster
        self.equipment = equipment
        self.state = state
