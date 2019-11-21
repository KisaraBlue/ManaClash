from manaclash import db

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

user_monster = db.Table('user_monster-association', db.metadata,
                        db.Column('monster_id',
                                  db.Integer,
                                  db.ForeignKey('monster.id')),
                        db.Column('user_id',
                                  db.Integer,
                                  db.ForeignKey('user.id'))
                        )

user_monster_effect = db.Table('user_monster_effect-association', db.metadata,
                               db.Column('monster_effect_id',
                                         db.Integer,
                                         db.ForeignKey('monster_effect.id')),
                               db.Column('user_id',
                                         db.Integer,
                                         db.ForeignKey('user.id'))
                               )

user_equipment = db.Table('user_equipment-association', db.metadata,
                          db.Column('equipment_id',
                                    db.Integer,
                                    db.ForeignKey('equipment.id')),
                          db.Column('user_id',
                                    db.Integer,
                                    db.ForeignKey('user.id'))
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
    users = db.relationship("User",
                            secondary=user_monster,
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
    users = db.relationship("User",
                            secondary=user_equipment,
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
    users = db.relationship("User",
                            secondary=user_monster_effect,
                            back_populates="monster_effects",
                            lazy=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return (f"Equipment('{self.name}'), Attack: {self.attack_points}, "
                f"Defense: '{self.defense_points}')")


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False, nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    wins = db.Column(db.Integer, unique=False, nullable=True, default=0)
    losses = db.Column(db.Integer, unique=False, nullable=True, default=0)
    ties = db.Column(db.Integer, unique=False, nullable=True, default=0)

    monsters = db.relationship("Monster",
                               secondary=user_monster,
                               back_populates="users",
                               lazy=True)
    monster_effects = db.relationship("MonsterEffect",
                                      secondary=user_monster_effect,
                                      back_populates="users",
                                      lazy=True)
    equipment = db.relationship("Equipment",
                                secondary=user_equipment,
                                back_populates="users",
                                lazy=True)


class Game(db.Model):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)

    turn = db.Column(db.Integer, unique=False, nullable=True, default=0)

    player_one_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    player_two_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    player_one = db.relationship("User", foreign_keys=[player_one_id])
    player_two = db.relationship("User", foreign_keys=[player_two_id])
