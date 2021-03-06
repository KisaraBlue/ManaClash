from flask import render_template, flash, redirect, url_for, request
from manaclash import app, db, bcrypt, api
from manaclash.forms import RegistrationForm, LoginForm
from manaclash.models import User, Monster, MonsterEffect, State
from manaclash.models import BoardMonster, BoardMonsterEffect
from manaclash.models import Game, Board

from flask_login import login_user, current_user, logout_user, login_required

from flask_restplus import Resource

import random


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html',
                           title='Register',
                           form=form)


@app.route("/login",
           methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page \
                else redirect(url_for('home'))
        else:
            flash("Login unsuccessful!", 'danger')

    return render_template('login.html',
                           title='Log in',
                           form=form)


@app.route("/logout",
           methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html',
                           title='Account')


@api.route('/user/id=<int:id>',
           doc={'description': 'Get User stats from user id.'})
@api.doc(params={'id': 'User ID'})
class GetUserStats(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {
            'id': id,
            'username': user.username,
            'email': user.email,
            'wins': user.win,
            'losses': user.loss,
            'ties': user.tie
        }


@api.route('/user/board/id=<int:id>',
           doc={'description': 'Get all user boards from user id.'})
@api.doc(params={'id': 'User ID'})
class GetUserBoards(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        return {
            i: user.boards[i].id for i in range(0, len(user.boards))
        }


@api.route('/monster/id=<int:id>',
           doc={'description': 'Get monster name and attributes from id.'})
@api.doc(params={'id': 'Monster ID'})
class GetMonsterStats(Resource):
    def get(self, id):
        monster = Monster.query.filter_by(id=id).first()
        return {
            'id': id,
            'name': monster.name,
            'attack': monster.attack_points,
            'defense': monster.defense_points
        }


@api.route('/monster/type/id=<int:id>',
           doc={'description': 'Get monster types from id.'})
@api.doc(params={'id': 'Monster ID'})
class GetMonsterType(Resource):
    def get(self, id):
        monster = Monster.query.filter_by(id=id).first()

        return{
            i: monster.types[i].name for i in range(0, len(monster.types))
        }


@api.route('/monster/archetype/id=<int:id>',
           doc={'description': 'Get monster archetypes from id.'})
@api.doc(params={'id': 'Monster ID'})
class GetMonsterArchetype(Resource):
    def get(self, id):
        monster = Monster.query.filter_by(id=id).first()

        return{
            i: monster.archetypes[i]
                      .name for i in range(0, len(monster.archetypes))
        }


@api.route('/effect/monster/id=<int:id>',
           doc={'description': 'Get monster effect name, '
                               'attack bonus, and defense bonus from id.'})
@api.doc(params={'id': 'MonsterEffect ID'})
class GetMonsterEffectStats(Resource):
    def get(self, id):
        monster_effect = MonsterEffect.query.filter_by(id=id).first()

        return{
            'id': monster_effect.id,
            'name': monster_effect.name,
            'attack': monster_effect.attack_points,
            'defense': monster_effect.defense_points
        }


@api.route('/effect/monster/type/id=<int:id>',
           doc={'description': 'Get monster effect types '
                               'from id.'})
@api.doc(params={'id': 'MonsterEffect ID'})
class GetMonsterEffectType(Resource):
    def get(self, id):
        monster_effect = MonsterEffect.query.filter_by(id=id).first()

        return{
            i: monster_effect.types[i]
                             .name for i in range(0, len(monster_effect.types))
        }


@api.route('/effect/monster/archetype/id=<int:id>',
           doc={'description': 'Get monster effect archetypes '
                               'from id.'})
@api.doc(params={'id': 'MonsterEffect ID'})
class GetMonsterEffectArchetype(Resource):
    def get(self, id):
        monster_effect = MonsterEffect.query.filter_by(id=id).first()

        return{
            i: monster_effect.archetypes[i]
                             .name for i in range(0,
                                                  len(monster_effect.archetypes))
        }


@api.route('/board/id=<int:id>',
           doc={'description': 'Get game_id, board (player) health '
                               'from id.'})
@api.doc(params={'id': 'Board ID'})
class GetBoardStats(Resource):
    def get(self, id):
        board = Board.query.filter_by(id=id).first()

        return{
            'id': board.id,
            'game_id': board.game_id,
            'health': board.health
        }


@api.route('/board/hand/id=<int:id>',
           doc={'description': 'Get all cards (monsters and monster effects) '
                               'in hand on a board '
                               'from id.'})
@api.doc(params={'id': 'Board ID'})
class GetBoardHand(Resource):
    def get(self, id):
        hand_monsters = BoardMonster.query\
                                    .filter_by(board_id=id,
                                               state=State.Hand).all()
        hand_monster_effects = BoardMonsterEffect.query\
                                                 .filter_by(board_id=id,
                                                            state=State.Hand)\
                                                 .all()
        return{
            'monsters': {
                i: hand_monsters.id[i] for i in range(0,
                                                      len(hand_monsters))
            },
            'monster-effects': {
                i: hand_monster_effects.id[i]
                for i in range(0, len(hand_monster_effects))
            }
        }


@api.route('/board/field/id=<int:id>',
           doc={'description': 'Get all cards (monsters and monster effects) '
                               'on field (active) on a board '
                               'from id.'})
@api.doc(params={'id': 'Board ID'})
class GetBoardField(Resource):
    def get(self, id):
        field_monsters = BoardMonster.query\
                                     .filter_by(board_id=id,
                                                state=State.Field).all()
        field_monster_effects = BoardMonsterEffect.query\
                                                  .filter_by(board_id=id,
                                                             state=State.Field)\
                                                  .all()
        return{
            'monsters': {
                i: field_monsters.id[i] for i in range(0,
                                                       len(field_monsters))
            },
            'monster-effects': {
                i: field_monster_effects.id[i]
                for i in range(0, len(field_monster_effects))
            }
        }


@api.route('/board/discarded/id=<int:id>',
           doc={'description': 'Get all cards (monsters and monster effects) '
                               'that were discarded (graveyard) on a board '
                               'from id.'})
@api.doc(params={'id': 'Board ID'})
class GetBoardDiscarded(Resource):
    def get(self, id):
        dead_monsters = BoardMonster.query\
                                    .filter_by(board_id=id,
                                               state=State.Discarded).all()
        dead_monster_effects = BoardMonsterEffect.query\
                                                 .filter_by(board_id=id,
                                                            state=State.Discarded)\
                                                 .all()
        return{
            'monsters': {
                i: dead_monsters.id[i] for i in range(0,
                                                      len(dead_monsters))
            },
            'monster-effects': {
                i: dead_monster_effects.id[i]
                for i in range(0, len(dead_monster_effects))
            }
        }


@api.route('/game/player1=<int:id1>/player2=<int:id2>',
           doc={'description': 'Create a new game between two players '
                               'from two user IDs.'})
@api.doc(params={'id1': 'Player One ID',
                 'id2': 'Player Two ID'})
class CreateGame(Resource):
    def put(self, id1, id2):
        player_one = User.query.filter_by(id=id1).first()
        player_two = User.query.filter_by(id=id2).first()

        game = Game(player_one=player_one,
                    player_two=player_two)
        board_one = Board(game.id, player_one.id)
        board_two = Board(game.id, player_two.id)

        db.session.add_all([board_one, board_two])
        db.session.commit()

        return{
            'id': game.id,
            'board_one': board_one.id,
            'board_two': board_two.id
        }


@api.route(
    '/board/activate/'
    'monster/monster=<int:monster_id>/board=<int:board_id>',
    doc={'description': 'Place monster on field '
                        'on a board '
                        'from monster id and board id.'})
@api.doc(params={'monster_id': 'Monster ID',
                 'board_id': 'Board ID'})
class ActivateMonster(Resource):
    def put(self, monster_id, board_id):
        board = Board.query.filter_by(id=board_id)

        BoardMonster.query.filter_by(monster_id=monster_id,
                                     board_id=board_id)\
                          .first()\
                          .state = State.Field

        db.session.add(board)
        db.session.commit()

        return{
            'board_id': board_id
        }


@api.route(
    '/board/activate/'
    'effect/monster/id=<int:id>/board=<int:board_id>',
    doc={'description': 'Activate Monster Effect '
                        'on a board '
                        'from monster_effect id and board id.'})
@api.doc(params={'id': 'MonsterEffect ID',
                 'board_id': 'Board ID'})
class ActivateMonsterEffect(Resource):
    def put(self, id, board_id):
        board = Board.query.filter_by(id=board_id)

        BoardMonsterEffect.query.filter_by(monster_effect_id=id,
                                           board_id=board_id)\
                          .first()\
                          .state = State.Field

        db.session.add(board)
        db.session.commit()

        return{
            'board_id': board_id
        }


@api.route(
    '/board/evaluate/'
    'effects/monster/id=<int:board_id>/monster_id=<int:monster_id>',
    doc={'description': 'Evaluate all active MonsterEffects on board '
                        'for a monster '
                        'from monster id and board id.'})
@api.doc(params={'monster_id': 'Monster ID',
                 'board_id': 'Board ID'})
class EvaluateMonsterEffects(Resource):
    def get(self, board_id, monster_id):
        board = Board.query.filter_by(id=board_id)
        monster = Monster.query.filter_by(id=monster_id).first()

        attack_bonus = 0
        defense_bonus = 0

        for effect in board.monster_effects:
            if effect.state is State.Field:
                common_types = False
                common_archetypes = 0

                for type in monster.types:
                    if type in effect.types:
                        common_types = True
                for archetype in monster.archetypes:
                    if archetype in effect.archetypes:
                        common_archetypes = True

                if (common_types or common_archetypes) or \
                   (not effect.types and not effect.archetypes):
                    attack_bonus = attack_bonus + effect.attack_points
                    defense_bonus = defense_bonus + effect.defense_points
        return{
            'attack_bonus': attack_bonus,
            'defense_bonus': defense_bonus
        }


@api.route(
    '/board/discard/'
    'monster/monster_id=<int:monster_id>/board_id=<int:board_id>',
    doc={'description': 'Discard a monster from board '
                        'from monster id and board id. '
                        'Also decrements player health.'})
@api.doc(params={'monster_id': 'Monster ID',
                 'board_id': 'Board ID'})
class DiscardMonster(Resource):
    def put(self, monster_id, board_id):
        #   if a monster is being discarded, a player loses a health point
        board = Board.query.filter_by(id=board_id)
        board.health = board.health - 1

        BoardMonster.query.filter_by(monster_id=monster_id,
                                     board_id=board_id)\
                          .first()\
                          .state = State.Discarded

        db.session.add(board)
        db.session.commit()

        return{
            'board_id': board_id
        }


@api.route(
    '/board/discard/'
    'effect/monster/id=<int:id>/board_id=<int:board_id>',
    doc={'description': 'Discard a monster effect from board '
                        'from monster_effect id and board id. '})
@api.doc(params={'id': 'MonsterEffect ID',
                 'board_id': 'Board ID'})
class DiscardMonsterEffect(Resource):
    def put(self, id, board_id):
        board = Board.query.filter_by(id=board_id)

        BoardMonsterEffect.query.filter_by(monster_effect_id=id,
                                           board_id=board_id)\
                          .first()\
                          .state = State.Discarded

        db.session.add(board)
        db.session.commit()

        return{
            'board_id': board_id
        }


@api.route(
    '/board/draw/'
    'user_id=<int:user_id>/board_id=<int:board_id>',
    doc={'description': 'Draw a card for a user from user deck. '
                        'Adds card to user hand on given board. '})
@api.doc(params={'user_id': 'User ID',
                 'board_id': 'Board ID'})
class Draw(Resource):
    def put(self, user_id, board_id):
        user = User.query.filter_by(id=user_id).first()
        user_board = Board.query.filter_by(id=board_id).first()

        new_card = False
        enough_cards = True

        NUM_OF_MONSTERS = len(user.monsters)
        NUM_OF_MONSTER_EFFECTS = len(user.monster_effects)
        NUM_OF_EQUIPMENT = len(user.equipment)

        while (not new_card) and enough_cards:
            x = random.randrange(0, NUM_OF_MONSTERS
                                 + NUM_OF_MONSTER_EFFECTS
                                 + NUM_OF_EQUIPMENT)

            if x in range(0, NUM_OF_MONSTERS - 1):
                #   Here we retrieve a monster from the deck and place it
                #   in a user's hand.
                y = 0

                type = "Monster"

                while (not new_card) and (y < NUM_OF_MONSTERS)\
                        and enough_cards:

                    new_monster = user.monsters[y]

                    board_monsters = [monster.id
                                      for monster in user_board.monsters]

                    if new_monster.id not in board_monsters:
                        id = new_monster.id
                        user_board.monsters.append(new_monster)
                        new_card = True
                    else:
                        print("Monster already added!")
                    y = y + 1
                    if y == NUM_OF_MONSTERS:
                        enough_cards = False
                        #    Go to MonsterEffect deck
                        x = NUM_OF_MONSTERS
                        # print("No more cards!")

            elif x in range(NUM_OF_MONSTERS,
                            NUM_OF_MONSTERS
                            + NUM_OF_MONSTER_EFFECTS - 1):
                y = 0
                type = "Monster Effect"
                while (not new_card) and (y < NUM_OF_MONSTERS)\
                        and enough_cards:

                    if NUM_OF_MONSTER_EFFECTS != 0:
                        new_monster_effect = user.monster_effects[y]
                        id = new_monster_effect.id
                    else:
                        new_monster_effect = None
                    if new_monster_effect is not None:
                        board_monster_effects = [effect.id
                                                 for effect
                                                 in user_board.monster_effects]
                        if new_monster_effect.id not in board_monster_effects:
                            new_card = True
                        user_board.monster_effects\
                                  .append(new_monster_effect)
                    y = y + 1
        db.session.add(user_board)
        db.session.commit()

        return{
            'type': type,
            'card_id': id,
            'board_id': user_board.id
        }
