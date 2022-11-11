from otree.api import *
import numpy as np
import random

doc = """
Get the note written in Guess if the sound is heard or not for a single trial for which only one light is shown.
"""


class C(BaseConstants):
    NAME_IN_URL = 'Pay'
    PLAYERS_PER_GROUP = None
    # there is only one round because only one case is selected for the guess.
    # The case selected is random at participant level
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    pass


class Feedback(Page):
    @staticmethod
    def vars_for_template(player: Player):
        participant = player.participant
        pay2 = 0
        draw = random.sample([i for i in range(len(participant.guesses))], 1)
        if participant.guesses[draw[0]] == participant.sound[draw[0]]:
            pay2 = 25
            player.payoff += 25
        else:
            player.payoff += 0

        return dict(pay=participant.payoff, guesses=sum(participant.guesses), p2=pay2,
                    total=participant.payoff_plus_participation_fee())


class ResultsWaitPage(WaitPage):
    pass


page_sequence = [Feedback]
