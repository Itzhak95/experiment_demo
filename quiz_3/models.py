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

from random import choice

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'quiz_3'
    players_per_group = None
    num_rounds = 1

    max_value = 100
    seconds_for_timed_page = 60 * 5


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    q1 = models.StringField(label="")
    q2a = models.BooleanField(
        label="Do you win the auction?",
        choices=[(True, "Yes"), (False, "No")],
        widget=widgets.RadioSelect
    )
    q2b = models.IntegerField(
        label="How many tokens do you win (you may enter a negative number if you lose tokens)?")
    q2c = models.IntegerField(
        label="How many tokens does the opponent win (you may enter a negative number if they lose tokens)?")

    def live_quiz(self, data):
        is_next_q = data['is_next_q']
        if is_next_q:
            self.participant.vars['q'] = self.set_quiz_q()
            errors = dict()
            is_next_q = False
        else:
            errors = self.quiz_error_message(data['values'])
            is_next_q = True
        return {self.id_in_group: dict(question=self.participant.vars['q'], errors=errors, is_next_q=is_next_q)}

    def set_quiz_q(self):
        bid_step = self.session.config['bid_step']
        alter_v = choice(list(range(bid_step * 2, Constants.max_value + 1)))
        alter_b = choice(list(range(bid_step * 1, alter_v, bid_step)))
        ego_v = choice(list(range(bid_step * 1, Constants.max_value + 1)))
        ego_b = choice(list(range(0, min(alter_b, ego_v), bid_step)))
        return dict(ego_v=ego_v, ego_b=ego_b, alter_v=alter_v, alter_b=alter_b)

    def quiz_error_message(self, values):
        q = self.participant.vars['q']
        fields = list(values.keys())
        a = [True, q['ego_v'] - q['ego_b'], -q['alter_b']]
        if q['ego_b'] < q['alter_b']:
            a = [False, -q['ego_b'], q['alter_v'] - q['alter_b']]
        corrects = {k: v for k, v in zip(fields, a)}
        msg = {fields[0]: f"Since the opponent bid {q['alter_b']} and you bid only {q['ego_b']}, you lose the auction.",
               fields[1]: f"Since you lose the auction, you lose your bid of {q['ego_b']} tokens "
                          f"(so the answer is {-q['ego_b']}).",
               fields[2]: f"Since the opponent wins the auction, they receive their valuation of {q['alter_v']} "
                          f"tokens minus their bid of {q['alter_b']} tokens, or {q['alter_v'] - q['alter_b']} "
                          f"tokens in total."}
        errors = dict()
        for k in values.keys():
            if values[k] != corrects[k]:
                    errors[k] = msg[k]
        return errors
