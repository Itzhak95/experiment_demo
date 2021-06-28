from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from random import shuffle, randint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'arad_rubinstein'
    players_per_group = 2
    num_rounds = 1
    small_bonus = 100
    large_bonus = 200

    decision_min = 11
    decision_max = 20

    seconds_for_timed_page = 60 * 5


class Subsession(BaseSubsession):
    def set_groups_for_curr_round(self):
        size = Constants.players_per_group
        players = self.get_players()
        unmatched = []
        active_players = [p.participant.id_in_session for p in players if not p.participant.vars.get('is_dropout')]
        shuffle(active_players)
        if len(active_players) % 2 == 1:
            unmatched.append(active_players.pop())
        new_matrix = [active_players[n:n+size] for n in range(0, len(active_players), size)]
        if unmatched:
            for p in players:
                if p.participant.id_in_session in unmatched:
                    p.participant.vars['is_unmatched'] = True
            new_matrix.append(unmatched)
        dropouts = [p.participant.id_in_session for p in players if p.participant.vars.get('is_dropout')]
        if dropouts:
            new_matrix.append(dropouts)
        self.set_group_matrix(new_matrix)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    decision = models.IntegerField(label="What number will you choose?",
                                   min=Constants.decision_min, max=Constants.decision_max)
    explanation = models.LongStringField(label="")

    def get_other(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        alter_decision = self.get_other().decision
        if not alter_decision:
            alter_decision = randint(Constants.decision_min, Constants.decision_min)
        payoff = 10 * self.decision if self.decision else 0
        payoff += Constants.large_bonus if self.decision == alter_decision - 1 else 0
        payoff += Constants.small_bonus if self.decision == alter_decision else 0
        self.payoff = payoff
