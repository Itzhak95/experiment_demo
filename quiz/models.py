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
    name_in_url = 'quiz'
    players_per_group = None
    num_rounds = 1

    max_value = 100
    seconds_for_timed_page = 60 * 5

    bid_step = 1


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
    q2b = models.IntegerField(label="How many tokens do you win (you may enter 0)?")
    q2c = models.IntegerField(label="How many tokens does your opponent win (you may enter 0)?")
    q3a = models.BooleanField(
        label="Do you win the auction?",
        choices=[(True, "Yes"), (False, "No")],
        widget=widgets.RadioSelect
    )
    q3b = models.IntegerField(label="How many tokens do you win (you may enter 0)?")
    q3c = models.IntegerField(label="How many tokens does your opponent win (you may enter 0)?")

    def live_quiz(self, data):
        is_next_q = data['is_next_q']
        alter_bid_cancelled = data['alter_bid_cancelled']
        if is_next_q:
            self.participant.vars['q'] = self.set_quiz_q(alter_bid_cancelled)
            errors = dict()
            is_next_q = False
        else:
            errors = self.quiz_error_message(data['values'], alter_bid_cancelled)
            is_next_q = True
        return {self.id_in_group: dict(question=self.participant.vars['q'], errors=errors, is_next_q=is_next_q)}

    def set_quiz_q(self, alter_bid_cancelled):
        bid_step = self.session.config['bid_step']
        ego_v = choice(list(range(bid_step * 2, Constants.max_value + 1)))
        alter_v = choice(list(range(bid_step * 1, Constants.max_value + 1)))
        if alter_bid_cancelled:
            alter_b = choice(list(range(bid_step * 1, alter_v, bid_step)))
            ego_b = choice(list(range(0, min(alter_b, ego_v), bid_step)))
        else:
            ego_b = choice(list(range(bid_step * 1, ego_v, bid_step)))
            alter_b = choice(list(range(0, min(ego_b, alter_v), bid_step)))
        return dict(ego_v=ego_v, ego_b=ego_b, alter_v=alter_v, alter_b=alter_b)

    def quiz_error_message(self, values, alter_bid_cancelled):
        q = self.participant.vars['q']
        fields = list(values.keys())
        a = [True, q['ego_v'] - q['ego_b'], 0]
        if not alter_bid_cancelled:
            if q['ego_b'] < q['alter_b']:
                a = [False, 0, q['alter_v'] - q['alter_b']]
        corrects = {k: v for k, v in zip(fields, a)}
        if alter_bid_cancelled:
            msg = {fields[0]: f"Since your opponent’s bid was cancelled but yours was not, you win the auction.",
                   fields[1]: f"Since you win the auction, you receive your valuation of {q['ego_v']} minus "
                              f"your bid of {q['ego_b']} tokens, or {q['ego_v'] - q['ego_b']} tokens.",
                   fields[2]: 'Since your opponent loses the auction, they don’t gain any tokens (so the answer is 0).'}
        else:
            msg = {fields[0]: f"Since you bid {q['ego_b']} and your opponent only bid {q['alter_b']}, "
                              f"you win the auction.",
                   fields[1]: f"Since you win the auction, you receive your valuation of {q['ego_v']} minus your bid "
                              f"of {q['ego_b']} tokens, or {q['ego_v'] - q['ego_b']} tokens.",
                   fields[2]: 'Since your opponent loses the auction, they don’t gain any tokens (so the answer is 0).'}
        errors = dict()
        for k in values.keys():
            if values[k] != corrects[k]:
                    errors[k] = msg[k]
        return errors
