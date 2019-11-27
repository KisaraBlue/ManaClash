import random

from manaclash import db
# db.drop_all()
# db.create_all()

from manaclash import User, Game, CardsInGame
from manaclash import Card
from manaclash import Type, Archetype, Category
#from manaclash.models import board_monster_effect

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
        self.game.turn = int(0)
        self.game.health1 = 10
        self.game.health2 = 10
        print("Game:", self.game)

        self.player_one = player_one
        self.player_two = player_two
        print("Players: ", self.player_one, self.player_two)

        #self.board_one = Board(self.game.id, self.game.player_one.id)
        #self.board_two = Board(self.game.id, self.game.player_two.id)

        db.session.add(self.game)
        #db.session.add(self.board_one)
        #db.session.add(self.board_two)
        db.session.commit()

    def activate_card(self, cardingame):
        cardingame.state = 2


        #db.session.add(board)
        db.session.commit()

    #def evaluate_effects(self, board, monster):
    def evaluate_effects(self, creature):
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

        active_cards_id = db.session.query(CardsInGame.card_id).filter(CardsInGame.state == 2).filter(CardsInGame.game_id == self.game)
        active_effects = db.session.query(Card).filter(Card.category == 1).filter(Card.card_id.in_(active_cards_id))
        for effect in active_effects:
            affected_types = False
            affected_archetypes = False
            
            #in case no type/archetype is mentionned, it works for all
            defined_types = False
            defined_archetypes = False

            for type in creature.types:
                defined_types = True
                if type in effect.types:
                    affected_types = True
            if defined_types == False:
                affected_types = True

            for archetype in creature.archetypes:
                defined_archetypes = True
                if archetype in effect.archetypes:
                    affected_archetypes = True
            if defined_archetypes == False:
                affected_archetypes = True
            
            if (affected_types and affected_archetypes):
                attack_bonus += effect.attack_points
                defense_bonus += effect.defense_points

        return (attack_bonus, defense_bonus)

    def evaluate_equipment(self, board, monster):
        """
        For now, we will not allow a player to draw any equipment cards, and so
        this will not be included in the Phase One submission.
        """
        pass

    #def attack(self, boards, attacker, defender):
    def attack(self, attacker, defender):
        #attacker and defender are instances of CardsInGame
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
        #attacker_eval = self.evaluate_effects(boards[0], attacker)[0]
        #defender_eval = self.evaluate_effects(boards[1], defender)[1]

        attacker_eval = self.evaluate_effects(attacker)[0]
        defender_eval = self.evaluate_effects(defender)[1]

        total_attack = attacker.attack_points + attacker_eval
        total_defense = defender.defense_points + defender_eval

        if total_attack > total_defense:
            print(attacker, defender)
            #boards[1].health = boards[1].health - 1
            if defender.player == 1:
                self.game.health1 -= 1
            else:
                self.game.health2 -= 1
            #boards[1].monsters.remove(defender)
            defender.state = 3

            print("Attack succeeded!")
        else:
            print("Attack failed!")
        db.session.commit()

        return defender.state

    def draw(self, user_id):
        
        player = 0
        if self.player_one == user_id:
            player = 1
        else:
            player = 2
        cards_in_deck = db.session.query(CardsInGame).filter(CardsInGame.state == 0).filter(CardsInGame.game_id == self.game.id).filter(CardsInGame.player == player)
        left = cards_in_deck.count()
        if left > 0:
            x = random.randrange(left)
            card_drawn = cards_in_deck[x]
            cards_in_deck[x].state = 1
        else:
            print("no more cards")
            card_drawn = None

        db.session.commit()
        return card_drawn


    def play(self):
        print("Game started.")
        print("Drawing initial hand.")
        for i in range(6):
            self.draw(self.game.player_one.id)
            self.draw(self.game.player_two.id)

        win_condition = False
        while not win_condition:
            for player in (self.player_one, self.player_two):
                self.game.turn = self.game.turn + 1

                print(f"{player.username}'s turn.")
                
                self.draw(player)
                print("Current hand:")
                #print(board.hand_monsters, board.hand_monster_effects)

                print("Active monsters:")
                #print(board.monsters)

                print("Active effects:")
                #print(board.monster_effects)

                activate_card = query_yes_no("Do you want to activate a"
                                                " monster?")
                """if activate_monster:
                    monster_id = int(input("Enter monster_id from hand: "))
                    monster = Monster.query\
                                     .filter_by(id=monster_id).first()
                    self.activate_monster(monster, board)"""
                if activate_card:
                    card_id = int(input("Enter card_id from hand: "))
                    card = db.session.query(CardsInGame).filter_by(id=card_id).first()
                    self.activate_card(card)
                    #if equipment, one more step

                print("Current hand:")
                #print(board.hand_monsters, board.hand_monster_effects)

                print("Active monsters:")
                #print(board.monsters)

                print("Active effects:")
                #print(board.monster_effects)

                attack = query_yes_no("Do you want to attack?")

                if attack:
                    attacker_id = int(input("Enter attacker id: "))
                    defender_id = int(input("Enter defender id: "))

                    attacker = db.session.query(CardsInGame).filter_by(id=attacker_id).first()
                    defender = db.session.query(CardsInGame).filter_by(id=defender_id).first()
                    self.attack(attacker, defender)

            if self.game.health1 <= 0:
                win_condition = True
                if self.game.health2 > 0:
                    print("Player 2 wins!")
                    self.player_two.wins = self.player_two.wins + 1
                    self.player_one.losses = self.player_one.losses + 1
                else:
                    print("Tie!")
                    self.player_one.ties = self.player_one.ties + 1
                    self.player_two.ties = self.player_two.ties + 1
            else:
                if self.game.health2 <= 0:
                    win_condition = True
                    if self.game.health1 > 0:
                        print("Player 1 wins!")
                        self.player_one.wins = self.player_one.wins + 1
                        self.player_two.losses = self.player_two.losses + 1


if __name__ == "__main__":
    user1 = User.query.filter_by(username='Persona1').first()
    user2 = User.query.filter_by(username='Persona2').first()

    grim = Card.query.filter_by
    Battle = Controller(user1, user2)
    Battle.play()
