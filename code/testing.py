from manaclash import db

db.drop_all()
db.create_all()

from manaclash import User, Game, Board
from manaclash import Monster, MonsterEffect
from manaclash import BoardMonster
from manaclash import Type
from manaclash.models import State

#   create some users
charlie = User(username='charlie',
               email='charlie@lsv.fr',
               password='justapassword')
david = User(username='david',
             email='david@lsv.fr',
             password='justapassword')

db.session.add_all([charlie, david])
db.session.commit()
print(charlie, david)

#   create some types
philosopher = Type('Philosopher')
olympian = Type('Olympian')
db.session.add_all([philosopher, olympian])
db.session.commit()

#    create some monsters
nietzsche = Monster(name='Friedrich Nietzsche',
                    attack_points=300,
                    defense_points=200)
frege = Monster(name='Gottlob Frege',
                attack_points=200,
                defense_points=250)
hume = Monster(name='David Hume',
               attack_points=300,
               defense_points=150)


poseidon = Monster(name='Poseidon',
                   attack_points=200,
                   defense_points=250)
hades = Monster(name='Hades',
                attack_points=250,
                defense_points=250)
zeus = Monster(name='Zeus',
               attack_points=150,
               defense_points=150)
#    give monsters types
nietzsche.types.append(philosopher)
frege.types.append(philosopher)
hume.types.append(philosopher)

poseidon.types.append(olympian)
hades.types.append(olympian)
zeus.types.append(olympian)

db.session.add_all([nietzsche, frege, hume, poseidon, zeus, hades])
db.session.commit()

"""
print(Monster.query.filter(Monster.types.any(Type.name == 'Philosopher')).all())
"""

david.monsters.append(nietzsche)
david.monsters.append(frege)
david.monsters.append(hume)

charlie.monsters.append(poseidon)
charlie.monsters.append(zeus)
charlie.monsters.append(hades)

db.session.add_all([david, charlie])
db.session.commit()


from controller import Controller

Battle = Controller(david, charlie)
Battle.play()

# print([monster.id for monster in david.monsters])

david.boards[0].monsters.append(nietzsche)
