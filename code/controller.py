import random

from manaclash import db
# db.drop_all()
# db.create_all()

from manaclash import User, Game, Board
from manaclash import Monster, MonsterEffect
from manaclash import BoardMonster
from manaclash import Type
from manaclash.models import State

import sys


def query_yes_no(question, default="yes"):
    """
    source: http://code.activestate.com/recipes/577058/
    Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


class Controller():
    def __init__(self, player_one, player_two):
        self.game = Game(player_one=player_one,
                         player_two=player_two)
        self.game.turn = 0
        print("Game:", self.game)

        self.player_one = player_one
        self.player_two = player_two
        print("Players: ", self.player_one, self.player_two)

        self.board_one = Board(self.game.id, self.game.player_one.id)
        self.board_two = Board(self.game.id, self.game.player_two.id)

        db.session.add(self.game)
        db.session.add(self.board_one)
        db.session.add(self.board_two)
        db.session.commit()

    def activate_monster(self, monster, board):
        board.monsters.append(monster)
        BoardMonster.query.filter_by(monster_id=monster.id,
                                     board_id=board.id)\
                          .first()\
                          .state = State.Active

        db.session.add(board)
        db.session.commit()

    def activate_monster_effect(self, effect, board):
        board.monster_effects.append(effect)
        board.monster_effects.remove(effect)
        db.session.add(board)
        db.session.commit()

    def evaluate_effects(self, board, monster):
        """
        Evaluate all active MonsterEffects on a given Monster.
        Input:
            -   The player's board
            -   Monster
        Output:
            -   tuple(attack_bonus, defense_bonus) where attack_bonus
                is how much the attack_points of the monster are changed,
                and defense_bonus is how much the defense_points of the monster
                are changed.
        """
        attack_bonus = 0
        defense_bonus = 0

        for effect in board.monster_effects:
            if effect.state is State.Active:
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
                    print(effect)
                    attack_bonus = attack_bonus + effect.attack_points
                    defense_bonus = defense_bonus + effect.defense_points
        return (attack_bonus, defense_bonus)

    def evaluate_equipment(self, board, monster):
        """
        For now, we will not allow a player to draw any equipment cards, and so
        this will not be included in the Phase One submission.
        """
        pass

    def attack(self, boards, attacker, defender):
        """
        Execute an attack from monster (attacker) on another monster (defender).
        Evaluates all effects on the field first.
        One limitation: a player's effects only affect their own monsters.
        Input:
            -   boards: both player boards. Consider adding check to make sure
                        that the boards correspond to same game later.
            -   attacker: attacking monster
            -   defender: defending monster
        Output:
            -   boards: modified boards after executing the attack, i.e.
                        new health values and with or without the monster, based
                        on the result of the attack.
        """
        attacker_eval = self.evaluate_effects(boards[0], attacker)[0]
        defender_eval = self.evaluate_effects(boards[1], defender)[1]

        total_attack = attacker.attack_points + attacker_eval
        total_defense = defender.defense_points + defender_eval

        if total_attack > total_defense:
            print(attacker, defender)
            boards[1].health = boards[1].health - 1
            boards[1].monsters.remove(defender)

            print("Attack succeeded!")
        else:
            print("Attack failed!")

        return boards

    def draw(self, user, user_board):
        new_card = False

        NUM_OF_MONSTERS = len(user.monsters)
        NUM_OF_MONSTER_EFFECTS = len(user.monster_effects)
        NUM_OF_EQUIPMENT = len(user.equipment)

        x = random.randrange(0, NUM_OF_MONSTERS
                             + NUM_OF_MONSTER_EFFECTS
                             + NUM_OF_EQUIPMENT)
        while not new_card:
            #   possible infinite loop: no more new cards in deck.
            #   suggested fix: check if number of cards that are
            #   in user board is less than (strictly) the number
            #   of cards in deck.
            if x in range(0, NUM_OF_MONSTERS - 1):
                #   Here we retrieve a monster from the deck and place it
                #   in a user's hand.
                y = 0
                print("getting monster")
                while not new_card and y < len(user.monsters):
                    new_monster = user.monsters[y]
                    if new_monster not in user_board.monsters \
                       and new_monster not in user_board.monsters:

                        print(new_monster.id)
                        user_board.monsters.append(new_monster)

                        new_card = True
                    y = y + 1
            elif x in range(NUM_OF_MONSTERS,
                            NUM_OF_MONSTERS
                            + NUM_OF_MONSTER_EFFECTS - 1):
                y = 0
                print("getting monstereffect")
                while not new_card and y < len(user.monster_effects):
                    if len(user.monster_effects) != 0:
                        new_monster_effect = user.monster_effects[y]
                    else:
                        new_monster_effect = None
                    if new_monster_effect is not None:
                        if new_monster_effect not in user_board.monster_effects:
                            new_card = True
                        user_board.monster_effects\
                                  .append(new_monster_effect)
                    y = y + 1

            elif x in range(NUM_OF_MONSTERS + NUM_OF_MONSTER_EFFECTS,
                            NUM_OF_MONSTERS
                            + NUM_OF_MONSTER_EFFECTS
                            + NUM_OF_EQUIPMENT - 1):
                y = 0
                print("getting equipment")
                while not new_card and y < len(user.equipment):
                    if len(user.equipment) != 0:
                        new_equipment = user.equipment[y]
                    else:
                        new_equipment = None
                    if new_equipment is not None:
                        if new_equipment not in user_board.equipment:
                            new_card = True
                        user_board.equipment\
                                  .append(new_equipment)
                    y = y + 1
            else:
                print("Error!!!!! Random number not in range!!!!!")
        db.session.add(user_board)
        db.session.commit()
        return user_board

    def play(self):
        print("Game started.")
        print("Drawing initial hand.")
        for i in range(6):
            self.draw(self.player_one, self.board_one)
            self.draw(self.player_two, self.board_two)

        win_condition = False
        while not win_condition:
            for player in (self.player_one, self.player_two):
                self.game.turn = self.game.turn + 1

                print(f"{player.username}'s turn.")
                if player is self.player_one:
                    board = self.board_one
                    other = self.board_two
                else:
                    board = self.board_two
                    other = self.board_one
                self.draw(player, board)
                print(board)
                print("Current hand:")
                for monster in board.monsters:
                    if monster.state == State.Hand:
                        print(monster)

                print("Active monsters:")
                print(board.monsters)

                print("Active effects:")
                print(board.monster_effects)

                activate_monster = query_yes_no("Do you want to activate a"
                                                " monster?")
                if activate_monster:
                    monster_id = int(input("Enter monster_id from hand: "))
                    monster = Monster.query\
                                     .filter_by(id=monster_id).first()
                    self.activate_monster(monster, board)

                activate_effect = query_yes_no("Do you want to activate an"
                                               " effect?")
                if activate_effect:
                    effect_id = int(input("Enter effect_id from hand: "))
                    effect = MonsterEffect\
                        .query\
                        .filter_by(id=effect_id).first()
                    self.activate_monster(effect, board)

                attack = query_yes_no("Do you want to attack?")

                if attack:
                    attacker_id = int(input("Enter attacker id: "))
                    defender_id = int(input("Enter defender id: "))

                    attacker = Monster.query\
                                      .filter_by(id=attacker_id).first()
                    defender = Monster.query\
                                      .filter_by(id=defender_id).first()
                    self.attack((board, other), attacker, defender)

            if self.board_one.health <= 0:
                win_condition = True
                if self.board_two.health > 0:
                    print("Player 2 wins!")
                    self.player_two.wins = self.player_two.wins + 1
                    self.player_one.losses = self.player_one.losses + 1
                else:
                    print("Tie!")
                    self.player_one.ties = self.player_one.ties + 1
                    self.player_two.ties = self.player_two.ties + 1
            else:
                if self.board_two.health <= 0:
                    win_condition = True
                    if self.board_one.health > 0:
                        print("Player 1 wins!")
                        self.player_one.wins = self.player_one.wins + 1
                        self.player_two.losses = self.player_two.losses + 1


if __name__ == "__main__":
    charlie = User.query.filter_by(username='charlie').first()
    david = User.query.filter_by(username='david').first()

    Battle = Controller(charlie, david)
    Battle.play()
